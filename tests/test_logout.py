# tests/test_logout.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogout:
    """Test cases untuk fitur Logout - Latihan 3.1"""

    def test_login_then_logout(self, driver):
        """TC: Setelah login berhasil, user dapat logout dan kembali ke login page"""
        # Step 1: Login
        login = LoginPage(driver)
        login.login('tomsmith', 'SuperSecretPassword!')

        # Step 2: Verifikasi sudah di dashboard
        dashboard = DashboardPage(driver)
        assert dashboard.is_on_dashboard(), 'Seharusnya berhasil masuk dashboard'

        # Step 3: Logout
        dashboard.logout()

        # Step 4: Verifikasi kembali ke halaman login
        current_url = driver.current_url
        assert 'login' in current_url, \
            f'Harus kembali ke login page, tapi URL sekarang: {current_url}'

    def test_dashboard_header_text(self, driver):
        """TC: Header halaman dashboard harus berisi teks yang sesuai"""
        login = LoginPage(driver)
        login.login('tomsmith', 'SuperSecretPassword!')

        dashboard = DashboardPage(driver)
        header = dashboard.get_header_text()
        assert 'Secure Area' in header, \
            f'Header dashboard tidak sesuai: {header}'
