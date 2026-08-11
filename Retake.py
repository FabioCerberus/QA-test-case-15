#1. Launch browser
#2. Navigate to url 'http://automationexercise.com'
#3. Verify that home page is visible successfully
#4. Click 'Products' button
#5. Hover over first product and click 'Add to cart'
#6. Click 'Continue Shopping' button
#7. Hover over second product and click 'Add to cart'
#8. Click 'View Cart' button
#9. Verify both products are added to Cart
#10. Verify their prices, quantity and total price

from playwright.sync_api import sync_playwright, expect

def test_add_products_in_cart():
    with (sync_playwright() as p):
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://automationexercise.com")
        expect(page).to_have_title("Automation Exercise")

        page.get_by_role("link", name="Products").click()
        expect(page.get_by_text("All Products")).to_be_visible()

        # Choose which product to test
        product_index = 0

        # Save product card based on the chosen index
        product = page.locator(".single-products").nth(product_index)

        # Capture product information before adding it to the cart
        product_name = product.locator(".productinfo p").inner_text()
        product_price = product.locator(".productinfo h2").inner_text()

        print(f"Product selected: {product_name} | Price: {product_price}")

        # Capture product ID to find the same product later in the cart
        product_id = product.locator(".productinfo a.add-to-cart").get_attribute("data-product-id")

        # Hover over selected product and click 'Add to cart'
        product.scroll_into_view_if_needed()
        product.hover()
        product.locator(".product-overlay a.add-to-cart").click()

        # Click 'View Cart' button
        expect(page.locator("#cartModal")).to_be_visible()
        expect(page.locator("#cartModal").get_by_text("Added!")).to_be_visible()
        page.locator("#cartModal").get_by_role("link", name="View Cart").click()

        # Verify product is added to cart
        cart_product = page.locator(f"#product-{product_id}")
        expect(cart_product).to_be_visible()
        expect(cart_product).to_contain_text(product_name)

        # Verify price, quantity and total price
        expect(cart_product.locator(".cart_price")).to_contain_text(product_price)
        expect(cart_product.locator(".cart_quantity")).to_contain_text("1")
        expect(cart_product.locator(".cart_total_price")).to_contain_text(product_price)

        print(f"Product validated in cart: {product_name} | Price: {product_price}")

        browser.close()