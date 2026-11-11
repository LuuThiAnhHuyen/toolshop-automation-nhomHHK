
"""Sprint 1 - Smoke Tests for Toolshop.

Test 1: Product search - Huyen
Test 2: Add product to cart - Khoi
Test 3: Invalid login - Hanh (to be added)
Test 4: Empty contact form - Huyen
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
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
