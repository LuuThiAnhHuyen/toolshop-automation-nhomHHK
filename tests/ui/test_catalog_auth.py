
"""Sprint 2 - UI Testing: Catalog and Authentication.
Owner: Huyen
"""

import pytest
from playwright.sync_api import expect

from conftest import new_email
from pages.home_page import HomePage
from pages.login_page import LoginPage


# TEST 1 - TIM KIEM SAN PHAM
@pytest.mark.ui
def test_sprint2_search_valid_keyword(page):
    """Goal: Verify searching for a valid product.
    Precondition: Toolshop is available.
    Expected: Search results contain the keyword.
    """
    home = HomePage(page).open()
    home.search("pliers")

    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")

    names = home.product_names.all_inner_texts()

    assert len(names) > 0
    assert all("pliers" in name.lower() for name in names)


# TEST 2 - SAP XEP SAN PHAM (PARAMETRIZE)
@pytest.mark.ui
@pytest.mark.parametrize(
    "sort_value, reverse",
    [
        ("price,asc", False),
        ("price,desc", True),
    ],
)
def test_sprint2_sort_products_by_price(page, sort_value, reverse):
    """Goal: Verify product price sorting.
    Precondition: Products are available on the homepage.
    Expected: Prices follow the selected sorting direction.
    """
    home = HomePage(page).open()
    home.sort_by(sort_value)

    expect(home.sorting_completed).to_be_visible()

    prices = home.prices()

    assert len(prices) > 0
    assert prices == sorted(prices, reverse=reverse)


# TEST 3 - CHI TIET SAN PHAM
@pytest.mark.ui
def test_sprint2_product_details(page):
    """Goal: Verify product details.
    Precondition: At least one product is available.
    Expected: Product name and price are displayed correctly.
    """
    home = HomePage(page).open()

    expect(home.product_names.first).to_be_visible()
    product_name = home.product_names.first.inner_text().strip()

    product = home.open_product(product_name)

    expect(product.name).to_have_text(product_name)
    expect(product.unit_price).to_be_visible()

    assert product.price() > 0


# TEST 4 - THEM SAN PHAM VAO GIO HANG
@pytest.mark.ui
def test_sprint2_add_product_to_cart(page):
    """Goal: Verify adding a product to the cart.
    Precondition: A product is available.
    Expected: Cart quantity increases to one.
    """
    home = HomePage(page).open()

    expect(home.product_names.first).to_be_visible()
    product_name = home.product_names.first.inner_text().strip()

    product = home.open_product(product_name)

    expect(product.add_to_cart_button).to_be_enabled()

    product.add_to_cart()

    expect(product.cart_quantity).to_have_text("1")


# TEST 5 - DANG NHAP SAI
@pytest.mark.ui
def test_sprint2_invalid_login(page):
    """Goal: Verify login error handling.
    Precondition: An unregistered email is used.
    Expected: The application displays a login error.
    """
    login = LoginPage(page).open()

    login.login(
        new_email(),
        "InvalidLogin123!"
    )

    expect(login.error).to_be_visible()


# TEST 6 - LOC SAN PHAM THEO DANH MUC
@pytest.mark.ui
@pytest.mark.parametrize(
    "category",
    ["Hand Tools", "Power Tools"]
)
def test_sprint2_filter_by_category(page, category):
    """Goal: Verify category filtering.
    Precondition: Toolshop homepage is available.
    Expected: Category is selected and products are displayed.
    """
    home = HomePage(page).open()

    home.filter_by_category(category)

    expect(
        home.category_is_selected(category)
    ).to_be_checked()

    expect(home.product_names.first).to_be_visible()

    assert home.product_names.count() > 0
