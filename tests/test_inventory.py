# tests/test_inventory.py
"""TC-EC-004, TC-EC-005 - Inventory/Produk SauceDemo"""
import allure
import pytest
from pages.login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage


@allure.feature('Product Catalog')
class TestInventory:

    @pytest.fixture(autouse=True)
    def login_first(self, driver):
        """Login otomatis sebelum setiap test di class ini"""
        SauceDemoLoginPage(driver).login('standard_user', 'secret_sauce')
        self.inv = InventoryPage(driver)

    @allure.title('TC-EC-004: Verifikasi jumlah produk yang tampil = 6')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_count(self, driver):
        count = self.inv.get_product_count()
        assert count == 6, f'Jumlah produk harus 6, tapi tampil: {count}'

    @allure.title('TC-EC-005: Sort produk harga terendah ke tertinggi')
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_price_low_to_high(self, driver):
        self.inv.sort_by('lohi')
        prices = self.inv.get_product_prices()
        assert prices == sorted(prices), \
            f'Produk belum terurut dari harga terendah: {prices}'
