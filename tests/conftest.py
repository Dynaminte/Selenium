# tests/conftest.py
import pytest
import csv
import os
from selenium import webdriver

# ── Driver fixture ────────────────────────────────────────────────────────────
@pytest.fixture(scope='function')
def driver():
    """Fixture: buat driver baru setiap test, tutup otomatis setelah selesai"""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    # Aktifkan headless saat berjalan di CI/CD (GitHub Actions)
    if os.getenv('CI'):
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

    d = webdriver.Chrome(options=options)
    yield d          # <-- test berjalan di sini
    d.quit()         # <-- teardown otomatis setelah test selesai


# ── Page fixtures ─────────────────────────────────────────────────────────────
@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture(scope='function')
def saucedemo_login_page(driver):
    from pages.login_page import SauceDemoLoginPage
    return SauceDemoLoginPage(driver)


# ── Helper: baca CSV ──────────────────────────────────────────────────────────
def load_csv(filename):
    """Baca file CSV dari folder data/ dan kembalikan sebagai list of dict"""
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


# ── Screenshot otomatis saat test FAIL ────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)

            # Coba ambil TC ID dari parameter test (row['tc_id'])
            tc_id = None
            if hasattr(item, 'callspec') and 'row' in item.callspec.params:
                row = item.callspec.params['row']
                if isinstance(row, dict):
                    tc_id = row.get('tc_id')

            if tc_id:
                # Nama file: tests_test_register_ddt_TC-REG-002.png
                base_name = item.nodeid.split('::')[0].replace('/', '_').replace('\\', '_')
                name = f'{base_name}_{tc_id}'
            else:
                # Fallback: nama dari nodeid
                name = item.nodeid.replace('/', '_').replace('::', '_').replace('\\', '_')

            screenshot_path = f'reports/screenshots/{name}.png'
            driver.save_screenshot(screenshot_path)
            print(f'\n📸 Screenshot disimpan: {screenshot_path}')
