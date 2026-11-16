"""Sprint 2 UI Tests - Gio hang, Thanh toan, Tai khoan ca nhan, Lien he (Contact).
Owner: Khôi
"""
import pytest
from playwright.sync_api import expect

from conftest import new_email
from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage

PRODUCT_NAME = "Claw Hammer"


@pytest.mark.ui
def test_cart_add_product_updates_badge(page):
    """Goal: Verify adding a product updates the cart badge.
    Precondition: Claw Hammer is available in the product catalogue.
    Expected: Adding two items changes the cart badge to 2."""
    product = HomePage(page).open().open_product(PRODUCT_NAME)

    product.add_to_cart(quantity=2)

    expect(product.cart_quantity).to_have_text("2")


@pytest.mark.ui
def test_cart_remove_product_removes_cart_line(page):
    """Goal: Verify a product can be removed from the shopping cart.
    Precondition: Claw Hammer has been added to this browser context's cart.
    Expected: The Claw Hammer line no longer appears after removal."""
    product = HomePage(page).open().open_product(PRODUCT_NAME)
    product.add_to_cart()
    cart = product.go_to_cart()
    expect(cart.product_title(PRODUCT_NAME)).to_have_count(1)

    cart.remove_product(PRODUCT_NAME)

    expect(cart.product_title(PRODUCT_NAME)).to_have_count(0)


@pytest.mark.ui
def test_account_logged_in_user_sees_account_navigation(logged_in_page):
    """Goal: Verify an authenticated user can open the account overview.
    Precondition: logged_in_page has loaded the reusable storage_state session.
    Expected: The account title and Profile navigation are visible."""
    account = AccountPage(logged_in_page).open()

    expect(account.title).to_have_text("My account")
    expect(account.nav_profile).to_be_visible()


@pytest.mark.ui
def test_contact_valid_form_shows_confirmation(page):
    """Goal: Verify a visitor can submit a valid contact message.
    Precondition: A unique test email and a message of at least 50 characters are available.
    Expected: The contact form displays its success confirmation."""
    contact = ContactPage(page).open()
    contact.fill_form(
        "Khoi",
        "QA",
        new_email(),
        "customer-service",
        "Automated test message for Sprint 2; it contains enough characters to be valid.",
    ).submit()

    expect(contact.success).to_be_visible()
