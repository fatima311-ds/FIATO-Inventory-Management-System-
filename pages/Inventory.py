import streamlit as st

from services.inventory_service import (
    get_all_current_stock,
    get_stock_status
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)

st.title("📦 Inventory")

stock_data = get_all_current_stock()

if not stock_data:
    st.info("No inventory data available.")
else:

    rows = []

    for item in stock_data:

        status = get_stock_status(
            item["current_stock"],
            item["minimum_level"]
        )

        rows.append({
            "Ingredient": item["name"],
            "Current Stock": item["current_stock"],
            "Unit": item["unit"],
            "Minimum Level": item["minimum_level"],
            "Rate (PKR)": item["rate"],
            "Status": status
        })

    st.dataframe(
        rows,
        use_container_width=True
    )