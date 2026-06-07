# tests/test_login.py
import pytest
from pages.login_page import LoginPage


class TestLogin:
    """Test cases untuk fitur Login - https://www.saucedemo.com """

    def test_login_valid(self, login_page):
        """TC: Login dengan kredensial yang benar harus berhasil"""
        login_page.login('tomsmith', 'SuperSecretPassword!')
        assert login_page.is_login_successful(), 'Login valid harus berhasil'

    def test_login_invalid_password(self, login_page):
        """TC: Login dengan password salah harus gagal"""
        login_page.login('tomsmith', 'wrongpassword')
        assert login_page.is_login_failed(), 'Login dengan password salah harus gagal'

    def test_login_empty_username(self, login_page):
        """TC: Login tanpa username harus gagal"""
        login_page.login('', 'SuperSecretPassword!')
        assert login_page.is_login_failed(), 'Login tanpa username harus gagal'

    def test_flash_message_content(self, login_page):
        """TC: Pesan error harus mengandung kata 'invalid'"""
        login_page.login('wronguser', 'wrongpass')
        msg = login_page.get_flash_message()
        assert 'invalid' in msg.lower(), f'Pesan error tidak sesuai: {msg}'
