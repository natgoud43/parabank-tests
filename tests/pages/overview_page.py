from playwright.sync_api import expect

class OverviewPage:
    def __init__(self, page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Accounts Overview")
        self.account_links = page.locator("#accountTable a")
        self.transfer_funds = page.get_by_role("link", name="Transfer Funds")
        self.greeting = page.locator("#leftPanel")

    def account_ids(self):
        expect(self.account_links.first).to_be_visible()
        return self.account_links.all_inner_texts()

    def open_account(self, account_id):
        self.page.get_by_role("link", name=str(account_id), exact=True).click()

    def go_to_transfer_funds(self):
        self.transfer_funds.click()

    def log_out(self):
        self.page.get_by_role("link", name="Log Out").click()