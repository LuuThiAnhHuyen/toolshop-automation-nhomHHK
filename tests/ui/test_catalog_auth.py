"""Sprint 2 UI Tests - Trang chu, Tim kiem/Loc, Chi tiet san pham, Dang nhap/Dang ky.
Owner: Luu Thi Anh Huyen
"""
import pytest
from playwright.sync_api import expect

from conftest import new_email, strong_password
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

# Huyền viết các test UI tại đây (nhớ gắn @pytest.mark.ui và docstring 3 ý)