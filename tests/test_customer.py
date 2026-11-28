import pytest
from playwright.sync_api import expect
from pages.account_details_page import AccountDetailsPage

def test_customer_has_a_name(api, api_base_url, test_user):
    response = api.get(f"{api_base_url}/customers/{test_user['customer_id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["firstName"]
    assert body["lastName"]

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

def test_greeting_message_uses_correct_customer_name(api, api_base_url, overview, test_user):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}")
    assert response.status_code == 200
    body = response.json()
    assert body
    customer_first_name = body["firstName"]
    customer_last_name = body["lastName"]
    expect(overview.greeting).to_contain_text("Welcome")
    expect(overview.greeting).to_contain_text(f" {customer_first_name} {customer_last_name}")