# tests/test_login_allure.py
"""Login test dengan anotasi Allure Framework - BAB 5"""
import allure
import pytest
from pages.login_page import LoginPage


@allure.feature('Authentication')
@allure.story('Login')
class TestLoginWithAllure:

    @allure.title('Login dengan kredensial valid')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        'Verifikasi bahwa user dapat login dengan email dan password yang benar'
    )
    def test_login_valid(self, driver):
        with allure.step('Buka halaman login'):
            page = LoginPage(driver)
            page.navigate()

        with allure.step('Masukkan kredensial valid'):
            page.enter_username('tomsmith')
            page.enter_password('SuperSecretPassword!')

        with allure.step('Klik tombol Login'):
            page.click_login()

        with allure.step('Verifikasi login berhasil'):
            assert page.is_login_successful(), 'Login valid harus berhasil'
            allure.attach(
                driver.get_screenshot_as_png(),
                name='login_success',
                attachment_type=allure.attachment_type.PNG
            )

    @allure.title('Login dengan password salah')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_password(self, driver):
        with allure.step('Buka halaman login'):
            page = LoginPage(driver)
            page.navigate()

        with allure.step('Masukkan password yang salah'):
            page.enter_username('tomsmith')
            page.enter_password('wrongpassword')

        with allure.step('Klik tombol Login'):
            page.click_login()

        with allure.step('Verifikasi muncul pesan error'):
            assert page.is_login_failed(), 'Login dengan password salah harus gagal'
            allure.attach(
                driver.get_screenshot_as_png(),
                name='login_failed',
                attachment_type=allure.attachment_type.PNG
            )
