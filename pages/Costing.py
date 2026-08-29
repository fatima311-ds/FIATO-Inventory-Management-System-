import streamlit as st

from database.database import SessionLocal
from database.models import MenuItem, Size

from services.costing_service import (
    calculate_recipe_cost
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)


st.title("💰 Costing")

st.caption(
    "Calculate ingredient cost, packaging cost, selling price "
    "and estimated profit."
)


# =========================================================
# SESSION STATE
# =========================================================

if "costing_result" not in st.session_state:
    st.session_state.costing_result = None


if "costing_menu_id" not in st.session_state:
    st.session_state.costing_menu_id = None


if "costing_size_id" not in st.session_state:
    st.session_state.costing_size_id = None


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()

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


if not menu_items or not sizes:

    db.close()

    st.warning(
        "Menu items or sizes are not configured."
    )

    st.stop()


menu_options = {
    item.name: item
    for item in menu_items
}

size_options = {
    size.name: size
    for size in sizes
}


# =========================================================
# SELECT PASTA + SIZE
# =========================================================

col1, col2 = st.columns(2)

with col1:

    selected_menu = st.selectbox(
        "🍝 Select Pasta",
        list(menu_options.keys()),
        key="costing_pasta"
    )

with col2:

    selected_size = st.selectbox(
        "📦 Select Size",
        list(size_options.keys()),
        key="costing_size"
    )


menu_item = menu_options[selected_menu]
size = size_options[selected_size]


# =========================================================
# CHECK IF SELECTION CHANGED
# =========================================================

if (
    st.session_state.costing_menu_id != menu_item.id
    or
    st.session_state.costing_size_id != size.id
):

    st.session_state.costing_result = None

    st.session_state.costing_menu_id = menu_item.id

    st.session_state.costing_size_id = size.id


# =========================================================
# CALCULATE BUTTON
# =========================================================

if st.button(
    "🧮 Calculate Cost",
    use_container_width=True
):

    result = calculate_recipe_cost(
        menu_item_id=menu_item.id,
        size_id=size.id
    )

    if not result:

        st.error(
            "No recipe found for this pasta and size."
        )

        st.session_state.costing_result = None

    else:

        st.session_state.costing_result = result

        st.session_state.costing_menu_id = menu_item.id

        st.session_state.costing_size_id = size.id


# =========================================================
# SHOW COSTING
# =========================================================

result = st.session_state.costing_result


if result:

    st.divider()

    st.subheader(
        f"🍝 {selected_menu} — {selected_size}"
    )


    # =====================================================
    # INGREDIENT TABLE
    # =====================================================

    rows = []

    missing_rates = []

    for item in result["details"]:

        if item["rate"] is None:

            missing_rates.append(
                item["ingredient"]
            )

            rows.append({
                "Ingredient": item["ingredient"],
                "Quantity": item["quantity"],
                "Unit": item["unit"],
                "Rate(Weighted Avg)": "Not Set",
                "Cost": "Not Set"
            })

        else:

            rows.append({
                "Ingredient": item["ingredient"],
                "Quantity": item["quantity"],
                "Unit": item["unit"],
                "Rate(Weighted Avg)": round(
                    item["rate"],
                    4
                ),
                "Cost": round(
                    item["cost"],
                    2
                )
            })


    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # INGREDIENT COST
    # =====================================================

    ingredient_cost = (
        result["total_ingredient_cost"]
    )


    st.metric(
        "🥘 Total Ingredient Cost",
        f"PKR {ingredient_cost:,.2f}"
    )


    # =====================================================
    # PACKAGING
    # =====================================================

    st.subheader("📦 Packaging")

    packaging_cost = st.number_input(
        "Packaging Cost (PKR)",
        min_value=0.0,
        value=50.0,
        step=1.0,
        key="costing_packaging"
    )


    # =====================================================
    # TOTAL COST
    # =====================================================

    total_cost = (
        ingredient_cost +
        packaging_cost
    )


    st.metric(
        "💰 Total Cost",
        f"PKR {total_cost:,.2f}"
    )


    # =====================================================
    # SELLING PRICE
    # =====================================================

    st.subheader("🏷️ Selling Price")

    selling_price = st.number_input(
        "Enter Selling Price (PKR)",
        min_value=0.0,
        step=10.0,
        value=0.0,
        key="costing_selling_price"
    )


    # =====================================================
    # PROFIT + MARGIN
    # =====================================================

    if selling_price > 0:

        profit = (
            selling_price -
            total_cost
        )

        gross_margin = (
            profit /
            selling_price
        ) * 100


        st.divider()

        st.subheader("📊 Profit Analysis")


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "💵 Profit per Order",
                f"PKR {profit:,.2f}"
            )


        with col2:

            st.metric(
                "📈 Gross Margin",
                f"{gross_margin:.2f}%"
            )


        # =================================================
        # PROFIT STATUS
        # =================================================

        if profit > 0:

            st.success(
                f"✅ This selling price gives a profit of "
                f"PKR {profit:,.2f} per pasta."
            )

        elif profit == 0:

            st.warning(
                "⚠️ Selling price is equal to total cost. "
                "There is no profit."
            )

        else:

            st.error(
                f"❌ This selling price results in a loss of "
                f"PKR {abs(profit):,.2f} per pasta."
            )


    # =====================================================
    # MISSING RATES
    # =====================================================

    if missing_rates:

        st.warning(
            "⚠️ Rate is missing for: "
            + ", ".join(missing_rates)
        )


db.close()