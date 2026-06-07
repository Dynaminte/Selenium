# pages/checkout_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout page untuk saucedemo.com"""

    # ── Locators ──────────────────────────────────────
    FIRST_NAME   = (By.ID, 'first-name')
    LAST_NAME    = (By.ID, 'last-name')
    POSTAL_CODE  = (By.ID, 'postal-code')
    CONTINUE_BTN = (By.ID, 'continue')
    FINISH_BTN   = (By.ID, 'finish')
    SUCCESS_MSG  = (By.CLASS_NAME, 'complete-header')
    ERROR_MSG    = (By.CSS_SELECTOR, '[data-test=error]')
    TOTAL_LABEL  = (By.CLASS_NAME, 'summary_total_label')
    ITEM_TOTAL   = (By.CLASS_NAME, 'summary_subtotal_label')

    # ── Actions ───────────────────────────────────────
    def fill_info(self, first_name, last_name, postal):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal)

    def continue_checkout(self):
        self.click(self.CONTINUE_BTN)

    def finish_checkout(self):
        self.click(self.FINISH_BTN)

    # ── Assertion helpers ─────────────────────────────
    def is_order_confirmed(self):
        return self.is_visible(self.SUCCESS_MSG)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)

    def get_total_price(self):
        """Ambil teks total harga di halaman konfirmasi"""
        return self.get_text(self.TOTAL_LABEL)

    def get_item_total(self):
        return self.get_text(self.ITEM_TOTAL)
