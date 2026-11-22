import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenario, then, when

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


@pytest.fixture
def bdd_context():
    """Shared context storing product unit price across BDD steps."""
    return {}


@pytest.mark.bdd
@pytest.mark.ui
@scenario("cart.feature", "Search product, add to cart, and verify cart total")
def test_search_add_to_cart_and_verify_total():
    """Goal: Verify end-to-end cart total calculation using BDD Scenario Outline.
    Precondition: Toolshop catalog has matching products with unit prices.
    Expected: Cart total equals unit price multiplied by selected quantity."""


@given("the user is on the Toolshop home page")
def user_on_home_page(page):
    HomePage(page).open()


@when(parsers.parse('the user searches for "{keyword}"'))
def user_searches_product(page, keyword):
    home = HomePage(page)
    home.search(keyword)
    expect(home.search_completed).to_be_visible()


@when(parsers.parse('the user opens the product "{product_name}"'))
def user_opens_product(page, product_name):
    HomePage(page).open_product(product_name)


@when(parsers.parse("the user adds {quantity:d} items to the cart"))
def user_adds_items_to_cart(page, quantity, bdd_context):
    product = ProductPage(page)
    expect(product.unit_price).to_be_visible()
    bdd_context["unit_price"] = product.price()
    product.add_to_cart(quantity=quantity)
    expect(product.cart_quantity).to_have_text(str(quantity))


@when("the user opens the shopping cart")
def user_opens_cart(page):
    CartPage(page).open()


@then(
    parsers.parse(
        'the cart shows "{product_name}" with accurate total for {quantity:d} items'
    )
)
def verify_cart_product_and_total(page, product_name, quantity, bdd_context):
    cart = CartPage(page)
    expect(cart.product_title(product_name)).to_be_visible()
    expect(cart.total).to_be_visible()

    expected_total = round(bdd_context["unit_price"] * quantity, 2)
    actual_total = round(cart.total_value(), 2)
    assert actual_total == expected_total, (
        f"Expected total {expected_total}, got {actual_total}"
    )