# tests/test_saucedemo_login.py
"""TC-EC-001, TC-EC-002, TC-EC-003 - Login SauceDemo"""
import allure
import pytest
from pages.login_page import SauceDemoLoginPage

SAUCE_LOGIN_DATA = [
    ('standard_user',   'secret_sauce', True,  'TC-EC-001', 'Login user valid'),
    ('locked_out_user', 'secret_sauce', False, 'TC-EC-002', 'User yang dikunci sistem'),
    ('wrong_user',      'secret_sauce', False, 'TC-EC-003', 'Username tidak ada'),
]


@allure.feature('Authentication')
@allure.story('SauceDemo Login')
class TestSauceDemoLogin:

    @pytest.mark.parametrize(
        'username, password, expected_success, tc_id, description',
        SAUCE_LOGIN_DATA,
        ids=[d[3] for d in SAUCE_LOGIN_DATA]
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login(self, driver, username, password, expected_success, tc_id, description):
        allure.dynamic.title(f'{tc_id}: {description}')

        page = SauceDemoLoginPage(driver)
        page.login(username, password)

        if expected_success:
            assert page.is_login_successful(), \
                f'[{tc_id}] Login seharusnya BERHASIL untuk user: {username}'
        else:
            # TC-EC-003: Sengaja assert login berhasil untuk wrong_user
            # supaya test ini FAILED di Allure (expected behavior untuk demo report)
            if tc_id == 'TC-EC-003':
                assert page.is_login_successful(), \
                    f'[{tc_id}] wrong_user tidak bisa login ke sistem'
            else:
                assert page.is_login_failed(), \
                    f'[{tc_id}] Login seharusnya GAGAL untuk user: {username}'
