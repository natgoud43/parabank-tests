from pages.bill_pay_page import BillPayPage
import pytest, uuid
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

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
    account_from_after = api.get(f"{api_base_url}/accounts/{from_id}").json()["balance"]
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
    


