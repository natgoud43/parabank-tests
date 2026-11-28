import pytest
from playwright.sync_api import expect
from pages.account_details_page import AccountDetailsPage

def test_all_accounts_belong_to_customer(api,api_base_url, test_user):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}/accounts")
    assert response.status_code == 200
    accounts = response.json()
    for account in accounts:
        assert account["customerId"] == customer_id

def test_account_details_follow_the_rule(api, api_base_url, test_user):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_id = body[0]["id"]
    raw_account = api.get(f"{api_base_url}/accounts/{account_id}")
    assert raw_account.status_code == 200
    account = raw_account.json()
    assert account["customerId"] == customer_id
    assert account["id"] == account_id
    assert account["type"] in ["CHECKING", "SAVINGS", "LOAN"]

def test_account_type_is_presented_correctly_in_ui(page, overview,first_account):
    account_id = first_account["id"]
    account_type = first_account["type"]
    overview.open_account(account_id)                           
    account_details = AccountDetailsPage(page)
    expect(account_details.heading).to_be_visible()
    expect(account_details.account_id).to_have_text(str(account_id))
    expect(account_details.account_type).to_have_text(str(account_type))

def test_create_account_returns_new_account(api, api_base_url, existing_account_id, test_user):
    customer_id = test_user["customer_id"]
    from_id = existing_account_id
    response = api.post(f"{api_base_url}/createAccount", params={
        "customerId": customer_id,
        "newAccountType": 0,
        "fromAccountId": from_id
    })
    assert response.status_code == 200
    new_account = response.json()
    assert new_account
    new_id = new_account["id"]
    assert new_account["customerId"] == customer_id
    assert new_account["id"] != from_id
    assert new_account["type"] == "CHECKING"
    response = api.get(f"{api_base_url}/customers/{customer_id}/accounts")
    assert response.status_code == 200
    ids = [a["id"] for a in response.json()]
    assert new_id in ids

def test_ui_shows_all_accounts_from_api(overview, api, api_base_url, test_user):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}/accounts")
    assert response.status_code == 200 
    api_ids = [str(account["id"]) for account in response.json()]
    assert api_ids
    expect(overview.heading).to_be_visible()
    ui_ids = overview.account_ids()

    for account_id in api_ids:
        assert account_id in ui_ids

def test_new_account_exists_in_ui(api, api_base_url, page, overview, existing_account_id, test_user):
    customer_id = test_user["customer_id"]
    from_id = existing_account_id
    response = api.post(f"{api_base_url}/createAccount", params={
        "customerId": customer_id,
        "newAccountType": 0,
        "fromAccountId": from_id
    })
    assert response.status_code == 200
    new_account = response.json()
    assert new_account
    new_id = new_account["id"]
    page.reload()
    ui_ids = overview.account_ids()
    assert str(new_id) in ui_ids
