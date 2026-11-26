# Parabank Tests
![Parabank tests suite](https://github.com/natgoud43/parabank-tests/actions/workflows/tests.yml/badge.svg)

Pytest tests for the [Parabank](https://parabank.parasoft.com) demo bank, on two layers: the **REST API** (requests) and the **web UI** (Playwright), plus **cross-checks** that compare the two.

## What the suite checks

### API (`tests/api`)
- An existing customer's details include the expected first name.
- Every account returned for a customer belongs to that customer (customerId matches).
- Account details follow the rules: correct id and customer, and a known account type.
- A customer's address has all its fields (street, city, state, zipCode).
- Unknown customer ids return 404 (expected by REST convention; see Known issues); -1 returns 400; a non-numeric id returns 404
- Creating an account via the API returns a new CHECKING account, which appears in the customer's account list

### UI (`tests/ui`)
- Logging in with a valid user shows Accounts Overview.
- A wrong password shows "The username and password could not be verified."
- Log Out returns to the Customer Login form.

### Cross-layer checks (`tests/ui/test_cross_checks.py`)
- Every account the API returns appears on the Accounts Overview page.
- The greeting shows the customer name the API returns.
- An account's details page shows the same account type as the API.
- A transfer made through the UI moves both balances by exactly the amount, verified through the API before and after
- A new account created via the API appears on the Accounts Overview page

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

## Project structure:
parabank-tests/
├── .github/workflows/tests.yml
├── README.md
├── pytest.ini
├── requirements.txt
├── pages/                         # page objects: locators and actions, no asserts
│   ├── login_page.py
│   ├── overview_page.py
    ├── transfer_funds_page_page.py
│   └── account_details_page.py
└── tests/
    ├── conftest.py                # shared fixtures: api session, api_base_url
    ├── api/
    │   └── test_customers.py
    └── ui/
        ├── test_login.py
        └── test_cross_checks.py

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
