from datetime import datetime
from sqlalchemy import select
from src.db import engine, SessionLocal
from src.models import Base, Product
import requests
from bs4 import BeautifulSoup

BASE = "https://atid.store"

def init_db():
    Base.metadata.create_all(bind=engine)

def get_products():
    r = requests.get(f"{BASE}/store/", headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "lxml")
    products = []

    for li in soup.select("li.product"):
        name = li.select_one("h2").get_text(strip=True)
        price_text = li.select_one("span.price").get_text(strip=True)
        price = float(''.join(c for c in price_text if c.isdigit() or c=='.'))
        url = li.select_one("a")["href"]

        products.append({
            "name": name,
            "price": price,
            "url": url
        })
    return products

def seed():
    products = get_products()[:10]
    with SessionLocal() as db:
        for p in products:
            existing = db.execute(select(Product).where(Product.product_url == p["url"])).scalar_one_or_none()
            if not existing:
                db.add(Product(
                    name=p["name"],
                    price=p["price"],
                    currency="ILS",
                    in_stock=True,
                    product_url=p["url"],
                    last_seen_at=datetime.utcnow()
                ))
        db.commit()

if __name__ == "__main__":
    init_db()
    seed()
    print("Seed completed")
