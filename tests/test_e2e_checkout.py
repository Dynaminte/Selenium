# tests/test_e2e_checkout.py
"""
TC-EC-011 dan TC-EC-012 — End-to-End Test SauceDemo
Alur: Login → Browse → Add to Cart → Checkout → Logout
"""
import allure
import pytest
from selenium.webdriver.common.by import By
from pages.login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage


@allure.feature('E-Commerce Flow')
@allure.story('End-to-End Purchase')
class TestE2ECheckout:

    @allure.title('TC-EC-011: User dapat logout setelah login berhasil')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, driver):
        with allure.step('Login sebagai standard_user'):
            SauceDemoLoginPage(driver).login('standard_user', 'secret_sauce')
            assert 'inventory' in driver.current_url, 'Harus berhasil login'

        with allure.step('Buka menu burger dan klik Logout'):
            driver.find_element(By.ID, 'react-burger-menu-btn').click()
            import time; time.sleep(0.5)
            driver.find_element(By.ID, 'logout_sidebar_link').click()

        with allure.step('Verifikasi kembali ke halaman login'):
            assert driver.current_url == 'https://www.saucedemo.com/', \
                f'Harus kembali ke halaman login, URL: {driver.current_url}'

    @allure.title('TC-EC-012: Alur Penuh Login → Add Cart → Checkout → Verifikasi')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_purchase_flow(self, driver):

        # STEP 1: Login
        with allure.step('1. Login sebagai standard_user'):
            login = SauceDemoLoginPage(driver)
            login.login('standard_user', 'secret_sauce')
            assert login.is_login_successful(), 'Login harus berhasil'

        # STEP 2: Add to Cart
        with allure.step('2. Tambahkan produk pertama ke cart'):
            inv = InventoryPage(driver)
            inv.add_first_product_to_cart()
            assert inv.get_cart_count() == 1, 'Badge cart harus = 1'
            allure.attach(
                driver.get_screenshot_as_png(),
                name='after_add_to_cart',
                attachment_type=allure.attachment_type.PNG
            )

        # STEP 3: Go to Cart & Checkout
        with allure.step('3. Buka cart dan mulai checkout'):
            inv.go_to_cart()
            driver.find_element(By.ID, 'checkout').click()

        # STEP 4: Isi data checkout
        with allure.step('4. Isi data pengiriman'):
            checkout = CheckoutPage(driver)
            checkout.fill_info('Budi', 'Santoso', '40123')
            checkout.continue_checkout()

        # STEP 5: Finish
        with allure.step('5. Selesaikan order'):
            checkout.finish_checkout()

        # STEP 6: Verifikasi
        with allure.step('6. Verifikasi order berhasil'):
            assert checkout.is_order_confirmed(), \
                'Order harus terkonfirmasi dengan pesan Thank you!'
            allure.attach(
                driver.get_screenshot_as_png(),
                name='order_confirmed',
                attachment_type=allure.attachment_type.PNG
            )


