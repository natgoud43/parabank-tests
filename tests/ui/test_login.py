from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage
import pytest

pytestmark = pytest.mark.ui

def test_login_with_valid_user_shows_accounts_overview(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("john", "demo")
    overview = OverviewPage(page)
    expect(overview.heading).to_be_visible()

def test_logout_returns_to_login_page(overview, page):
    overview.log_out()
    expect(page.locator("#leftPanel")).to_contain_text("Customer Login")

@pytest.mark.parametrize("user, password, error", [
    pytest.param("john", "wrong", "The username and password could not be verified.", marks=pytest.mark.xfail(strict=False,raises=AssertionError, reason="Intermittent Parabank error handling")),
    pytest.param("nobody12", "demo", "The username and password could not be verified.", marks=pytest.mark.xfail(strict=False,raises=AssertionError, reason="Intermittent Parabank error handling")),
    ("", "", "Please enter a username and password."),
    ("john", "", "Please enter a username and password.")
], ids = ["wrong-password","wrong-username", "empty-username-password", "empty-password"]
)
def test_invalid_login_credentials(page: Page, user, password, error):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user,password)
    expect(login_page.error_heading).to_be_visible()
    expect(login_page.error_message).to_contain_text(error)





                                                   



