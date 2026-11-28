from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.overview_page import OverviewPage
from pages.register_page import RegisterPage
import pytest

def test_login_with_valid_user_shows_accounts_overview(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("john", "demo")
    overview = OverviewPage(page)
    expect(overview.heading).to_be_visible()

def test_logout_returns_to_login_page(overview, page):
    overview.log_out()
    expect(page.locator("#leftPanel")).to_contain_text("Customer Login")

@pytest.mark.parametrize("user, password, error", [
    ("john", "pass", "The username and password could not be verified."),
    ("nobody12", "demo", "The username and password could not be verified."),
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

def test_register_new_customer_shows_welcome(page, new_username):
    register_page = RegisterPage(page)
    register_page.open()
    register_page.register(new_username, "Test12345")
    expect (register_page.welcome_heading).to_have_text(f"Welcome {new_username}")