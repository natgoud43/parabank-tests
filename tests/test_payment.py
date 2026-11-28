from playwright.sync_api import Page, expect
from pages.bill_pay_page import BillPayPage
from pages.transfer_funds_page import TransferFundsPage
import pytest, uuid
from helpers import get_balance, find_transactions

def test_transfer_in_ui_moves_balances_in_api(overview, page, api, api_base_url, test_user, existing_account_id, second_account_id, amount):
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
    transfer_page.transfer(amount, account_from, account_to)
    expect(transfer_page.heading_complete).to_be_visible()
    expect(transfer_page.result_from_account).to_have_text(str(account_from))
    expect (transfer_page.result_to_account).to_have_text(str(account_to))
    expect (transfer_page.result_amount).to_have_text(f"${amount}.00")
    account_from_after = get_balance(api, api_base_url, account_from)
    account_to_after = get_balance(api, api_base_url, account_to)
    assert account_from_after == pytest.approx(account_from_balance - amount)
    assert account_to_after == pytest.approx(account_to_balance + amount)

def test_bill_pay_in_ui_shows_in_api(overview, page, api, api_base_url, first_account, amount):
    from_id = first_account["id"]
    balance = first_account["balance"]
    payee_name = f"name_{uuid.uuid4().hex[:5]}"
    overview.go_to_bill_pay()
    bill_pay_page = BillPayPage(page)
    bill_pay_page.pay_bill(payee_name, amount, from_id)
    expect(bill_pay_page.success_heading).to_be_visible()
    expect(bill_pay_page.result_payee_name).to_have_text(str(payee_name))
    expect(bill_pay_page.result_from_account).to_have_text(str(from_id))
    expect(bill_pay_page.result_amount).to_have_text(f"${amount}.00")
    account_from_after = get_balance(api, api_base_url, from_id)
    assert account_from_after == pytest.approx(balance - amount)
    mine = find_transactions(api, api_base_url, from_id, f"Bill Payment to {payee_name}")
    assert len(mine) == 1
    payment = mine[0]
    assert payment["type"] == "Debit"
    assert payment["amount"] == pytest.approx(amount)

def test_api_transfer_moves_the_amount_between_accounts(api, api_base_url, first_account, second_account_id, amount):
    from_account = first_account["id"]
    to_account = second_account_id
    from_before_balance = get_balance(api, api_base_url, from_account)
    to_before_balance = get_balance(api, api_base_url, to_account)
    response = api.post(f"{api_base_url}/transfer", params={
        "fromAccountId": from_account,
        "toAccountId": to_account,
        "amount": amount
        })
    assert response.status_code == 200
    expected = f"Successfully transferred ${amount} from account #{from_account} to account #{to_account}"
    assert response.text == expected
    assert get_balance(api, api_base_url, from_account) == pytest.approx(from_before_balance - amount)
    assert get_balance(api, api_base_url, to_account) == pytest.approx(to_before_balance + amount)

def test_api_pay_bill_moves_the_amount_from_account_and_transaction_exists(api, api_base_url, first_account, amount):
    account_id = first_account["id"]
    balance = get_balance(api, api_base_url, account_id)
    name = f"name_{uuid.uuid4().hex[:5]}"
    response = api.post(f"{api_base_url}/billpay", params={
        "accountId": account_id,
        "amount": amount
    }, json={
        "name": name,
        "address": {"street": "Street str., 77", "city":"City", "state":"State", "zipCode":"234554"},
        "phoneNumber": "098455334333",
        "accountNumber": "87658"
    })
    assert response.status_code  == 200
    payment = response.json()
    assert payment["payeeName"] == name
    assert payment["amount"] == pytest.approx(amount)
    assert payment["accountId"] == account_id
    assert get_balance(api, api_base_url, account_id) == pytest.approx(balance - amount)
    mine = find_transactions(api, api_base_url, account_id, f"Bill Payment to {name}")
    assert len(mine) == 1
    assert mine[0]["type"] == "Debit"
    assert mine[0]["amount"] == pytest.approx(amount)

