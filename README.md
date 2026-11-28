# Parabank Tests
![Parabank tests suite](https://github.com/natgoud43/parabank-tests/actions/workflows/tests.yml/badge.svg)

Pytest tests for the [Parabank](https://parabank.parasoft.com) demo bank, on two layers: the **REST API** (requests) and the **web UI** (Playwright), plus **cross-checks** that compare the two.

## What the suite checks

### Sign-in

| Check | API | UI | Cross-check |
| --- | :-: | :-: | :-: |
| A valid login shows Accounts Overview | | ✅ | |
| Logout returns to the login page | | ✅ | |
| Invalid credentials show the right error (wrong password, unknown user, empty fields) | | ✅ | |
| Registering a new customer shows a personal welcome | | ✅ | |

### Customer

| Check | API | UI | Cross-check |
| --- | :-: | :-: | :-: |
| A customer has a first and last name | ✅ | | |
| A customer's address has all fields | ✅ | | |
| Unknown and invalid customer ids return the expected errors | ✅ | | |
| The greeting shows the customer's name from the API | ✅ | ✅ | ✅ |

### Accounts

| Check | API | UI | Cross-check |
| --- | :-: | :-: | :-: |
| Every account belongs to its customer | ✅ | | |
| Account details follow the rules (id, customer, known type) | ✅ | | |
| Creating an account returns a new CHECKING account in the customer's list | ✅ | | |
| Accounts Overview shows every account the API returns | ✅ | ✅ | ✅ |
| An account's details page shows the API's type | ✅ | ✅ | ✅ |
| An account created via the API appears in the UI | ✅ | ✅ | ✅ |

### Payments

| Check | API | UI | Cross-check |
| --- | :-: | :-: | :-: |
| A transfer in the UI moves both balances by exactly the amount | ✅ | ✅ | ✅ |
| A bill paid in the UI lowers the balance, and exactly one matching debit appears | ✅ | ✅ | ✅ | 
| A transfer via the API moves the amount between the two accounts| ✅ | | |
| A bill paid via the API lowers the balance, and exactly one matching debit appears | ✅ | | |

## Known issues (by design: xfail)
- For customer id "0" and "99999999" Parabank returns code 400.

## Findings
- Lookups of non-existent customers return 400 instead of 404; the server log shows the error handler itself failing ("An unexpected error occurred during error handling") and logging an expected "not found" as an ERROR with a stack trace.

## Design notes
- **Its own server in CI.** Each CI job starts a private Parabank from the official Docker image, waits until it answers, and seeds known demo data, so results never depend on the shared public site.
- **One address setting.** All tests read the server address from base_url (the public site by default, localhost in CI).
- **Both layers read at the same moment.** Cross-checks call the API inside the test, right before checking the UI, so data changes on the shared server don't cause false failures.
- **Test data comes from the API.** No hard-coded account ids: tests ask the API for a real account first, because accounts on the demo server come and go.
- **Exact for values, contains for containers.** Single values (an account id or type) are checked exactly; page sections are checked with "contains".
- **Same tests, any browser.** Browser settings come from the command line, not the code. CI runs headless with the Chrome preinstalled on Ubuntu, so a full run takes about 30 seconds.
- **Page objects.** Each page has a class in `pages/` that holds its locators and actions (`LoginPage`, `OverviewPage`, `AccountDetailsPage`). Tests press their buttons and do all the asserting, so a change on the website is fixed in one place.
- **Act in one layer, verify in the other.** UI actions are confirmed through the API, so the UI never grades itself.
- **Tests start where they need to.** An overview fixture logs in through LoginPage, so only the login tests log in by hand.
- **Its own test user.** Each run registers a fresh customer once (session fixture), and tests that need money create their own accounts through the API, so every test passes alone and in any order.
- **Unique markers to find your own data.** Each bill payment uses a unique payee name, so the test can find exactly its own transaction among all of the account's transactions.
- **Labels by what a test needs, applied automatically.** A conftest hook marks every test that needs a browser (directly or through a fixture) as `ui`, and every other test as `api`. CI runs the two labels as separate jobs. Markers are registered with `--strict-markers`, so a typo can't create a new label, and no test can end up unlabeled and silently skipped by both jobs.
- **Grouped by feature.** Tests live in one file per feature (sign-in, customer, account, payment), so a reader finds a feature's API, UI and cross-checks in one place.
- **Random amounts.** A fixture picks a random whole amount for each money test, so values vary between runs; failure messages always show the amount used.

## Project structure:
parabank-tests/
├── .github/workflows/tests.yml    # two CI jobs (api, ui), each with its own Parabank in Docker
├── README.md
├── pytest.ini                     # base_url, markers, --strict-markers
├── requirements.txt
└── tests/
    ├── conftest.py                # fixtures (api session, test_user, accounts, overview) + auto-labeling hook
    ├── helpers.py                 # get_balance, find_transactions
    ├── pages/                     # page objects: locators and actions, no asserts
    │   ├── login_page.py
    │   ├── register_page.py
    │   ├── overview_page.py
    │   ├── account_details_page.py
    │   ├── transfer_funds_page.py
    │   └── bill_pay_page.py
    ├── test_sign_in.py            # login, wrong logins, logout, register
    ├── test_customer.py           # name, address, unknown ids, greeting
    ├── test_account.py            # account rules, create, UI account checks
    └── test_payment.py            # transfer, bill pay
## How to run

> **Note about the public site:** parabank.parasoft.com is shared and sometimes unstable. Wrong-credential logins occasionally return "An internal error has occurred", and the site may block automated browsers. For reliable results, run against the Docker image (see "Run locally with Docker").

```
pip install -r requirements.txt
python -m pytest                                 # everything, headless
python -m pytest tests/api                       # API tests only
python -m pytest tests/ui --headed --slowmo 500  # watch the browser
```

On Windows with Smart App Control, add `--browser-channel chrome` to use the installed, signed Chrome.

## Run locally with Docker (recommended)

The public Parabank site sometimes blocks automated browsers, so run a private copy:

```
docker run -d --name parabank -p 8080:8080 parasoft/parabank
curl -X POST http://localhost:8080/parabank/services/bank/initializeDB
python -m pytest --base-url http://localhost:8080/parabank/
```
