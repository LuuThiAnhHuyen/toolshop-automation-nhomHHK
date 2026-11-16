"""Sprint 2 - Network interception, response mocking, and storage_state UI tests."""
import json
import re

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.home_page import HomePage

PRODUCT_LIST = re.compile(r"/products(\?.*)?$")
EMPTY_PAGE = {"current_page": 1, "data": [], "from": None, "last_page": 1, "per_page": 9, "to": None, "total": 0}


@pytest.mark.ui
def test_ui_home_without_images_still_lists_products(page):
    """Goal: Verify the home page remains functional when image assets are blocked.
    Precondition: Image requests matching common extensions are aborted via page.route().
    Expected: At least one image request is blocked and the first product name is visible."""
    blocked = []

    def block(route):
        blocked.append(route.request.url)
        route.abort()

    page.route(re.compile(r"\.(png|jpeg|webp|avif|svg)(\?.*)?$"), block)
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    assert len(blocked) > 0


@pytest.mark.ui
def test_ui_home_with_empty_product_list_shows_no_results(page):
    """Goal: Verify UI displays an empty-state message when the product API returns no items.
    Precondition: GET /products is mocked via page.route() to return an empty data list.
    Expected: 'There are no products found.' text is displayed and 0 product cards render."""
    page.route(
        PRODUCT_LIST,
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(EMPTY_PAGE),
        ),
    )
    home = HomePage(page).open()
    expect(home.no_results).to_contain_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


@pytest.mark.ui
def test_ui_home_when_product_api_fails_stays_usable(page):
    """Goal: Verify the UI degrades gracefully without crashing when the product API fails.
    Precondition: GET /products is mocked via page.route() to return HTTP 500.
    Expected: Search input remains editable and 0 product items are displayed."""
    page.route(PRODUCT_LIST, lambda route: route.fulfill(status=500, body="{}"))
    home = HomePage(page).open()
    expect(home.search_box).to_be_editable()
    expect(home.product_names).to_have_count(0)


@pytest.mark.ui
def test_ui_logged_in_page_shows_user_menu(logged_in_page):
    """Goal: Verify reusable authentication via storage_state skips the login form.
    Precondition: Session storage_state is generated once by auth_state fixture.
    Expected: Opening /account directly displays 'My account' title and 'QA Bot' in nav menu."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")