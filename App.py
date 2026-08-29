import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="FIATO Inventory Management",
    page_icon="🍝",
    layout="wide"
)

# =========================================================
# FIATO BRANDING
# =========================================================

logo_path = Path("assets/fiato_logo.png.jpeg")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    if logo_path.exists():
        st.image(
            str(logo_path),
            width=150
        )

    st.markdown(
        "<h1 style='text-align:center;'>FIATO Inventory Management System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Inventory Management • Recipe Costing • Stock Monitoring"
        "</p>",
        unsafe_allow_html=True
    )
#st.title("🍝 FIATO Inventory Management System")

#st.write(
  #  "Inventory Management • Recipe Costing • Stock Monitoring"
#)

st.success("FIATO system is running successfully!") 

st.logo("assets/fiato_logo.png.jpeg", size="large")
with st.sidebar:

    st.markdown("---")

    st.caption("FIATO Inventory Management")