from playwright.sync_api import Page, expect
from pages.bill_pay_page import BillPayPage
from pages.transfer_funds_page import TransferFundsPage
import pytest, uuid
from helpers import get_balance

def test_transfer_in_ui_moves_balances_in_api(overview, page, api, api_base_url, test_user, existing_account_id, second_account_id):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_from = existing_account_id
    account_from_balance = get_balance(api, api_base_url, account_from)
    account_to = second_account_id
    account_to_balance = get_balance(api, api_base_url, account_to)
    overview.go_to_transfer_funds()
    transfer_page = TransferFundsPage(page)
    transfer_page.transfer(10, account_from, account_to)
    expect(transfer_page.heading_complete).to_be_visible()
    expect(transfer_page.result_from_account).to_have_text(str(account_from))
    expect (transfer_page.result_to_account).to_have_text(str(account_to))
    expect (transfer_page.result_amount).to_have_text("$10.00")
    account_from_after = get_balance(api, api_base_url, account_from)
    account_to_after = get_balance(api, api_base_url, account_to)
    assert account_from_after == pytest.approx(account_from_balance - 10)
    assert account_to_after == pytest.approx(account_to_balance + 10)

def test_bill_pay_in_ui_shows_in_api(overview, page, api, api_base_url, first_account):
    from_id = first_account["id"]
    balance = first_account["balance"]
    payee_name = f"name_{uuid.uuid4().hex[:5]}"
    overview.go_to_bill_pay()
    bill_pay_page = BillPayPage(page)
    bill_pay_page.pay_bill(payee_name, 10, from_id)
    expect(bill_pay_page.success_heading).to_be_visible()
    expect(bill_pay_page.result_payee_name).to_have_text(str(payee_name))
    expect(bill_pay_page.result_from_account).to_have_text(str(from_id))
    expect(bill_pay_page.result_amount).to_have_text("$10.00")
    account_from_after = get_balance(api, api_base_url, from_id)
    assert account_from_after == pytest.approx(balance - 10)
    expected_description = f"Bill Payment to {payee_name}"
    response = api.get(f"{api_base_url}/accounts/{from_id}/transactions")
    assert response.status_code == 200
    transactions = response.json()
    mine = [t for t in transactions if t["description"] == expected_description]
    assert len(mine) == 1
    payment = mine[0]
    assert payment["type"] == "Debit"
    assert payment["amount"] == pytest.approx(10)