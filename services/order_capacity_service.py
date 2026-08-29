from database.database import SessionLocal
from database.models import (
    Recipe,
    Ingredient,
    MenuItem,
    Size,
    Order,
    StockTransaction
)


# =========================================================
# GET CURRENT STOCK
# =========================================================

def get_current_stock(db, ingredient_id):

    transactions = db.query(
        StockTransaction
    ).filter(
        StockTransaction.ingredient_id == ingredient_id
    ).all()

    return sum(
        transaction.quantity
        for transaction in transactions
    )


# =========================================================
# GET PASTA CAPACITY
# =========================================================

def calculate_pasta_capacity(menu_item_id, size_id):

    db = SessionLocal()

    try:

        recipes = db.query(Recipe).filter(
            Recipe.menu_item_id == menu_item_id,
            Recipe.size_id == size_id
        ).all()

        if not recipes:
            return None

        capacity_list = []

        for recipe in recipes:

            stock = get_current_stock(
                db,
                recipe.ingredient_id
            )

            if recipe.quantity <= 0:
                continue

            possible_orders = int(
                stock / recipe.quantity
            )

            capacity_list.append({
                "ingredient": recipe.ingredient.name,
                "available": stock,
                "required": recipe.quantity,
                "unit": recipe.unit,
                "possible_orders": possible_orders
            })

        if not capacity_list:
            return None

        limiting_item = min(
            capacity_list,
            key=lambda x: x["possible_orders"]
        )

        return {
            "maximum_orders": limiting_item["possible_orders"],
            "limiting_ingredient": limiting_item["ingredient"],
            "details": capacity_list
        }

    finally:
        db.close()


# =========================================================
# GET ALL PASTA CAPACITY
# =========================================================

def get_all_pasta_capacity():

    db = SessionLocal()

    try:

        menu_items = db.query(
            MenuItem
        ).filter(
            MenuItem.is_active == True
        ).order_by(
            MenuItem.name
        ).all()

        sizes = db.query(
            Size
        ).order_by(
            Size.volume_ml
        ).all()

        results = []

        for menu_item in menu_items:

            for size in sizes:

                result = calculate_pasta_capacity(
                    menu_item.id,
                    size.id
                )

                if result:

                    results.append({
                        "Pasta": menu_item.name,
                        "Size": size.name,
                        "Maximum Orders": result["maximum_orders"],
                        "Limiting Ingredient": result[
                            "limiting_ingredient"
                        ]
                    })

        return results

    finally:
        db.close()


# =========================================================
# SIMULATE ORDER
# =========================================================

def simulate_order(
    menu_item_id,
    size_id,
    order_quantity
):

    if order_quantity <= 0:
        raise ValueError(
            "Order quantity must be greater than zero."
        )

    db = SessionLocal()

    try:

        recipes = db.query(Recipe).filter(
            Recipe.menu_item_id == menu_item_id,
            Recipe.size_id == size_id
        ).all()

        if not recipes:
            raise ValueError(
                "Recipe not found for this pasta and size."
            )

        ingredient_details = []

        for recipe in recipes:

            stock = get_current_stock(
                db,
                recipe.ingredient_id
            )

            required_total = (
                recipe.quantity * order_quantity
            )

            remaining_stock = stock - required_total

            ingredient_details.append({
                "ingredient": recipe.ingredient.name,
                "current_stock": stock,
                "required": required_total,
                "remaining": remaining_stock,
                "unit": recipe.unit,
                "available": remaining_stock >= 0
            })

        unavailable = [
            item
            for item in ingredient_details
            if not item["available"]
        ]

        return {
            "can_make": len(unavailable) == 0,
            "quantity": order_quantity,
            "details": ingredient_details
        }

    finally:
        db.close()


# =========================================================
# PLACE ACTUAL ORDER
# =========================================================

def place_order(
    menu_item_id,
    size_id,
    order_quantity
):

    if order_quantity <= 0:
        raise ValueError(
            "Order quantity must be greater than zero."
        )

    db = SessionLocal()

    try:

        # -------------------------------------------------
        # Get recipe
        # -------------------------------------------------

        recipes = db.query(Recipe).filter(
            Recipe.menu_item_id == menu_item_id,
            Recipe.size_id == size_id
        ).all()

        if not recipes:
            raise ValueError(
                "Recipe not found for this pasta and size."
            )

        # -------------------------------------------------
        # Check stock BEFORE changing anything
        # -------------------------------------------------

        stock_check = []

        for recipe in recipes:

            current_stock = get_current_stock(
                db,
                recipe.ingredient_id
            )

            required_quantity = (
                recipe.quantity * order_quantity
            )

            if required_quantity > current_stock:

                raise ValueError(
                    f"Insufficient stock for "
                    f"{recipe.ingredient.name}. "
                    f"Required: {required_quantity:g} "
                    f"{recipe.unit}, "
                    f"Available: {current_stock:g} "
                    f"{recipe.unit}."
                )

            stock_check.append({
                "recipe": recipe,
                "current_stock": current_stock,
                "required": required_quantity
            })

        # -------------------------------------------------
        # Calculate total cost
        # -------------------------------------------------

        total_cost = 0

        for item in stock_check:

            recipe = item["recipe"]
            ingredient = recipe.ingredient

            if ingredient.rate:

                total_cost += (
                    ingredient.rate
                    * item["required"]
                )

        # -------------------------------------------------
        # Create Order
        # -------------------------------------------------

        order = Order(
            menu_item_id=menu_item_id,
            size_id=size_id,
            quantity=order_quantity,
            total_cost=total_cost
        )

        db.add(order)

        # -------------------------------------------------
        # Remove ingredients from stock
        # -------------------------------------------------

        stock_changes = []

        for item in stock_check:

            recipe = item["recipe"]
            required_quantity = item["required"]

            transaction = StockTransaction(
                ingredient_id=recipe.ingredient_id,
                transaction_type="ORDER",
                quantity=-required_quantity,
                unit=recipe.unit,
                reference=f"ORDER",
                notes=(
                    f"{order_quantity} x "
                    f"{recipe.menu_item.name} "
                    f"{recipe.size.name}"
                )
            )

            db.add(transaction)

            stock_changes.append({
                "ingredient": recipe.ingredient.name,
                "used": required_quantity,
                "unit": recipe.unit
            })

        db.commit()

        return {
            "order_id": order.id,
            "menu_item": recipes[0].menu_item.name,
            "size": recipes[0].size.name,
            "quantity": order_quantity,
            "total_cost": total_cost,
            "stock_changes": stock_changes
        }

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()