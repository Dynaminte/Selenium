# tests/test_cart.py
"""TC-EC-006, TC-EC-007 - Cart/Keranjang SauceDemo"""
import allure
import pytest
from pages.login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage


@allure.feature('Shopping Cart')
class TestCart:

    @pytest.fixture(autouse=True)
    def login_first(self, driver):
        SauceDemoLoginPage(driver).login('standard_user', 'secret_sauce')
        self.inv = InventoryPage(driver)

    @allure.title('TC-EC-006: Tambah 1 produk ke cart, badge = 1')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_product(self, driver):
        self.inv.add_first_product_to_cart()
        count = self.inv.get_cart_count()
        assert count == 1, f'Badge cart harus 1, tapi: {count}'

    @allure.title('TC-EC-007: Tambah 3 produk, hapus 1, badge = 2')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_three_remove_one(self, driver):
        # Tambah 3 produk
        for i in range(3):
            self.inv.add_product_to_cart(index=i)

        assert self.inv.get_cart_count() == 3, 'Setelah add 3, badge harus 3'

        # Hapus 1 produk
        self.inv.remove_product_from_cart(index=0)

        count = self.inv.get_cart_count()
        # Sengaja expect 3 agar test FAILED di Allure (demo 75% pass rate)
        assert count == 3, f'Setelah hapus 1, badge harus 3, tapi: {count}'
