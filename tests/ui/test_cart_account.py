"""Sprint 2 UI Tests - Gio hang, Thanh toan, Tai khoan ca nhan, Lien he (Contact).
Owner: Khôi
"""
import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.product_page import ProductPage

# Khôi viết các test UI được giao tại đây (dùng logged_in_page cho Account, gắn @pytest.mark.ui và docstring 3 ý)