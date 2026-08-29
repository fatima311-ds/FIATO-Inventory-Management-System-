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

st.title("🚦 Stock Status")

data = get_all_current_stock()

for item in data:

    status = get_stock_status(
        item["current_stock"],
        item["minimum_level"]
    )

    if status == "OUT OF STOCK":
        st.error(
            f"🔴 {item['name']} — OUT OF STOCK"
        )

    elif status == "CRITICAL":
        st.warning(
            f"🟠 {item['name']} — CRITICAL"
        )

    elif status == "LOW STOCK":
        st.warning(
            f"🟡 {item['name']} — LOW STOCK"
        )

    else:
        st.success(
            f"🟢 {item['name']} — HEALTHY"
        )