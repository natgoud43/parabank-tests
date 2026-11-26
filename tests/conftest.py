from playwright.sync_api import expect
import pytest, requests, uuid
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage
from pages.register_page import RegisterPage

BASE = "https://parabank.parasoft.com/parabank/services/bank"

@pytest.fixture(scope="session")
def api():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()

@pytest.fixture(scope="session")
def api_base_url(base_url):
    return f"{base_url}services/bank"

@pytest.fixture
def overview(page,test_user):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(test_user["username"], test_user["password"])
    overview = OverviewPage(page)
    expect(overview.heading).to_be_visible()
    return overview

@pytest.fixture
def existing_account_id(api, api_base_url, test_user):
    customer_id = test_user["customer_id"]
    response = api.get(f"{api_base_url}/customers/{customer_id}/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_id = body[0]["id"]
    return account_id

@pytest.fixture
def new_username():
    return f"qa_{uuid.uuid4().hex[:8]}"

@pytest.fixture(scope="session")
def test_user(browser, base_url, api, api_base_url):
    username = f"qa_{uuid.uuid4().hex[:8]}"
    password = "Tester12345"
    page = browser.new_page(base_url=base_url)
    register_page = RegisterPage(page)
    register_page.open()
    register_page.register(username, password)
    page.close()

    response = api.get(f"{api_base_url}/login/{username}/{password}")
    assert response.status_code == 200
    customer_id = response.json()["id"]
    return{"username": username, "password": password, "customer_id": customer_id}

@pytest.fixture
def second_account_id(api, api_base_url, test_user, existing_account_id):
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
    return new_id
