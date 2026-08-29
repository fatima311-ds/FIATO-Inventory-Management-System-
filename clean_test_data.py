from database.database import SessionLocal
from database.models import (
    Ingredient,
    Recipe,
    Purchase,
    StockTransaction,
    Order
)

db = SessionLocal()

try:

    print("\n========== CLEANING TEST DATA ==========\n")

    # =====================================================
    # 1. REMOVE TEST TRANSACTIONS
    # =====================================================

    print("Deleting test purchases...")
    db.query(Purchase).delete(
        synchronize_session=False
    )

    print("Deleting test stock transactions...")
    db.query(StockTransaction).delete(
        synchronize_session=False
    )

    print("Deleting test orders...")
    db.query(Order).delete(
        synchronize_session=False
    )

    # Reset stock
    print("Resetting current stock...")

    db.query(Ingredient).update(
        {
            Ingredient.current_stock: 0
        },
        synchronize_session=False
    )

    # =====================================================
    # 2. CLIENT CANONICAL NAMES
    # =====================================================

    canonical_names = {
        "Black Pepper": [
            "Black Pepper",
            "Black peper"
        ],

        "Butter": [
            "Butter"
        ],

        "Cheddar": [
            "Cheddar",
            "Cheddar(Cheese )"
        ],

        "Chicken": [
            "Chicken"
        ],

        "Chili Flakes": [
            "Chili Flakes",
            "Chili flakes"
        ],

        "Cream": [
            "Cream"
        ],

        "Fettuccine": [
            "Fettuccine"
        ],

        "Fork": [
            "Fork"
        ],

        "Garlic": [
            "Garlic"
        ],

        "Gas Cylinder Refill": [
            "Gas Cylinder Refill"
        ],

        "LargeBox": [
            "LargeBox",
            "Large Box"
        ],

        "Milk": [
            "Milk"
        ],

        "Oil": [
            "Oil"
        ],

        "Oregano": [
            "Oregano"
        ],

        "PaperBag": [
            "PaperBag",
            "Paper Bag"
        ],

        "Penne": [
            "Penne"
        ],

        "Regular Box": [
            "Regular Box",
            "Regular Box "
        ],

        "Salt": [
            "Salt"
        ],

        "Sticker": [
            "Sticker"
        ],

        "Tikka Masala": [
            "Tikka Masala",
            "TikkaMassala"
        ],

        "Tomato": [
            "Tomato"
        ]
    }

    # =====================================================
    # 3. MERGE DUPLICATE INGREDIENTS
    # =====================================================

    for canonical_name, possible_names in canonical_names.items():

        rows = []

        for name in possible_names:

            found = db.query(Ingredient).filter(
                Ingredient.name == name
            ).all()

            rows.extend(found)

        if not rows:
            continue

        # Prefer exact canonical name
        canonical = None

        for row in rows:
            if row.name == canonical_name:
                canonical = row
                break

        # If exact canonical row doesn't exist,
        # keep the first available row and rename it.
        if canonical is None:

            canonical = rows[0]
            canonical.name = canonical_name

        # =================================================
        # MOVE RECIPES FROM DUPLICATE → CANONICAL
        # =================================================

        for duplicate in rows:

            if duplicate.id == canonical.id:
                continue

            recipes = db.query(Recipe).filter(
                Recipe.ingredient_id == duplicate.id
            ).all()

            for recipe in recipes:

                existing_recipe = db.query(Recipe).filter(
                    Recipe.menu_item_id == recipe.menu_item_id,
                    Recipe.size_id == recipe.size_id,
                    Recipe.ingredient_id == canonical.id
                ).first()

                if existing_recipe:

                    # Duplicate recipe already exists.
                    db.delete(recipe)

                else:

                    # Move recipe to canonical ingredient.
                    recipe.ingredient_id = canonical.id

            # Delete duplicate ingredient
            db.delete(duplicate)

    # =====================================================
    # 4. REMOVE PRACTICE-ONLY INGREDIENT
    # =====================================================

    parmesan = db.query(Ingredient).filter(
        Ingredient.name == "Parmesan"
    ).first()

    if parmesan:

        # Parmesan should not be used by final client recipes
        recipes = db.query(Recipe).filter(
            Recipe.ingredient_id == parmesan.id
        ).all()

        for recipe in recipes:
            db.delete(recipe)

        db.delete(parmesan)

    # =====================================================
    # 5. COMMIT
    # =====================================================

    db.commit()

    print("\n========================================")
    print("CLIENT DATABASE CLEANED SUCCESSFULLY")
    print("========================================\n")

    # =====================================================
    # 6. SHOW REMAINING INGREDIENTS
    # =====================================================

    ingredients = db.query(
        Ingredient
    ).order_by(
        Ingredient.name
    ).all()

    print("Remaining Ingredients:\n")

    for ingredient in ingredients:

        print(
            f"{ingredient.name} | "
            f"{ingredient.unit} | "
            f"Rate: {ingredient.rate}"
        )

    print("\n========================================")
    print("Cleanup completed.")
    print("========================================")

except Exception as e:

    db.rollback()

    print("\nERROR:")
    print(e)

    print("\nNO CHANGES WERE COMMITTED.")

finally:

    db.close()