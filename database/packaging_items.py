from database.database import SessionLocal
from database.models import Ingredient

db = SessionLocal()

new_items = [
    {"name": "Regular Box ", "unit": "pcs"},
    {"name": "Large Box", "unit": "pcs"},
    {"name": "Sticker", "unit": "pcs"},
    {"name": "Paper Bag", "unit": "pcs"},
    {"name": "Fork", "unit": "pcs"},
    {"name": "Gas Cylinder Refill", "unit": "kg"},
]

for item in new_items:

    existing = db.query(Ingredient).filter(
        Ingredient.name == item["name"]
    ).first()

    if existing:
        print(f"Skipped (already exists): {item['name']}")
        continue

    ingredient = Ingredient(
        name=item["name"],
        unit=item["unit"],
        rate=0,
        minimum_level=0,
        current_stock=0,
        is_active=True
    )

    db.add(ingredient)
    print(f"Added: {item['name']} ({item['unit']})")

db.commit()
db.close()

print("Done! Packaging items added successfully.")