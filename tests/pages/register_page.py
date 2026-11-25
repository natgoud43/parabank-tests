class RegisterPage:
    def __init__(self, page):
        self.page=page
        self.first_name = page.locator("input[id='customer.firstName']")
        self.last_name = page.locator("input[id='customer.lastName']")
        self.street = page.locator("input[id='customer.address.street']")
        self.city = page.locator("input[id='customer.address.city']")
        self.state = page.locator("input[id='customer.address.state']")
        self.zip = page.locator("input[id='customer.address.zipCode']")
        self.phone = page.locator("input[id='customer.phoneNumber']")
        self.ssn = page.locator("input[id='customer.ssn']")
        self.username = page.locator("input[id='customer.username']")
        self.password = page.locator("input[id='customer.password']")
        self.confirm = page.locator("input[id='repeatedPassword']")
        self.register_button = page.get_by_role("button", name="Register")
        self.welcome_heading = page.locator("#rightPanel h1")
        self.success_panel = page.locator("#rightPanel")

    def open(self):
        self.page.goto("https://parabank.parasoft.com/parabank/register.htm")

    def register(self, username, password):
        self.first_name.fill("Tester")
        self.last_name.fill("Proud")
        self.street.fill("Green str., 11")
        self.city.fill("Town")
        self.state.fill("State")
        self.zip.fill("123456")
        self.phone.fill("0098436363")
        self.ssn.fill("8236634343")
        self.username.fill(username)
        self.password.fill(password)
        self.confirm.fill(password)
        self.register_button.click()