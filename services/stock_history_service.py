from database.database import SessionLocal
from database.models import StockTransaction


def get_stock_history():

    db = SessionLocal()

    transactions = db.query(
        StockTransaction
    ).order_by(
        StockTransaction.created_at.desc()
    ).all()

    history = []

    for transaction in transactions:

        history.append({
            "date": transaction.created_at,
            "ingredient": transaction.ingredient.name,
            "type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "unit": transaction.unit,
            "reference": transaction.reference,
            "notes": transaction.notes
        })

    db.close()

    return history