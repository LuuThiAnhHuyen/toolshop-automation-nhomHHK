
"""Sprint 1 - Smoke Tests for Toolshop.

Test 1: Product search - Huyen
Test 2: Add product to cart - Khoi
Test 3: Invalid login - Hanh (to be added)
Test 4: Empty contact form - Huyen
"""
import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage


# =====================================================
# TEST 1 - HUYEN: TIM KIEM SAN PHAM
# =====================================================
@pytest.mark.smoke
@pytest.mark.ui
def test_search_product(page):
    """Goal: verify product search.
    Precondition: Toolshop is available.
    Expected: all displayed products contain the search keyword."""

    home = HomePage(page).open().search("pliers")

    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")

    names = home.product_names.all_inner_texts()

    assert names, "Khong tim thay san pham"
    assert all("pliers" in name.lower() for name in names)


# =====================================================
# TEST 2 - KHOI: THEM SAN PHAM VAO GIO HANG
# =====================================================
@pytest.mark.smoke
@pytest.mark.ui
def test_add_product_to_cart(page):
    """Goal: verify adding products to the shopping cart.
    Precondition: Claw Hammer is available.
    Expected: the cart badge displays quantity 3."""

    product = HomePage(page).open().open_product("Claw Hammer")

    product.add_to_cart(quantity=3)

    expect(product.cart_quantity).to_have_text("3")


# =====================================================
# TEST 3 - HANH: DANG NHAP SAI
# Hanh se bo sung bai test tai day.
# =====================================================
@pytest.mark.smoke
@pytest.mark.ui
def test_b3_login_wrong_password_shows_error(page):
    """
    Goal: Ensure logging in with non-existent credentials displays an error message and stays on login page.
    Precondition: Use a random non-existent email (avoiding shared class account lockout).
    Expected: Error message displays 'Invalid email or password' and the URL ends with /auth/login.
    """
    login_page = LoginPage(page).open()
    login_page.login("nonexistent_user_hanh_99999@test.com", "WrongPassword123!")

    expect(login_page.error).to_have_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))

# =====================================================
# TEST 4 - HUYEN: FORM LIEN HE TRONG
# =====================================================
@pytest.mark.smoke
@pytest.mark.ui
def test_contact_empty_form(page):
    """Goal: validate an empty contact form.
    Precondition: all contact fields are empty.
    Expected: subject and message required errors appear."""

    contact = ContactPage(page).open()

    contact.submit()

    expect(contact.errors).to_contain_text([
        "Subject is required",
        "Message is required"
    ])
