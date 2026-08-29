import streamlit as st

from database.database import SessionLocal
from database.models import Ingredient
from services.inventory_service import remove_stock
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)

st.title("🗑️ Wastage")

st.subheader("Record Wastage")

db = SessionLocal()

ingredients = db.query(
    Ingredient
).filter(
    Ingredient.is_active == True
).order_by(
    Ingredient.name
).all()

if not ingredients:
    st.warning("No ingredients found.")
    db.close()
    st.stop()

ingredient_options = {
    ingredient.name: ingredient
    for ingredient in ingredients
}

selected_name = st.selectbox(
    "Ingredient",
    list(ingredient_options.keys())
)

ingredient = ingredient_options[selected_name]

# Current stock
from services.inventory_service import get_current_stock

current_stock = get_current_stock(
    db,
    ingredient.id
)

st.info(
    f"Current Stock: {current_stock:g} {ingredient.unit}"
)

quantity = st.number_input(
    f"Wasted Quantity ({ingredient.unit})",
    min_value=0.0,
    max_value=float(current_stock),
    step=0.1
)

reason = st.selectbox(
    "Reason",
    [
        "Expired",
        "Spoilage",
        "Damaged",
        "Cooking Loss",
        "Other"
    ]
)

notes = st.text_area(
    "Notes"
)

if st.button(
    "🗑️ Record Wastage",
    use_container_width=True
):

    try:

        remove_stock(
            ingredient_id=ingredient.id,
            quantity=quantity,
            transaction_type="WASTAGE",
            reference=reason,
            notes=notes
        )

        st.success(
            f"{quantity:g} {ingredient.unit} "
            f"of {ingredient.name} recorded as wastage."
        )

        st.rerun()

    except Exception as e:

        st.error(str(e))

db.close()