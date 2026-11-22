Feature: Shopping cart total calculation
  As a customer on Toolshop
  I want to search for a product, add it to the cart with a quantity, and check the cart total
  So that I can verify the price calculation before checkout

  Scenario Outline: Search product, add to cart, and verify cart total
    Given the user is on the Toolshop home page
    When the user searches for "<keyword>"
    And the user opens the product "<product_name>"
    And the user adds <quantity> items to the cart
    And the user opens the shopping cart
    Then the cart shows "<product_name>" with accurate total for <quantity> items

    Examples:
      | keyword | product_name | quantity |
      | hammer  | Claw Hammer  | 2        |
      | bolt    | Bolt Cutters | 3        |