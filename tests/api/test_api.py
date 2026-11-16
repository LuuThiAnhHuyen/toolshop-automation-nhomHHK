"""Sprint 2 - Automated API tests using Playwright APIRequestContext."""
import json
from pathlib import Path

import pytest

from conftest import new_email, register_user, strong_password

KEYWORDS = json.loads(
    (Path(__file__).parents[2] / "data" / "search_keywords.json").read_text(encoding="utf-8")
)


@pytest.mark.smoke
@pytest.mark.api
def test_api_status_returns_toolshop(api):
    """Goal: Verify the API health check endpoint is alive.
    Precondition: API server is running and accessible via api fixture.
    Expected: Status code 200 and response JSON has app_name equal to 'Toolshop'."""
    response = api.get("/status")
    assert response.status == 200, response.text()
    assert response.json()["app_name"] == "Toolshop"


@pytest.mark.api
def test_api_products_pagination_and_contract(api):
    """Goal: Verify pagination keys and product item schema of GET /products.
    Precondition: At least one product exists in the system.
    Expected: Status code 200, required pagination keys exist, 0 < len(data) <= per_page, and valid id/name/price."""
    response = api.get("/products", params={"page": 1})
    assert response.status == 200, response.text()
    body = response.json()

    for key in ["current_page", "data", "per_page", "total", "last_page"]:
        assert key in body, f"Missing key {key}"

    assert 0 < len(body["data"]) <= body["per_page"]

    for product in body["data"]:
        assert isinstance(product["id"], (str, int))
        assert isinstance(product["name"], str) and product["name"].strip()
        assert isinstance(product["price"], (int, float)) and product["price"] > 0


@pytest.mark.api
@pytest.mark.parametrize("case", KEYWORDS, ids=[c["keyword"] for c in KEYWORDS])
def test_api_search_products_from_json(api, case):
    """Goal: Verify data-driven product search filters results by keyword from JSON.
    Precondition: data/search_keywords.json contains valid search terms.
    Expected: Status code 200, non-empty results, and every product name contains the target keyword."""
    response = api.get("/products/search", params={"q": case["keyword"]})
    assert response.status == 200, response.text()
    names = [p["name"] for p in response.json()["data"]]
    assert len(names) > 0, "Search result list is empty"
    assert all(case["must_contain"] in n.lower() for n in names), names


@pytest.mark.api
@pytest.mark.parametrize("path, expected", [("/users/me", 401), ("/products/does-not-exist", 404)])
def test_api_protected_or_missing_returns_4xx(api, path, expected):
    """Goal: Verify unauthorized or non-existent endpoints return proper 4xx client errors.
    Precondition: Request is sent without an authentication token or to an invalid product ID.
    Expected: Status code matches the expected 401 or 404 error code."""
    response = api.get(path)
    assert response.status == expected, response.text()


@pytest.mark.api
def test_api_register_empty_body_returns_422(api):
    """Goal: Verify server-side validation rejects empty registration payloads.
    Precondition: None.
    Expected: Status code 422 and error response contains 'email' and 'password' keys."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    body = response.json()
    assert "email" in body and "password" in body, body


@pytest.mark.api
def test_api_users_me_with_token_returns_profile(api, auth_headers, test_user):
    """Goal: Verify Bearer token grants access to the authenticated user's profile.
    Precondition: A fresh user is registered and logged in via session fixtures.
    Expected: Status code 200 and returned email matches test_user['email']."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"]


@pytest.mark.api
def test_api_register_does_not_expose_password(api):
    """Goal: Verify user registration succeeds without leaking sensitive password data.
    Precondition: Unique email and strong password are generated dynamically.
    Expected: Status code 201 and 'password' key is absent from the response JSON."""
    response = register_user(api, new_email(), strong_password())
    assert response.status == 201, response.text()
    assert "password" not in response.json()