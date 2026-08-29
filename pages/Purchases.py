import streamlit as st

from database.database import SessionLocal

from database.models import (
    Ingredient,
    Purchase
)

from services.inventory_service import (
    add_purchase,
    delete_purchase
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)

if "purchase_success" not in st.session_state:
    st.session_state.purchase_success = False


st.title("🛒 Purchases")

st.subheader("Add New Purchase")

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
       list(ingredient_options.keys()),
        key="purchase_ingredient"
    )
    

with st.form("purchase_form",enter_to_submit=False):

    ingredient = ingredient_options[selected_name]
    st.info(
    f"Base Unit: {ingredient.unit}"
    )

    col1, col2 = st.columns(2)

    with col1:
        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            step=1.0,
            key="purchase_quantity"
        )

    with col2:
        if ingredient.unit == "g":
            purchase_units = ["g", "kg"]
        elif ingredient.unit == "ml":
            purchase_units = ["ml", "L"]
        else:
            purchase_units = [ingredient.unit]

        purchase_unit = st.selectbox(
            "Purchase Unit",
            purchase_units,
            key="purchase_unit"
        )
    unit_price = st.number_input(
    "Unit Purchase Price (PKR)",
    min_value=0.0,
    step=1.0,
    key="purchase_unit_price"
)

    total_cost = st.number_input(
    "Total Purchase Cost (PKR)",
    min_value=0.0,
    step=1.0,
    key="purchase_cost"
)

    supplier = st.text_input(
        "Supplier (Optional)",
        key="purchase_supplier"
    )

    notes = st.text_area(
        "Notes (Optional)",
        key="purchase_notes"
    )

    submitted = st.form_submit_button(
        "➕ Add Purchase"
    )    
if submitted:
    try:

        purchase = add_purchase(
            db=db,
            ingredient_id=ingredient.id,
            quantity=quantity,
            unit=purchase_unit,
            unit_price=unit_price,
            total_cost=total_cost,
            supplier=supplier,
            notes=notes
        )

        st.session_state.purchase_success = True
        st.rerun()

    except Exception as e:

        st.error(str(e))
if st.session_state.purchase_success:
    st.success("✅ Purchase added successfully!")
    st.session_state.purchase_success = False    


db.close()
# =========================================================
# PURCHASE HISTORY
# =========================================================

st.divider()

st.header("📜 Purchase History")

db = SessionLocal()

purchases = db.query(
    Purchase
).order_by(
    Purchase.created_at.desc()
).all()

if not purchases:

    st.info("No purchases found.")

else:

    for purchase in purchases:

        ingredient_name = purchase.ingredient.name
        unit = purchase.ingredient.unit

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.subheader(
                    f"🛒 {ingredient_name}"
                )

                st.write(
                    f"**Purchase ID:** {purchase.id}"
                )

                st.write(
                    f"**Quantity:** "
                    f"{purchase.quantity:g} {unit}"
                )

                if purchase.total_cost is not None:
                    st.write(
                        f"**Total Cost:** "
                        f"PKR {purchase.total_cost:,.2f}"
                    )

                if purchase.supplier:
                    st.write(
                        f"**Supplier:** "
                        f"{purchase.supplier}"
                    )

                if purchase.created_at:
                    st.caption(
                        f"Date: {purchase.created_at}"
                    )

            with col2:

                st.write("")

                delete_button = st.button(
                    "🗑️ Delete",
                    key=f"delete_purchase_{purchase.id}",
                    use_container_width=True
                )

                if delete_button:

                    try:

                        delete_purchase(
                            purchase.id
                        )

                        st.success(
                            f"Purchase #{purchase.id} "
                            f"deleted successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(str(e))

db.close()