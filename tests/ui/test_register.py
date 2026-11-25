from playwright.sync_api import expect
from pages.register_page import RegisterPage

def test_register_new_customer_shows_welcome(page, new_username):
    register_page = RegisterPage(page)
    register_page.open()
    register_page.register(new_username, "Test12345")
    expect (register_page.welcome_heading).to_have_text(f"Welcome {new_username}")
