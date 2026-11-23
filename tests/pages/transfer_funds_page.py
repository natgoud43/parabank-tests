from playwright.sync_api import expect

class TransferFundsPage:
    def __init__(self, page):
        self.page = page
        self.amount = page.locator("#amount")
        self.from_account = page.locator("#fromAccountId")
        self.to_account = page.locator("#toAccountId")
        self.transfer_button = page.get_by_role("button", name="Transfer")
        self.heading_funds = page.get_by_role("heading", name = "Transfer Funds")
        self.heading_complete = page.get_by_role("heading", name= "Transfer Complete!")
        self.result_from_account = page.locator("#fromAccountIdResult")
        self.result_to_account = page.locator("#toAccountIdResult")
        self.result_amount = page.locator("#amountResult")


    def transfer(self, amount, from_id, to_id):
        expect(self.heading_funds).to_be_visible()
        self.amount.fill(str(amount))
        self.from_account.select_option(str(from_id))
        self.to_account.select_option(str(to_id))
        self.transfer_button.click()
        

