from database.database import SessionLocal

from database.models import (
    Ingredient,
    Purchase,
    Recipe
)


# =========================================================
# RATE CONVERSION
# =========================================================

def convert_rate_to_base_unit(
    rate,
    purchase_unit,
    base_unit
):
    """
    Convert purchase rate into ingredient base-unit rate.

    Examples:

    1190 PKR/kg → 1.19 PKR/g

    750 PKR/L → 0.75 PKR/ml
    """

    if purchase_unit == base_unit:
        return rate

    if purchase_unit == "kg" and base_unit == "g":
        return rate / 1000

    if purchase_unit == "L" and base_unit == "ml":
        return rate / 1000

    return rate


# =========================================================
# WEIGHTED AVERAGE COST
# =========================================================

def get_weighted_average_cost(
    ingredient_id
):
    """
    Calculate weighted average purchase cost
    using purchase history.
    """

    db = SessionLocal()

    try:

        ingredient = db.query(
            Ingredient
        ).filter(
            Ingredient.id == ingredient_id
        ).first()

        if not ingredient:
            return None

        purchases = db.query(
            Purchase
        ).filter(
            Purchase.ingredient_id == ingredient_id
        ).all()

        if not purchases:
            return None

        total_quantity = 0.0
        total_value = 0.0

        for purchase in purchases:

            if not purchase.quantity:
                continue

            if purchase.unit_price is None:
                continue

            quantity = purchase.quantity

            # Purchase quantity is already saved
            # in ingredient's base unit.

            if quantity > 0:
                rate_per_base_unit = purchase.total_cost / quantity
            else:
                continue

            total_quantity += quantity

            total_value += (
                quantity *
                rate_per_base_unit
            )

        if total_quantity == 0:
            return None

        return (
            total_value /
            total_quantity
        )

    finally:

        db.close()


# =========================================================
# RECIPE COST
# =========================================================

def calculate_recipe_cost(
    menu_item_id,
    size_id
):

    db = SessionLocal()

    try:

        recipes = db.query(
            Recipe
        ).filter(
            Recipe.menu_item_id == menu_item_id,
            Recipe.size_id == size_id
        ).all()

        if not recipes:
            return None

        details = []

        total_ingredient_cost = 0.0

        missing_rates = []

        for recipe in recipes:

            ingredient = recipe.ingredient

            weighted_rate = (
                get_weighted_average_cost(
                    ingredient.id
                )
            )

            # -----------------------------------------
            # No purchase history
            # -----------------------------------------

            if weighted_rate is None:

                details.append({
                    "ingredient": ingredient.name,
                    "quantity": recipe.quantity,
                    "unit": recipe.unit,
                    "rate": None,
                    "cost": None
                })

                missing_rates.append(
                    ingredient.name
                )

                continue

            ingredient_cost = (
                recipe.quantity *
                weighted_rate
            )

            total_ingredient_cost += (
                ingredient_cost
            )

            details.append({
                "ingredient": ingredient.name,
                "quantity": recipe.quantity,
                "unit": recipe.unit,
                "rate": weighted_rate,
                "cost": ingredient_cost
            })

        return {
            "total_ingredient_cost":
                total_ingredient_cost,

            "details":
                details,

            "missing_rates":
                missing_rates
        }

    finally:

        db.close()


def get_packaging_cost(size_name):

    db = SessionLocal()

    try:

        packaging = {
            "Regular": {
                "Regular Box": 1,
                "Fork": 1,
                "PaperBag": 1,
                "Sticker": 1
            },

            "Large": {
                "LargeBox": 1,
                "Fork": 1,
                "PaperBag": 1,
                "Sticker": 1
            }
        }

        required_items = packaging.get(
            size_name,
            {}
        )

        total = 0.0
        details = []

        for item_name, quantity in required_items.items():

            ingredient = db.query(
                Ingredient
            ).filter(
                Ingredient.name == item_name
            ).first()

            if not ingredient:
                continue

            rate = get_weighted_average_cost(
                ingredient.id
            )

            if rate is None:
                continue

            cost = rate * quantity

            total += cost

            details.append({
                "item": item_name,
                "quantity": quantity,
                "rate": rate,
                "cost": cost
            })

        return {
            "total": total,
            "details": details
        }

    finally:

        db.close()        