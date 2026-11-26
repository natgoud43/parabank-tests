import pytest

pytestmark = pytest.mark.api

def test_customer_has_a_name(api, api_base_url, test_user):
    response = api.get(f"{api_base_url}/customers/{test_user['customer_id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["firstName"]
    assert body["lastName"]

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

def test_customer_address_has_all_fields(api, api_base_url, test_user):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}")
    assert response.status_code == 200
    body = response.json()
    for key in ["street","city","state","zipCode"]:
        assert key in body["address"]

@pytest.mark.parametrize("id, response_code", [
    pytest.param("0", 404, marks=pytest.mark.xfail(raises=AssertionError, reason="Parabank returns 400")),
    pytest.param("99999999", 404, marks=pytest.mark.xfail(raises=AssertionError, reason="Parabank returns 400")),
    ("-1", 400),
    ("abc", 404)
])
def test_not_existing_and_invalid_customer_id(api, api_base_url, id, response_code):
    response = api.get(f"{api_base_url}/customers/{id}")
    assert response.status_code == response_code

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

