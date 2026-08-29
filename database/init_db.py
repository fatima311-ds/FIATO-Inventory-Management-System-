from database.database import engine, Base

# Import models so SQLAlchemy knows about the tables
from database.models import Ingredient, MenuItem,Recipe,StockTransaction,Order,Purchases


def create_database():
    Base.metadata.create_all(bind=engine)
    print("FIATO database created successfully!")


if __name__ == "__main__":
    create_database()