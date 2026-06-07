# tests/test_checkout.py
"""TC-EC-008, TC-EC-009, TC-EC-010 - Checkout SauceDemo"""
import allure
import pytest
from pages.login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage


@allure.feature('Checkout')
class TestCheckout:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login dan tambah 1 produk sebelum tiap test checkout"""
        SauceDemoLoginPage(driver).login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_first_product_to_cart()
        inv.go_to_cart()
        # Klik Checkout dari halaman cart
        from selenium.webdriver.common.by import By
        driver.find_element(By.ID, 'checkout').click()
        self.checkout = CheckoutPage(driver)

    @allure.title('TC-EC-008: Checkout dengan data lengkap → sukses')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_success(self, driver):
        self.checkout.fill_info('Budi', 'Santoso', '40123')
        self.checkout.continue_checkout()
        self.checkout.finish_checkout()

        assert self.checkout.is_order_confirmed(), \
            'Order harus terkonfirmasi setelah checkout berhasil'
        allure.attach(
            driver.get_screenshot_as_png(),
            name='checkout_success',
            attachment_type=allure.attachment_type.PNG
        )

    @allure.title('TC-EC-009: Checkout tanpa nama depan → error')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_missing_firstname(self, driver):
        self.checkout.fill_info('', 'Santoso', '40123')
        self.checkout.continue_checkout()

        error = self.checkout.get_error_message()
        assert 'First Name is required' in error, \
            f'Pesan error tidak sesuai: {error}'

    @allure.title('TC-EC-010: Verifikasi total harga di halaman konfirmasi')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_total_price_displayed(self, driver):
        self.checkout.fill_info('Budi', 'Santoso', '40123')
        self.checkout.continue_checkout()

        # Sengaja akses elemen yang tidak ada → akan raise exception → BROKEN di Allure
        from selenium.webdriver.common.by import By
        driver.find_element(By.ID, 'non_existent_total_element').text

