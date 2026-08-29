import streamlit as st

from services.dashboard_service import (
    get_inventory_summary,
    get_recent_stock_activity,
    get_order_summary,
    get_dashboard_capacity
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="FIATO Dashboard",
    page_icon="🍝",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🍝 FIATO Dashboard")

st.caption(
    "Real-time overview of inventory, stock health, "
    "orders and pasta production capacity."
)

st.divider()


# =========================================================
# GET DATA
# =========================================================

inventory = get_inventory_summary()

orders = get_order_summary()

capacity = get_dashboard_capacity()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📦 Total Inventory Items",
        inventory["total_items"]
    )

with col2:

    st.metric(
        "🟢 Healthy Stock",
        inventory["healthy"]
    )

with col3:

    st.metric(
        "⚠️ Low / Critical",
        inventory["low_stock"] + inventory["critical"]
    )

with col4:

    st.metric(
        "❌ Out of Stock",
        inventory["out_of_stock"]
    )


st.divider()


# =========================================================
# STOCK HEALTH
# =========================================================

st.subheader("📊 Stock Health")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Healthy",
        inventory["healthy"]
    )

with col2:
    st.metric(
        "Low Stock",
        inventory["low_stock"]
    )

with col3:
    st.metric(
        "Critical",
        inventory["critical"]
    )

with col4:
    st.metric(
        "Out of Stock",
        inventory["out_of_stock"]
    )

with col5:
    st.metric(
        "Not Set",
        inventory["not_set"]
    )


st.divider()


# =========================================================
# PASTA PRODUCTION CAPACITY
# =========================================================

st.subheader("🍝 Current Pasta Production Capacity")

st.caption(
    "Maximum number of Regular and Large pastas "
    "that can currently be prepared from available stock."
)

if capacity:

    st.dataframe(
        capacity,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No recipe or inventory data available."
    )


st.divider()


# =========================================================
# ORDER SUMMARY
# =========================================================

st.subheader("🧾 Order Summary")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Orders",
        orders["total_orders"]
    )

with col2:

    st.metric(
        "Total Pasta Quantity",
        orders["total_quantity"]
    )


st.divider()


# =========================================================
# RECENT STOCK ACTIVITY
# =========================================================

st.subheader("📋 Recent Stock Activity")

recent_activity = get_recent_stock_activity()

if recent_activity:

    st.dataframe(
        recent_activity,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No stock activity recorded yet."
    )


# =========================================================
# REFRESH
# =========================================================

st.divider()

if st.button(
    "🔄 Refresh Dashboard",
    use_container_width=True
):

    st.rerun()