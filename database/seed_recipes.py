from database.database import SessionLocal
from database.models import MenuItem, Size, Ingredient, Recipe

from database.recipe_data import (
    ALFREDO_LARGE,
    ALFREDO_REGULAR,
    PINK_LARGE,
    PINK_REGULAR,
    ARRABIATA_LARGE,
    ARRABIATA_REGULAR
)


def add_recipe(
    db,
    menu_name,
    size_name,
    recipe_data
):

    menu_item = db.query(MenuItem).filter(
        MenuItem.name == menu_name
    ).first()

    size = db.query(Size).filter(
        Size.name == size_name
    ).first()

    if not menu_item:
        raise ValueError(
            f"Menu item not found: {menu_name}"
        )

    if not size:
        raise ValueError(
            f"Size not found: {size_name}"
        )

    for ingredient_name, quantity in recipe_data.items():

        ingredient = db.query(Ingredient).filter(
            Ingredient.name == ingredient_name
        ).first()

        if not ingredient:
            raise ValueError(
                f"Ingredient not found: {ingredient_name}"
            )

        existing = db.query(Recipe).filter(
            Recipe.menu_item_id == menu_item.id,
            Recipe.size_id == size.id,
            Recipe.ingredient_id == ingredient.id
        ).first()

        if not existing:

            recipe = Recipe(
                menu_item_id=menu_item.id,
                size_id=size.id,
                ingredient_id=ingredient.id,
                quantity=quantity,
                unit=ingredient.unit
            )

            db.add(recipe)


def seed_recipes():

    db = SessionLocal()

    add_recipe(
        db,
        "Alfredo Fettuccine",
        "Large",
        ALFREDO_LARGE
    )

    add_recipe(
        db,
        "Alfredo Fettuccine",
        "Regular",
        ALFREDO_REGULAR
    )

    add_recipe(
        db,
        "Pink Penne",
        "Large",
        PINK_LARGE
    )

    add_recipe(
        db,
        "Pink Penne",
        "Regular",
        PINK_REGULAR
    )

    add_recipe(
        db,
        "Penne Arrabbiata",
        "Large",
        ARRABIATA_LARGE
    )

    add_recipe(
        db,
        "Penne Arrabbiata",
        "Regular",
        ARRABIATA_REGULAR
    )

    db.commit()
    db.close()

    print("FIATO recipes added successfully!")


if __name__ == "__main__":
    seed_recipes()