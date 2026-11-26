class LoginPage:
    def __init__(self, page):
        self.page = page
        self.error_message = page.locator("#rightPanel .error")
        self.error_heading = page.get_by_role("heading", name="Error!")

    def open(self):
        self.page.goto("index.htm")

    def login(self, username, password):
        self.page.locator("input[name='username']").fill(username)
        self.page.locator("input[name='password']").fill(password)
        self.page.get_by_role("button", name="Log In").click()



                                        
   