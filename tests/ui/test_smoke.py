import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.ui
def test_search_product(page):
    """Goal: test product search.
    Precondition: Toolshop is available.
    Expected: search results match the keyword."""

    home = HomePage(page).open().search("pliers")

    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")

    names = home.product_names.all_inner_texts()

    assert names, "Khong tim thay san pham"
    assert all("pliers" in name.lower() for name in names)


@pytest.mark.smoke
@pytest.mark.ui
def test_add_product_to_cart(page):
    """Goal: add a product to the shopping cart.
    Precondition: Toolshop is available and Claw Hammer is in the catalogue.
    Expected: the cart badge shows the selected quantity."""

    product = HomePage(page).open().open_product("Claw Hammer")

    product.add_to_cart(quantity=3)

    expect(product.cart_quantity).to_have_text("3")
@pytest.mark.smoke
def test_b3_login_wrong_password_shows_error(page):
    """
    Mục tiêu: Đảm bảo đăng nhập bằng thông tin không tồn tại sẽ bị từ chối và hiển thị thông báo lỗi.
    Tiền điều kiện: Dùng email ngẫu nhiên không tồn tại (tránh làm khóa tài khoản chung của lớp).
    Kết quả mong đợi: Hiển thị thông báo 'Invalid email or password' và URL kết thúc bằng /auth/login.
    """
    login_page = LoginPage(page).open()
    login_page.login("nonexistent_user_hanh_99999@test.com", "WrongPassword123!")

    # Sửa lại đúng thuộc tính error của LoginPage
    expect(login_page.error).to_have_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))