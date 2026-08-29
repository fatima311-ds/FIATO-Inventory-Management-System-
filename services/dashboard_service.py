from database.database import SessionLocal
from database.models import (
    Ingredient,
    StockTransaction,
    Order
)

from services.inventory_service import (
    get_current_stock,
    get_stock_status
)

from services.order_capacity_service import (
    get_all_pasta_capacity
)


# =========================================================
# INVENTORY SUMMARY
# =========================================================

def get_inventory_summary():

    db = SessionLocal()

    try:

        ingredients = db.query(
            Ingredient
        ).filter(
            Ingredient.is_active == True
        ).all()

        total_items = len(ingredients)

        healthy = 0
        low_stock = 0
        critical = 0
        out_of_stock = 0
        not_set = 0

        for ingredient in ingredients:

            transactions_exist = db.query(
                StockTransaction
            ).filter(
                StockTransaction.ingredient_id == ingredient.id
            ).first() is not None

            current_stock = get_current_stock(
                db,
                ingredient.id
            )

            status = get_stock_status(
                current_stock,
                ingredient.minimum_level,
                transactions_exist
            )

            if status == "HEALTHY":
                healthy += 1

            elif status == "LOW STOCK":
                low_stock += 1

            elif status == "CRITICAL":
                critical += 1

            elif status == "OUT OF STOCK":
                out_of_stock += 1

            elif status == "NOT SET":
                not_set += 1

        return {
            "total_items": total_items,
            "healthy": healthy,
            "low_stock": low_stock,
            "critical": critical,
            "out_of_stock": out_of_stock,
            "not_set": not_set
        }

    finally:

        db.close()


# =========================================================
# RECENT STOCK ACTIVITY
# =========================================================

def get_recent_stock_activity(limit=10):

    db = SessionLocal()

    try:

        transactions = db.query(
            StockTransaction
        ).order_by(
            StockTransaction.created_at.desc()
        ).limit(limit).all()

        rows = []

        for transaction in transactions:

            rows.append({
                "Date": transaction.created_at,
                "Ingredient": transaction.ingredient.name,
                "Type": transaction.transaction_type,
                "Quantity": transaction.quantity,
                "Unit": transaction.unit
            })

        return rows

    finally:

        db.close()


# =========================================================
# ORDER SUMMARY
# =========================================================

def get_order_summary():

    db = SessionLocal()

    try:

        total_orders = db.query(
            Order
        ).count()

        total_quantity = 0

        orders = db.query(Order).all()

        for order in orders:
            total_quantity += order.quantity

        return {
            "total_orders": total_orders,
            "total_quantity": total_quantity
        }

    finally:

        db.close()


# =========================================================
# PASTA CAPACITY SUMMARY
# =========================================================

def get_dashboard_capacity():

    try:

        capacity_data = get_all_pasta_capacity()

        if capacity_data:
            return capacity_data

        return []

    except Exception:

        return []