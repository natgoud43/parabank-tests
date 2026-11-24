from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage
from pages.account_details_page import AccountDetailsPage
from pages.transfer_funds_page import TransferFundsPage
import pytest

pytestmark = pytest.mark.ui

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

#known risk for this test - other activities can be performed on shared server on same time 
def test_transfer_in_ui_moves_balances_in_api(overview, page, api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    assert len(body) >= 2
    account_from = body[0]["id"]
    account_from_balance = api.get(f"{api_base_url}/accounts/{account_from}").json()["balance"]
    account_to = body[1]["id"]
    account_to_balance = api.get(f"{api_base_url}/accounts/{account_to}").json()["balance"]
    overview.go_to_transfer_funds()
    transfer_page = TransferFundsPage(page)
    transfer_page.transfer(10, account_from, account_to)
    expect(transfer_page.heading_complete).to_be_visible()
    expect(transfer_page.result_from_account).to_have_text(str(account_from))
    expect (transfer_page.result_to_account).to_have_text(str(account_to))
    expect (transfer_page.result_amount).to_have_text("$10.00")
    account_from_after = api.get(f"{api_base_url}/accounts/{account_from}").json()["balance"]
    account_to_after = api.get(f"{api_base_url}/accounts/{account_to}").json()["balance"]
    assert account_from_after == pytest.approx(account_from_balance - 10)
    assert account_to_after == pytest.approx(account_to_balance + 10)

