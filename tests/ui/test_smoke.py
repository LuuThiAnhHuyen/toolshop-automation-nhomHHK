
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


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
