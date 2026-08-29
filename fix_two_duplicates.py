from database.database import SessionLocal
from database.models import Ingredient, Recipe

db = SessionLocal()

try:

    # =====================================================
    # BLACK PEPPER
    # =====================================================

    black_pepper = db.query(Ingredient).filter(
        Ingredient.name == "Black Pepper"
    ).first()

    black_pepper_duplicate = db.query(Ingredient).filter(
        Ingredient.name == "Black pepper"
    ).first()

    if black_pepper and black_pepper_duplicate:

        recipes = db.query(Recipe).filter(
            Recipe.ingredient_id == black_pepper_duplicate.id
        ).all()

        for recipe in recipes:

            existing_recipe = db.query(Recipe).filter(
                Recipe.menu_item_id == recipe.menu_item_id,
                Recipe.size_id == recipe.size_id,
                Recipe.ingredient_id == black_pepper.id
            ).first()

            if existing_recipe:
                db.delete(recipe)
            else:
                recipe.ingredient_id = black_pepper.id

        db.delete(black_pepper_duplicate)

        print("✅ Black pepper duplicate removed.")

    elif black_pepper_duplicate and not black_pepper:

        black_pepper_duplicate.name = "Black Pepper"

        print("✅ Black pepper renamed.")

    else:

        print("ℹ️ Black Pepper duplicate not found.")


    # =====================================================
    # TIKKA MASALA
    # =====================================================

    tikka_masala = db.query(Ingredient).filter(
        Ingredient.name == "Tikka Masala"
    ).first()

    tikka_duplicate = db.query(Ingredient).filter(
        Ingredient.name == "Tikka Massala"
    ).first()

    if tikka_masala and tikka_duplicate:

        recipes = db.query(Recipe).filter(
            Recipe.ingredient_id == tikka_duplicate.id
        ).all()

        for recipe in recipes:

            existing_recipe = db.query(Recipe).filter(
                Recipe.menu_item_id == recipe.menu_item_id,
                Recipe.size_id == recipe.size_id,
                Recipe.ingredient_id == tikka_masala.id
            ).first()

            if existing_recipe:
                db.delete(recipe)
            else:
                recipe.ingredient_id = tikka_masala.id

        db.delete(tikka_duplicate)

        print("✅ Tikka Masala duplicate removed.")

    elif tikka_duplicate and not tikka_masala:

        tikka_duplicate.name = "Tikka Masala"

        print("✅ Tikka Masala renamed.")

    else:

        print("ℹ️ Tikka Masala duplicate not found.")


    # =====================================================
    # SAVE
    # =====================================================

    db.commit()

    print("\n===================================")
    print("✅ DUPLICATES FIXED SUCCESSFULLY")
    print("===================================")

except Exception as e:

    db.rollback()

    print("❌ ERROR:")
    print(e)

finally:

    db.close()