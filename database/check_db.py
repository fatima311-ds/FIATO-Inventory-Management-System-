from database.models import Recipe
from database.database import SessionLocal
from database.models import Ingredient, MenuItem, Size


db = SessionLocal()

print("\n========== INGREDIENTS ==========")

ingredients = db.query(Ingredient).all()

for ingredient in ingredients:
    print(
        ingredient.name,
        "|",
        ingredient.rate,
        "Rs/",
        ingredient.unit
    )


print("\n========== MENU ==========")

menu_items = db.query(MenuItem).all()

for item in menu_items:
    print(item.name)


print("\n========== SIZES ==========")

sizes = db.query(Size).all()

for size in sizes:
    print(
        size.name,
        "|",
        size.volume_ml,
        "ml",
        "| multiplier:",
        size.multiplier
    )


db.close()
print("\n========== RECIPES ==========")

recipes = db.query(Recipe).all()

for recipe in recipes:

    print(
        recipe.menu_item.name,
        "|",
        recipe.size.name,
        "|",
        recipe.ingredient.name,
        "|",
        recipe.quantity,
        recipe.unit
    )