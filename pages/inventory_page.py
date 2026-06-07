# pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Inventory/produk page untuk saucedemo.com"""
    URL = 'https://www.saucedemo.com/inventory.html'

    # ── Locators ──────────────────────────────────────
    SORT_DROPDOWN    = (By.CLASS_NAME, 'product_sort_container')
    PRODUCT_NAMES    = (By.CLASS_NAME, 'inventory_item_name')
    PRODUCT_PRICES   = (By.CLASS_NAME, 'inventory_item_price')
    ADD_TO_CART_BTNS = (By.CSS_SELECTOR, '[data-test^=add-to-cart]')
    CART_BADGE       = (By.CLASS_NAME, 'shopping_cart_badge')
    CART_ICON        = (By.CLASS_NAME, 'shopping_cart_link')
    REMOVE_BTNS      = (By.CSS_SELECTOR, '[data-test^=remove]')

    # ── Actions ───────────────────────────────────────
    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_NAMES))

    def get_product_names(self):
        return [el.text for el in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def get_product_prices(self):
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(el.text.replace('$', '')) for el in prices]

    def sort_by(self, option):
        """
        option values:
          'az'   = Name (A to Z)
          'za'   = Name (Z to A)
          'lohi' = Price (low to high)
          'hilo' = Price (high to low)
        """
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option)

    def add_first_product_to_cart(self):
        self.find_clickable(self.ADD_TO_CART_BTNS).click()

    def add_product_to_cart(self, index=0):
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        btns[index].click()

    def remove_product_from_cart(self, index=0):
        btns = self.driver.find_elements(*self.REMOVE_BTNS)
        btns[index].click()

    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except Exception:
            return 0

    def go_to_cart(self):
        self.click(self.CART_ICON)
