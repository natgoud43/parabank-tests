from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage
from pages.account_details_page import AccountDetailsPage

def test_ui_shows_all_accounts_from_api(overview, api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts")
    assert response.status_code == 200 
    api_ids = [str(account["id"]) for account in response.json()]
    assert api_ids
    expect(overview.heading).to_be_visible()
    ui_ids = overview.account_ids()

    for account_id in api_ids:
        assert account_id in ui_ids

def test_greeting_message_uses_correct_customer_name(api, api_base_url, overview):
    response = api.get(f"{api_base_url}/customers/12212")
    assert response.status_code == 200
    body = response.json()
    assert body
    customer_first_name = body["firstName"]
    customer_last_name = body["lastName"]
    expect(overview.greeting).to_contain_text("Welcome")
    expect(overview.greeting).to_contain_text(f" {customer_first_name} {customer_last_name}")

def test_account_type_is_presented_correctly_in_ui(page:Page, overview, api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_id = body[0]["id"]
    account_type = body[0]["type"]
    overview.open_account(account_id)                           
    account_details = AccountDetailsPage(page)
    expect(account_details.heading).to_be_visible()
    expect(account_details.account_id).to_have_text(f"{account_id}")
    expect(account_details.account_type).to_have_text(f"{account_type}")

