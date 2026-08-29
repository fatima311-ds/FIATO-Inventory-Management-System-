from database.database import SessionLocal
from database.models import Ingredient


# =========================================================
# CLIENT INGREDIENTS + CURRENT MARKET RATES
# =========================================================

client_ingredients = {

    "Black Pepper": {
        "unit": "g",
        "rate": 4000 / 1000
    },

    "Butter": {
        "unit": "g",
        "rate": 2835 / 1000
    },

    "Cheddar": {
        "unit": "g",
        "rate": 1899 / 1000
    },

    "Chicken": {
        "unit": "g",
        "rate": 722 / 1000
    },

    "Chili Flakes": {
        "unit": "g",
        "rate": 350 / 1000
    },

    "Cream": {
        "unit": "ml",
        "rate": 750 / 1000
    },

    "Fettuccine": {
        "unit": "g",
        "rate": 1190 / 1000
    },

    "Garlic": {
        "unit": "g",
        "rate": 339 / 1000
    },

    "Gas Cylinder Refill": {
        "unit": "kg",
        "rate": 500
    },

    "Large Box": {
        "unit": "pcs",
        "rate": 36
    },

    "Milk": {
        "unit": "ml",
        "rate": 250 / 1000
    },

    "Oil": {
        "unit": "ml",
        "rate": 600 / 1000
    },

    "Oregano": {
        "unit": "g",
        "rate": 5114 / 1000
    },

    "Paper Bag": {
        "unit": "pcs",
        "rate": 26
    },

    "Penne": {
        "unit": "g",
        "rate": 250 / 1000
    },

    "Regular Box": {
        "unit": "pcs",
        "rate": 32
    },

    "Salt": {
        "unit": "g",
        "rate": 110 / 1000
    },

    "Sticker": {
        "unit": "pcs",
        "rate": 3
    },

    "Tikka Masala": {
        "unit": "g",
        "rate": 3212 / 1000
    },

    "Tomato": {
        "unit": "g",
        "rate": 240 / 1000
    },

    "Fork": {
        "unit": "pcs",
        "rate": 6
    }
}


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


try:

    added = 0
    updated = 0


    for name, data in client_ingredients.items():

        ingredient = db.query(
            Ingredient
        ).filter(
            Ingredient.name == name
        ).first()


        if ingredient:

            # Update existing ingredient
            ingredient.unit = data["unit"]
            ingredient.rate = data["rate"]
            ingredient.is_active = True

            updated += 1

        else:

            # Create new ingredient
            ingredient = Ingredient(
                name=name,
                unit=data["unit"],
                rate=data["rate"],
                minimum_level=0,
                current_stock=0,
                is_active=True
            )

            db.add(ingredient)

            added += 1


    db.commit()


    print("========================================")
    print("CLIENT INGREDIENT SETUP COMPLETE")
    print("========================================")
    print(f"Ingredients added   : {added}")
    print(f"Ingredients updated : {updated}")
    print("========================================")


except Exception as e:

    db.rollback()

    print("ERROR:")
    print(e)


finally:

    db.close()