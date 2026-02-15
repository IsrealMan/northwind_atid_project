from sqlalchemy import select
from src.db import SessionLocal
from src.models import Product
from src.atid_playwright import get_category_names_from_ui

def test_category_subset_exists_on_ui():
    # Example category on the demo store
    category_slug = "women"
    category_url = f"https://atid.store/product-category/{category_slug}/"

    ui_names = get_category_names_from_ui(category_url, headless=True)
    assert ui_names, "No products found in UI category page."

    with SessionLocal() as db:
        db_names = set(
            p.name for p in db.execute(select(Product).where(Product.category.ilike("Women"))).scalars().all()
        )

    assert db_names, "DB has no 'Women' category products. Ensure seed captures category."

    missing = db_names - ui_names
    assert not missing, f"DB category products missing in UI category page: {missing}"
