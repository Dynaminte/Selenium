# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page untuk the-internet.herokuapp.com"""
    URL = 'https://the-internet.herokuapp.com/login'

    # ── Locators ──────────────────────────────────────
    USERNAME  = (By.ID, 'username')
    PASSWORD  = (By.ID, 'password')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button[type=submit]')
    FLASH_MSG = (By.ID, 'flash')
    FLASH_OK  = (By.CSS_SELECTOR, '.flash.success')
    FLASH_ERR = (By.CSS_SELECTOR, '.flash.error')

    # ── Actions ───────────────────────────────────────
    def navigate(self):
        self.open(self.URL)

    def enter_username(self, username):
        self.type(self.USERNAME, username)

    def enter_password(self, password):
        self.type(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BTN)

    def login(self, username, password):
        """High-level method: 1 baris di test = 1 aksi login"""
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertion helpers ─────────────────────────────
    def get_flash_message(self):
        return self.get_text(self.FLASH_MSG)

    def is_login_successful(self):
        return self.is_visible(self.FLASH_OK)

    def is_login_failed(self):
        return self.is_visible(self.FLASH_ERR)


class SauceDemoLoginPage(BasePage):
    """Login page khusus untuk saucedemo.com"""
    URL = 'https://www.saucedemo.com'

    # ── Locators ──────────────────────────────────────
    USERNAME  = (By.ID, 'user-name')
    PASSWORD  = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button')
    ERROR_MSG = (By.CSS_SELECTOR, '[data-test=error]')

    # ── Actions ───────────────────────────────────────
    def navigate(self):
        self.open(self.URL)

    def enter_username(self, username):
        self.type(self.USERNAME, username)

    def enter_password(self, password):
        self.type(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BTN)

    def login(self, username, password):
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertion helpers ─────────────────────────────
    def is_login_successful(self):
        return 'inventory' in self.get_current_url()

    def is_login_failed(self):
        return self.is_visible(self.ERROR_MSG)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)
