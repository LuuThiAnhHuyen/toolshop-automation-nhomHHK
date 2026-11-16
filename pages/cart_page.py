
import re

from pages.base_page import BasePage


def money(text: str) -> float:
    return float(text.replace("$", "").replace(",", "").strip())


class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)

        self.product_titles = page.get_by_test_id("product-title")
        self.quantities = page.get_by_test_id("product-quantity")
        self.line_prices = page.get_by_test_id("line-price")
        self.total = page.get_by_test_id("cart-total")
        self.continue_shopping = page.get_by_role(
            "button", name="Continue Shopping"
        )

    def line_totals(self) -> list[float]:
        return [
            money(text)
            for text in self.line_prices.all_inner_texts()
        ]

    def product_title(self, name: str):
        return self.product_titles.filter(
            has_text=re.compile(rf"^\s*{re.escape(name)}\s*$")
        )

    def remove_product(self, name: str):
        """Remove the named product from the cart table."""
        row = self.product_title(name).first.locator("xpath=ancestor::tr")
        row.locator("a.btn-danger").click()
        return self

    def total_value(self) -> float:
        return money(self.total.inner_text())

    def continue_shopping_to_home(self):
        from pages.home_page import HomePage

        self.continue_shopping.click()
        return HomePage(self.page)
