class AccountDetailsPage:
    def __init__(self, page):
        self.page = page
        self.account_id = page.locator("#accountId")
        self.account_type = page.locator("#accountType")
        self.heading = page.get_by_role("heading", name="Account Details")
        self.account_balance = page.locator("#accountDetails #balance")



