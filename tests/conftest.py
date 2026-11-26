from playwright.sync_api import expect
import pytest
import requests
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