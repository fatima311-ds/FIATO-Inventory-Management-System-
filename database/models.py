from datetime import datetime 
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey, 
    DateTime,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from database.database import Base


# =========================================================
# INGREDIENT
# =========================================================

class Ingredient(Base):

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    unit = Column(
        String,
        nullable=False
    )

    rate = Column(
        Float,
        nullable=True
    )

    minimum_level = Column(
        Float,
        default=0
    )

    current_stock = Column(
        Float,
        default=0
    )

    is_active = Column(
        Boolean,
        default=True
    )

    # Relationship with Recipe
    recipes = relationship(
        "Recipe",
        back_populates="ingredient"
    )


# =========================================================
# MENU ITEM
# =========================================================

class MenuItem(Base):

    __tablename__ = "menu_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    # Relationship with Recipe
    recipes = relationship(
        "Recipe",
        back_populates="menu_item"
    )


# =========================================================
# SIZE
# =========================================================

class Size(Base):

    __tablename__ = "sizes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    volume_ml = Column(
        Integer,
        nullable=False
    )

    multiplier = Column(
        Float,
        nullable=False
    )

    # Relationship with Recipe
    recipes = relationship(
        "Recipe",
        back_populates="size"
    )


# =========================================================
# RECIPE
# =========================================================

class Recipe(Base):

    __tablename__ = "recipes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.id"),
        nullable=False
    )

    size_id = Column(
        Integer,
        ForeignKey("sizes.id"),
        nullable=False
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    unit = Column(
        String,
        nullable=False
    )

    # Relationships
    menu_item = relationship(
        "MenuItem",
        back_populates="recipes"
    )

    size = relationship(
        "Size",
        back_populates="recipes"
    )

    ingredient = relationship(
        "Ingredient",
        back_populates="recipes"
    )

    # Prevent duplicate ingredient
    # in the same pasta + size
    __table_args__ = (
        UniqueConstraint(
            "menu_item_id",
            "size_id",
            "ingredient_id",
            name="unique_recipe_ingredient"
        ),
    )
class StockTransaction(Base):

    __tablename__ = "stock_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False
    )

    transaction_type = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    unit = Column(
        String,
        nullable=False
    )

    reference = Column(
        String,
        nullable=True
    )

    notes = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    ingredient = relationship(
        "Ingredient"
    )
class Order(Base):

    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.id"),
        nullable=False
    )

    size_id = Column(
        Integer,
        ForeignKey("sizes.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    total_cost = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    menu_item = relationship(
        "MenuItem"
    )

    size = relationship(
        "Size"
    )    
class Purchase(Base):

    __tablename__ = "purchases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=True
    )

    total_cost = Column(
        Float,
        nullable=True
    )

    supplier = Column(
        String,
        nullable=True
    )

    notes = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    ingredient = relationship(
        "Ingredient"
    )    