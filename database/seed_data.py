from database.database import SessionLocal
from database.models import Ingredient, MenuItem, Size


def seed_database():

    db = SessionLocal()

    # ---------------------------------------
    # INGREDIENTS
    # ---------------------------------------

    ingredients = [
        {
            "name": "Fettuccine",
            "unit": "g",
            "rate": 1.30
        },
        {
            "name": "Penne",
            "unit": "g",
            "rate": 0.50
        },
        {
            "name": "Cream",
            "unit": "ml",
            "rate": 0.725
        },
        {
            "name": "Cheddar",
            "unit": "g",
            "rate": 2.50
        },
        {
            "name": "Oil",
            "unit": "ml",
            "rate": 0.57
        },
        {
            "name": "Butter",
            "unit": "g",
            "rate": 0.57
        },
        {
            "name": "Tikka Masala",
            "unit": "g",
            "rate": 3.375
        },
        {
            "name": "Oregano",
            "unit": "g",
            "rate": 5.833
        },
        {
            "name": "Salt",
            "unit": "g",
            "rate": 0.1375
        },
        {
            "name": "Black Pepper",
            "unit": "g",
            "rate": 3.50
        },
        {
            "name": "Tomato",
            "unit": "g",
            "rate": 0.25
        },
        {
            "name": "Garlic",
            "unit": "g",
            "rate": 0.375
        },
        {
            "name": "Chicken",
            "unit": "g",
            "rate": 0.667
        },
        {
            "name": "Milk",
            "unit": "ml",
            "rate": 0.24
        },
        {
            "name": "Chili Flakes",
            "unit": "g",
            "rate": 8.00
        },
        {
            "name": "Parmesan",
            "unit": "g",
            "rate": None
        }
    ]

    for item in ingredients:

        existing = db.query(Ingredient).filter(
            Ingredient.name == item["name"]
        ).first()

        if not existing:

            ingredient = Ingredient(
                name=item["name"],
                unit=item["unit"],
                rate=item["rate"],
                minimum_level=0,
                current_stock=0
            )

            db.add(ingredient)

    # ---------------------------------------
    # MENU ITEMS
    # ---------------------------------------

    menu_items = [
        {
            "name": "Alfredo Fettuccine",
            "description": "Creamy chicken fettuccine"
        },
        {
            "name": "Pink Penne",
            "description": "Creamy tomato and cheese penne"
        },
        {
            "name": "Penne Arrabbiata",
            "description": "Tomato, garlic and chili penne"
        }
    ]

    for item in menu_items:

        existing = db.query(MenuItem).filter(
            MenuItem.name == item["name"]
        ).first()

        if not existing:

            menu_item = MenuItem(
                name=item["name"],
                description=item["description"]
            )

            db.add(menu_item)

    # ---------------------------------------
    # SIZES
    # ---------------------------------------

    sizes = [
        {
            "name": "Regular",
            "volume_ml": 700,
            "multiplier": 0.70
        },
        {
            "name": "Large",
            "volume_ml": 1000,
            "multiplier": 1.00
        }
    ]

    for item in sizes:

        existing = db.query(Size).filter(
            Size.name == item["name"]
        ).first()

        if not existing:

            size = Size(
                name=item["name"],
                volume_ml=item["volume_ml"],
                multiplier=item["multiplier"]
            )

            db.add(size)

    db.commit()
    db.close()

    print("FIATO initial data added successfully!")


if __name__ == "__main__":
    seed_database()