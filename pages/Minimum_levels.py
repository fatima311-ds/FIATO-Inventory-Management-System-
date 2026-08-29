import streamlit as st

from database.database import SessionLocal
from database.models import Ingredient
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)
st.title("⚙️ Minimum Stock Levels")

db = SessionLocal()

ingredients = db.query(
    Ingredient
).filter(
    Ingredient.is_active == True
).all()

for ingredient in ingredients:

    new_level = st.number_input(
        ingredient.name,
        min_value=0.0,
        value=float(ingredient.minimum_level),
        key=f"min_{ingredient.id}"
    )

    if st.button(
        f"Save {ingredient.name}",
        key=f"save_{ingredient.id}"
    ):

        ingredient.minimum_level = new_level

        db.commit()

        st.success(
            f"Minimum level updated for {ingredient.name}"
        )

db.close()