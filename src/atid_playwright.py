import re
from dataclasses import dataclass
from playwright.sync_api import sync_playwright

@dataclass
class UiProduct:
    name: str
    price: float
    in_stock: bool

_money_re = re.compile(r"([0-9]+(?:\.[0-9]+)?)")

def _parse_price(text: str) -> float:
    nums = _money_re.findall(text.replace(",", ""))
    if not nums:
        raise ValueError(f"Cannot parse price from: {text!r}")
    return float(nums[-1])

def get_product_from_ui(product_url: str, headless: bool = True) -> UiProduct:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        page.goto(product_url, wait_until="domcontentloaded")

        # WooCommerce selectors
        name = page.locator("h1.product_title").first.inner_text().strip()

        # price can be p.price or span.price
        price_text = (page.locator("p.price").first.inner_text()
                      if page.locator("p.price").count() else
                      page.locator("span.price").first.inner_text())
        price = _parse_price(price_text)

        stock_text = ""
        if page.locator("p.stock").count():
            stock_text = page.locator("p.stock").first.inner_text().lower()
        in_stock = "out of stock" not in stock_text

        browser.close()
        return UiProduct(name=name, price=price, in_stock=in_stock)

def get_category_names_from_ui(category_url: str, headless: bool = True) -> set[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        page.goto(category_url, wait_until="domcontentloaded")
        page.wait_for_timeout(500)  # small buffer for dynamic rendering

        names = set()
        for el in page.locator("li.product h2.woocommerce-loop-product__title").all():
            names.add(el.inner_text().strip())

        browser.close()
        return names
