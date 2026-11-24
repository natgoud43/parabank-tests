import pytest

pytestmark = pytest.mark.api

def test_customer_has_expected_name(api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212")
    assert response.status_code == 200
    body = response.json()
    assert body["firstName"] == "John"

def test_all_accounts_belong_to_customer(api,api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts")
    assert response.status_code == 200
    accounts = response.json()
    for account in accounts:
        assert account["customerId"] == 12212

def test_account_details_follow_the_rule(api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_id = body[0]["id"]
    raw_account = api.get(f"{api_base_url}/accounts/{account_id}")
    assert raw_account.status_code == 200
    account = raw_account.json()
    assert account["customerId"] == 12212
    assert account["id"] == account_id
    assert account["type"] in ["CHECKING", "SAVINGS", "LOAN"]

def test_customer_address_has_all_fields(api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212")
    assert response.status_code == 200
    body = response.json()
    for key in ["street","city","state","zipCode"]:
        assert key in body["address"]
    
def test_unknown_customer_returns_400(api, api_base_url):
    response = api.get(f"{api_base_url}/customers/9999999")
    assert response.status_code == 400
    assert "Could not find customer" in response.text

@pytest.mark.parametrize("id, response_code", [
    pytest.param("0", 404, marks=pytest.mark.xfail(raises=AssertionError, reason="Parabank returns 400")),
    pytest.param("99999999", 404, marks=pytest.mark.xfail(raises=AssertionError, reason="Parabank returns 400")),
    ("-1", 400),
    ("abc", 404)
])
def test_not_existing_and_invalid_customer_id(api, api_base_url, id, response_code):
    response = api.get(f"{api_base_url}/customers/{id}")
    assert response.status_code == response_code
    