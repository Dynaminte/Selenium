# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page untuk the-internet.herokuapp.com/secure"""

    # ── Locators ──────────────────────────────────────
    LOGOUT_BTN        = (By.CSS_SELECTOR, '.button.secondary.radius')
    FLASH_SUCCESS     = (By.CSS_SELECTOR, '.flash.success')
    SECURE_AREA_HEADER = (By.TAG_NAME, 'h2')

    # ── Actions ───────────────────────────────────────
    def logout(self):
        """Klik tombol logout"""
        self.click(self.LOGOUT_BTN)

    def is_on_dashboard(self):
        """Cek apakah kita sedang di halaman dashboard/secure area"""
        return self.is_visible(self.FLASH_SUCCESS)

    def get_header_text(self):
        """Ambil teks header halaman"""
        return self.get_text(self.SECURE_AREA_HEADER)
