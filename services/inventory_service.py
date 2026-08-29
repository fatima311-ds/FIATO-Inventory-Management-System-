from database.database import SessionLocal
from database.models import Ingredient, StockTransaction


def add_stock(
    ingredient_id,
    quantity,
    transaction_type="Purchase",
    reference=None,
    notes=None
):
    """
    Add stock to an ingredient.
    Used mainly for purchases and positive adjustments.
    """

    db = SessionLocal()

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        db.close()
        raise ValueError("Ingredient not found.")

    if quantity <= 0:
        db.close()
        raise ValueError("Quantity must be greater than zero.")

    transaction = StockTransaction(
        ingredient_id=ingredient.id,
        transaction_type=transaction_type,
        quantity=quantity,
        unit=ingredient.unit,
        reference=reference,
        notes=notes
    )

    db.add(transaction)
    db.commit()
    db.close()


def remove_stock(
    ingredient_id,
    quantity,
    transaction_type="Wastage",
    reference=None,
    notes=None
):
    """
    Remove stock from an ingredient.
    Used for wastage, orders, etc.
    """

    db = SessionLocal()

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        db.close()
        raise ValueError("Ingredient not found.")

    if quantity <= 0:
        db.close()
        raise ValueError("Quantity must be greater than zero.")

    current_stock = get_current_stock(
        db,
        ingredient_id
    )

    if quantity > current_stock:
        db.close()
        raise ValueError(
            f"Insufficient stock. "
            f"Available: {current_stock} {ingredient.unit}"
        )

    transaction = StockTransaction(
        ingredient_id=ingredient.id,
        transaction_type=transaction_type,
        quantity=-quantity,
        unit=ingredient.unit,
        reference=reference,
        notes=notes
    )

    db.add(transaction)
    db.commit()
    db.close()


def get_current_stock(db, ingredient_id):
    """
    Calculate current stock from all transactions.
    """

    transactions = db.query(
        StockTransaction
    ).filter(
        StockTransaction.ingredient_id == ingredient_id
    ).all()

    total = sum(
        transaction.quantity
        for transaction in transactions
    )

    return total


def get_all_current_stock():
    """
    Return current stock of all ingredients.
    """

    db = SessionLocal()

    ingredients = db.query(
        Ingredient
    ).filter(
        Ingredient.is_active == True
    ).all()

    stock_data = []

    for ingredient in ingredients:

        current_stock = get_current_stock(
            db,
            ingredient.id
        )

        stock_data.append({
            "id": ingredient.id,
            "name": ingredient.name,
            "unit": ingredient.unit,
            "current_stock": current_stock,
            "minimum_level": ingredient.minimum_level,
            "rate": ingredient.rate
        })

    db.close()

    return stock_data

def get_stock_status(
    current_stock,
    minimum_level,
    has_transactions=True
):

    if not has_transactions:
        return "NOT SET"

    if current_stock <= 0:
        return "OUT OF STOCK"

    if minimum_level <= 0:
        return "HEALTHY"

    if current_stock <= minimum_level * 0.5:
        return "CRITICAL"

    if current_stock <= minimum_level:
        return "LOW STOCK"

    return "HEALTHY"
def update_minimum_level(
    ingredient_id,
    minimum_level
):

    db = SessionLocal()

    ingredient = db.query(
        Ingredient
    ).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        db.close()
        raise ValueError("Ingredient not found.")

    if minimum_level < 0:
        db.close()
        raise ValueError(
            "Minimum level cannot be negative."
        )

    ingredient.minimum_level = minimum_level

    db.commit()
    db.close()
from datetime import datetime

def add_purchase(
    db,
    ingredient_id,
    quantity,
    unit,
    unit_price,
    total_cost,
    supplier=None,
    notes=None
):
    """
    Add a purchase and corresponding stock transaction.

    The purchase quantity is converted into the ingredient's
    base unit before saving.
    """

    from database.models import (
        Ingredient,
        Purchase,
        StockTransaction
    )

    ingredient = db.query(
        Ingredient
    ).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        raise ValueError("Ingredient not found.")

    if quantity <= 0:
        raise ValueError(
            "Purchase quantity must be greater than zero."
        )

    if unit_price < 0:
        raise ValueError(
            "Unit price cannot be negative."
        )

    if total_cost < 0:
        raise ValueError(
            "Total cost cannot be negative."
        )

    from utils.calculations import (
        convert_to_base_unit
    )

    base_quantity = convert_to_base_unit(
        quantity,
        unit,
        ingredient.unit
    )

    # ---------------------------------------------
    # Save Purchase
    # ---------------------------------------------

    purchase = Purchase(
        ingredient_id=ingredient_id,
        quantity=base_quantity,
        unit_price=unit_price,
        total_cost=total_cost,
        supplier=supplier,
        notes=notes
    )

    db.add(purchase)

    # ---------------------------------------------
    # Save Stock Transaction
    # ---------------------------------------------

    transaction = StockTransaction(
        ingredient_id=ingredient_id,
        transaction_type="PURCHASE",
        quantity=base_quantity,
        unit=ingredient.unit,
        reference="PURCHASE",
        notes=notes
    )

    db.add(transaction)

    db.commit()

    db.refresh(purchase)

    return purchase

def delete_purchase(purchase_id):
    from database.models import Purchase, StockTransaction

    db = SessionLocal()

    try:
        purchase = db.query(Purchase).filter(
            Purchase.id == purchase_id
        ).first()

        if not purchase:
            raise ValueError("Purchase not found.")

        ingredient_id = purchase.ingredient_id
        quantity = purchase.quantity
        unit = purchase.ingredient.unit

        # Check current stock
        current_stock = get_current_stock(
            db,
            ingredient_id
        )

        if current_stock < quantity:
            raise ValueError(
                f"Cannot delete this purchase because "
                f"current stock is only {current_stock:g} {unit}."
            )

        # Create reverse transaction
        reversal = StockTransaction(
            ingredient_id=ingredient_id,
            transaction_type="PURCHASE_REVERSAL",
            quantity=-quantity,
            unit=unit,
            reference=f"DELETE_PURCHASE:{purchase.id}",
            notes=f"Purchase #{purchase.id} deleted"
        )

        db.add(reversal)

        # Delete purchase record
        db.delete(purchase)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()