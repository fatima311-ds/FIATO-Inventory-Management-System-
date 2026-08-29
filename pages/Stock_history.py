import streamlit as st
import pandas as pd
from database.database import SessionLocal
from database.models import Purchase, Ingredient
from services.stock_history_service import get_stock_history
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)


st.title("📜 Stock History")

history = get_stock_history()

if not history:

    st.info(
        "No stock transactions yet."
    )

else:

    df = pd.DataFrame(history)

    # Format date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"]
        ).dt.strftime(
            "%Y-%m-%d %H:%M"
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

