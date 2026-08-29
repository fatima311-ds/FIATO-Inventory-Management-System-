from database.database import SessionLocal
from database.models import (
    Order,
    Recipe,
    Ingredient,
    StockTransaction
)


def simulate_order(menu_item_id, size_id, order_quantity):
    """
    Simulate an order without changing database stock.
    """

    if order_quantity <= 0:
        raise ValueError("Order quantity must be greater than zero.")

    db = SessionLocal()

    try:

        recipes = db.query(Recipe).filter(
            Recipe.menu_item_id == menu_item_id,
            Recipe.size_id == size_id
        ).all()

        if not recipes:
            raise ValueError(
                "Recipe not found for selected pasta and size."
            )

        details = []
        can_fulfill = True

        for recipe in recipes:

            ingredient = db.query(Ingredient).filter(
                Ingredient.id == recipe.ingredient_id
            ).first()

            if not ingredient:
                continue

            # Current stock from transactions
            transactions = db.query(
                StockTransaction
            ).filter(
                StockTransaction.ingredient_id == ingredient.id
            ).all()

            current_stock = sum(
                t.quantity for t in transactions
            )

            required = recipe.quantity * order_quantity

            remaining = current_stock - required

            if remaining < 0:
                can_fulfill = False

            details.append({
                "ingredient": ingredient.name,
                "current_stock": current_stock,
                "required": required,
                "remaining": remaining,
                "unit": ingredient.unit,
                "available": remaining >= 0
            })

        return {
            "can_fulfill": can_fulfill,
            "details": details
        }

    finally:
        db.close()


def place_order(menu_item_id, size_id, order_quantity):
    """
    Save actual order and deduct ingredient stock.
    """

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
                "Recipe not found for selected pasta and size."
            )

        total_cost = 0

        # Check stock first
        for recipe in recipes:

            ingredient = db.query(Ingredient).filter(
                Ingredient.id == recipe.ingredient_id
            ).first()

            transactions = db.query(
                StockTransaction
            ).filter(
                StockTransaction.ingredient_id == ingredient.id
            ).all()

            current_stock = sum(
                t.quantity for t in transactions
            )

            required = recipe.quantity * order_quantity

            if required > current_stock:
                raise ValueError(
                    f"Insufficient stock for {ingredient.name}. "
                    f"Required: {required:g} {ingredient.unit}, "
                    f"Available: {current_stock:g} {ingredient.unit}"
                )

            # Cost
            if ingredient.rate:
                total_cost += recipe.quantity * order_quantity * ingredient.rate

        # Save order
        order = Order(
            menu_item_id=menu_item_id,
            size_id=size_id,
            quantity=order_quantity,
            total_cost=total_cost
        )

        db.add(order)
        db.flush()

        # Deduct stock
        for recipe in recipes:

            ingredient = db.query(Ingredient).filter(
                Ingredient.id == recipe.ingredient_id
            ).first()

            required = recipe.quantity * order_quantity

            transaction = StockTransaction(
                ingredient_id=ingredient.id,
                transaction_type="ORDER",
                quantity=-required,
                unit=ingredient.unit,
                reference=f"ORDER-{order.id}",
                notes=f"Order of {order_quantity} item(s)"
            )

            db.add(transaction)

        db.commit()

        return order

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()