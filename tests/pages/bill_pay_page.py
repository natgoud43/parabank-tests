from playwright.sync_api import expect

class BillPayPage:
    def __init__ (self, page):
        self.page = page
        self.heading = page.get_by_role("heading", name= "Bill Payment Service")
        self.payee_name = page.locator("input[name='payee.name']")
        self.address = page.locator("input[name='payee.address.street']")
        self.city = page.locator("input[name='payee.address.city']")
        self.state = page.locator("input[name='payee.address.state']")
        self.zip = page.locator("input[name='payee.address.zipCode']")
        self.phone = page.locator("input[name='payee.phoneNumber']")
        self.payee_account = page.locator("input[name='payee.accountNumber']")
        self.verify_account = page.locator("input[name='verifyAccount']")
        self.amount = page.locator("input[name='amount']")
        self.from_account = page.locator("select[name='fromAccountId']")
        self.send_payment_button = page.get_by_role("button", name= "Send Payment")
        self.success_heading = page.get_by_role("heading", name = "Bill Payment Complete")
        self.result_payee_name = page.locator("#billpayResult #payeeName")
        self.result_amount = page.locator("#billpayResult #amount")
        self.result_from_account = page.locator("#billpayResult #fromAccountId")

    def pay_bill(self, payee_name, amount, from_account):
        expect(self.heading).to_be_visible()
        self.payee_name.fill(payee_name)
        self.address.fill("Street str., 19")
        self.city.fill("City")
        self.state.fill("State")
        self.zip.fill("987655")
        self.phone.fill("0912343434")
        self.payee_account.fill("563433")
        self.verify_account.fill("563433")
        self.amount.fill(str(amount))
        self.from_account.select_option(str(from_account))
        self.send_payment_button.click()






    