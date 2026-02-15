import math
from sqlalchemy import select
from src.db import SessionLocal
from src.models import Product
from src.atid_playwright import get_product_from_ui

TOL = 0.01

def test_batch_5_products_price_and_stock_ui():
    with SessionLocal() as db:
        products = db.execute(select(Product).order_by(Product.id.asc())).scalars().all()[:5]
        assert len(products) == 5, "Need at least 5 products in DB. Run seed."

    for p in products:
        ui = get_product_from_ui(p.product_url, headless=True)
        assert p.name == ui.name
        assert math.isclose(p.price, ui.price, abs_tol=TOL)
        assert p.in_stock == ui.in_stock
