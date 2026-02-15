import math
from sqlalchemy import select
from src.db import SessionLocal
from src.models import Product
from src.atid_playwright import get_product_from_ui

TOL = 0.01

def test_single_product_name_and_price_ui():
    with SessionLocal() as db:
        p = db.execute(select(Product).order_by(Product.id.asc())).scalars().first()
        assert p is not None, "No products in DB. Run seed first."

    ui = get_product_from_ui(p.product_url, headless=True)

    assert p.name == ui.name
    assert math.isclose(p.price, ui.price, abs_tol=TOL)
