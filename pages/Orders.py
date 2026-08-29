import streamlit as st

from database.database import SessionLocal
from database.models import MenuItem, Size

from services.order_capacity_service import (
    calculate_pasta_capacity,
    get_all_pasta_capacity,
    simulate_order,
    place_order
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)


st.title("🍝 Orders & Pasta Capacity")

st.write(
    "Check production capacity, simulate orders, "
    "or place actual customer orders."
)


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

db.close()


if not menu_items or not sizes:

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
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Capacity",
        "🧪 Order Simulation",
        "🛒 Actual Order"
    ]
)


# =========================================================
# TAB 1 — CAPACITY
# =========================================================

with tab1:

    st.subheader("📊 Check Specific Pasta Capacity")

    col1, col2 = st.columns(2)

    with col1:

        selected_menu = st.selectbox(
            "Select Pasta",
            list(menu_options.keys()),
            key="capacity_pasta"
        )

    with col2:

        selected_size = st.selectbox(
            "Select Size",
            list(size_options.keys()),
            key="capacity_size"
        )

    if st.button(
        "🔍 Check Available Orders",
        use_container_width=True,
        key="capacity_button"
    ):

        menu_item = menu_options[selected_menu]
        size = size_options[selected_size]

        result = calculate_pasta_capacity(
            menu_item_id=menu_item.id,
            size_id=size.id
        )

        if not result:

            st.error(
                "Recipe not found for this pasta and size."
            )

        else:

            st.success(
                f"You can currently make "
                f"**{result['maximum_orders']} "
                f"{selected_size} "
                f"{selected_menu}**."
            )

            st.subheader("⚠️ Limiting Ingredient")

            st.warning(
                f"{result['limiting_ingredient']} "
                f"is currently limiting production."
            )

            st.subheader("Ingredient Capacity")

            for item in result["details"]:

                st.write(
                    f"**{item['ingredient']}** — "
                    f"{item['possible_orders']} orders"
                )

                st.caption(
                    f"Available: "
                    f"{item['available']:g} "
                    f"{item['unit']} | "
                    f"Required/order: "
                    f"{item['required']:g} "
                    f"{item['unit']}"
                )


    # -----------------------------------------------------
    # COMPLETE CAPACITY TABLE
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "📋 Current Pasta Production Capacity"
    )

    capacity_data = get_all_pasta_capacity()

    if capacity_data:

        st.dataframe(
            capacity_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No recipe or inventory data available."
        )


# =========================================================
# TAB 2 — SIMULATION
# =========================================================

with tab2:

    st.subheader("🧪 Simulate an Order")

    st.info(
        "Simulation does NOT change your inventory. "
        "It only checks what would happen."
    )

    col1, col2 = st.columns(2)

    with col1:

        sim_pasta = st.selectbox(
            "Select Pasta",
            list(menu_options.keys()),
            key="simulation_pasta"
        )

    with col2:

        sim_size = st.selectbox(
            "Select Size",
            list(size_options.keys()),
            key="simulation_size"
        )

    sim_quantity = st.number_input(
        "Order Quantity",
        min_value=1,
        step=1,
        value=1,
        key="simulation_quantity"
    )

    if st.button(
        "🧪 Simulate Order",
        use_container_width=True,
        key="simulation_button"
    ):

        menu_item = menu_options[sim_pasta]
        size = size_options[sim_size]

        try:

            result = simulate_order(
                menu_item_id=menu_item.id,
                size_id=size.id,
                order_quantity=sim_quantity
            )

            if result["can_make"]:

                st.success(
                    f"✅ Yes! You can make "
                    f"{sim_quantity} "
                    f"{sim_size} "
                    f"{sim_pasta}."
                )

            else:

                st.error(
                    f"❌ You cannot make "
                    f"{sim_quantity} "
                    f"{sim_size} "
                    f"{sim_pasta}."
                )

            st.subheader(
                "Inventory Impact Simulation"
            )

            simulation_rows = []

            for item in result["details"]:

                simulation_rows.append({

                    "Ingredient":
                        item["ingredient"],

                    "Current Stock":
                        item["current_stock"],

                    "Required":
                        item["required"],

                    "Remaining After Order":
                        item["remaining"],

                    "Unit":
                        item["unit"],

                    "Available":
                        "YES"
                        if item["available"]
                        else "NO"
                })

            st.dataframe(
                simulation_rows,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "⚠️ This is only a simulation. "
                "Inventory has NOT been changed."
            )

        except Exception as e:

            st.error(str(e))


# =========================================================
# TAB 3 — ACTUAL ORDER
# =========================================================

with tab3:

    st.subheader("🛒 Place Actual Order")

    st.warning(
        "⚠️ Actual orders will reduce ingredient inventory."
    )

    col1, col2 = st.columns(2)

    with col1:

        actual_pasta = st.selectbox(
            "Select Pasta",
            list(menu_options.keys()),
            key="actual_pasta"
        )

    with col2:

        actual_size = st.selectbox(
            "Select Size",
            list(size_options.keys()),
            key="actual_size"
        )

    actual_quantity = st.number_input(
        "Order Quantity",
        min_value=1,
        step=1,
        value=1,
        key="actual_quantity"
    )

    st.write(
        f"**Order:** "
        f"{actual_quantity} × "
        f"{actual_size} "
        f"{actual_pasta}"
    )

    if st.button(
        "🛒 Place Actual Order",
        use_container_width=True,
        key="actual_order_button"
    ):

        menu_item = menu_options[actual_pasta]
        size = size_options[actual_size]

        try:

            result = place_order(
                menu_item_id=menu_item.id,
                size_id=size.id,
                order_quantity=actual_quantity
            )

            st.success(
                f"✅ Order #{result['order_id']} "
                f"placed successfully!"
            )

            st.write(
                f"**{result['quantity']} × "
                f"{result['size']} "
                f"{result['menu_item']}**"
            )

            st.write(
                f"Total ingredient cost: "
                f"**PKR {result['total_cost']:,.2f}**"
            )

            st.subheader(
                "📦 Inventory Used"
            )

            stock_rows = []

            for item in result["stock_changes"]:

                stock_rows.append({
                    "Ingredient":
                        item["ingredient"],

                    "Used":
                        item["used"],

                    "Unit":
                        item["unit"]
                })

            st.dataframe(
                stock_rows,
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "Inventory has been automatically "
                "decreased."
            )

        except Exception as e:

            st.error(str(e))