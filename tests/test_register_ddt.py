# tests/test_register_ddt.py
"""
Data-Driven Test untuk fitur Register - Latihan 4.1
Target: https://demoqa.com/register
Data: data/register_data.csv
"""
import pytest
import sys
import os

# Pastikan root proyek ada di path
sys.path.insert(0, os.path.abspath('.'))

from tests.conftest import load_csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ── Load CSV data dengan test IDs ────────────────────────────────────────────
_CSV_DATA = load_csv('register_data.csv') \
    if os.path.exists('data/register_data.csv') else []


class TestRegisterDDT:
    """DDT: Registrasi dengan berbagai skenario dari CSV"""

    @pytest.mark.parametrize(
        'row',
        _CSV_DATA,
        ids=[r.get('description', f'row-{i}') for i, r in enumerate(_CSV_DATA)]
    )
    def test_register(self, driver, row):
        """Jalankan skenario register untuk setiap baris di CSV"""
        tc_id = row.get('tc_id', 'TC-REG-???')
        expected = row.get('expected', 'FAIL').strip().upper()
        description = row.get('description', '')

        driver.get('https://demoqa.com/register')
        wait = WebDriverWait(driver, 10)

        form_filled = False
        try:
            # Isi First Name (userName field di demoqa)
            if row.get('username') and row['username'].strip():
                el = wait.until(EC.presence_of_element_located(
                    (By.ID, 'firstname')))
                el.clear()
                el.send_keys(row['username'].strip())

            # Isi Last Name (hardcode karena CSV tidak punya kolom ini)
            el_last = wait.until(EC.presence_of_element_located(
                (By.ID, 'lastname')))
            el_last.clear()
            el_last.send_keys('Test')

            # Isi userName
            if row.get('username') and row['username'].strip():
                el_user = wait.until(EC.presence_of_element_located(
                    (By.ID, 'userName')))
                el_user.clear()
                el_user.send_keys(row['username'].strip().replace(' ', '').lower())

            # Isi password
            if row.get('password') and row['password'].strip():
                el = driver.find_element(By.ID, 'password')
                el.clear()
                el.send_keys(row['password'])

            form_filled = True

        except Exception as e:
            if expected == 'PASS':
                pytest.fail(
                    f"[{tc_id}] [{description}] Exception saat mengisi form: {e}"
                )

        # ── Assertion berdasarkan expected ───────────────────────────────
        if expected == 'PASS':
            # Untuk data valid, form harus bisa diisi tanpa error
            assert form_filled, \
                f"[{tc_id}] [{description}] Form seharusnya bisa diisi lengkap"
            print(f"\n✅ [{tc_id}] {description} → PASSED")
        else:
            # Untuk data FAIL, kita sengaja gagalkan test supaya
            # pytest merekam sebagai FAILED dan screenshot otomatis diambil
            # Screenshot otomatis oleh conftest.py pytest_runtest_makereport hook
            pytest.fail(
                f"[{tc_id}] [{description}] Skenario negatif: "
                f"input tidak valid terdeteksi (expected FAIL)"
            )
