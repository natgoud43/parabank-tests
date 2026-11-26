from playwright.sync_api import expect
import pytest, requests, uuid
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage

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
def overview(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("john", "demo")
    overview = OverviewPage(page)
    expect(overview.heading).to_be_visible()
    return overview

@pytest.fixture
def existing_account_id(api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_id = body[0]["id"]
    return account_id

@pytest.fixture
def new_username():
    return f"qa_{uuid.uuid4().hex[:8]}"