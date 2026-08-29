from database.database import SessionLocal
from database.models import MenuItem, Size, Ingredient, Recipe


db = SessionLocal()


# =========================================================
# CLIENT FINAL RECIPES
# =========================================================

recipes = {

    # -----------------------------------------------------
    # ALFREDO FETTUCCINE
    # -----------------------------------------------------

    "Alfredo Fettuccine": {

        "Regular": {
            "Fettuccine": (90, "g"),
            "Chicken": (100, "g"),
            "Cream": (72, "ml"),
            "Milk": (90, "ml"),
            "Cheddar": (20.25, "g"),
            "Oil": (15.75, "ml"),
            "Garlic": (4.95, "g"),
            "Salt": (1.575, "g"),
            "Black pepper": (0.45, "g"),
            "Oregano": (0.675, "g"),
            "Tikka Massala": (2.7, "g"),
        },

        "Large": {
            "Fettuccine": (120, "g"),
            "Chicken": (150, "g"),
            "Cream": (96, "ml"),
            "Milk": (120, "ml"),
            "Cheddar": (27, "g"),
            "Oil": (21, "ml"),
            "Garlic": (6.6, "g"),
            "Salt": (2.1, "g"),
            "Black pepper": (0.6, "g"),
            "Oregano": (0.9, "g"),
            "Tikka Massala": (3.6, "g"),
        },
    },


    # -----------------------------------------------------
    # PINK PENNE
    # -----------------------------------------------------

    "Pink Penne": {

        "Regular": {
            "Penne": (90, "g"),
            "Chicken": (100, "g"),
            "Tomato": (72, "g"),
            "Cream": (54, "ml"),
            "Milk": (36, "ml"),
            "Garlic": (4.5, "g"),
            "Oil": (9, "ml"),
            "Butter": (4.5, "g"),
            "Cheddar": (18, "g"),
            "Salt": (1.575, "g"),
            "Black pepper": (0.45, "g"),
            "Oregano": (0.45, "g"),
            "Chili flakes": (0.675, "g"),
        },

        "Large": {
            "Penne": (120, "g"),
            "Chicken": (150, "g"),
            "Tomato": (96, "g"),
            "Cream": (72, "ml"),
            "Milk": (48, "ml"),
            "Garlic": (6, "g"),
            "Oil": (12, "ml"),
            "Butter": (6, "g"),
            "Cheddar": (24, "g"),
            "Salt": (2.1, "g"),
            "Black pepper": (0.6, "g"),
            "Oregano": (0.6, "g"),
            "Chili flakes": (0.9, "g"),
        },
    },


    # -----------------------------------------------------
    # PENNE ARRABBIATA
    # -----------------------------------------------------

    "Penne Arrabbiata": {

        "Regular": {
            "Penne": (90, "g"),
            "Chicken": (100, "g"),
            "Tomato": (108, "g"),
            "Oil": (10.8, "ml"),
            "Garlic": (5.4, "g"),
            "Chili flakes": (1.35, "g"),
            "Salt": (1.575, "g"),
            "Black pepper": (0.36, "g"),
            "Oregano": (0.36, "g"),
            "Cheddar": (20, "g"),
        },

        "Large": {
            "Penne": (120, "g"),
            "Chicken": (150, "g"),
            "Tomato": (144, "g"),
            "Oil": (14.4, "ml"),
            "Garlic": (7.2, "g"),
            "Chili flakes": (1.8, "g"),
            "Salt": (2.1, "g"),
            "Black pepper": (0.48, "g"),
            "Oregano": (0.48, "g"),
            "Cheddar": (22, "g"),
        },
    },
}


# =========================================================
# UPDATE RECIPES
# =========================================================

try:

    updated = 0
    added = 0
    missing = []


    for pasta_name, sizes_data in recipes.items():

        # Find pasta
        pasta = db.query(MenuItem).filter(
            MenuItem.name == pasta_name
        ).first()

        if not pasta:

            missing.append(
                f"Pasta not found: {pasta_name}"
            )

            continue


        for size_name, ingredients_data in sizes_data.items():

            # Find size
            size = db.query(Size).filter(
                Size.name == size_name
            ).first()

            if not size:

                missing.append(
                    f"Size not found: {size_name}"
                )

                continue


            for ingredient_name, data in ingredients_data.items():

                quantity, unit = data


                # Find ingredient
                ingredient = db.query(Ingredient).filter(
                    Ingredient.name == ingredient_name
                ).first()


                if not ingredient:

                    missing.append(
                        f"Ingredient not found: {ingredient_name}"
                    )

                    continue


                # Find existing recipe
                recipe = db.query(Recipe).filter(
                    Recipe.menu_item_id == pasta.id,
                    Recipe.size_id == size.id,
                    Recipe.ingredient_id == ingredient.id
                ).first()


                if recipe:

                    # UPDATE existing recipe
                    recipe.quantity = quantity
                    recipe.unit = unit

                    updated += 1

                else:

                    # ADD if it doesn't already exist
                    new_recipe = Recipe(
                        menu_item_id=pasta.id,
                        size_id=size.id,
                        ingredient_id=ingredient.id,
                        quantity=quantity,
                        unit=unit
                    )

                    db.add(new_recipe)

                    added += 1


    db.commit()


    print("\n====================================")
    print("CLIENT RECIPES UPDATED")
    print("====================================")

    print(f"Updated recipes : {updated}")
    print(f"Added recipes   : {added}")


    if missing:

        print("\nMISSING ITEMS:")
        for item in missing:
            print("-", item)

    else:

        print("\n✅ All client recipe ingredients found.")


except Exception as e:

    db.rollback()

    print("\n❌ ERROR:")
    print(e)


finally:

    db.close()