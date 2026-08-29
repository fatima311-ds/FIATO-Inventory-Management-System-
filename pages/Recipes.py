import streamlit as st

from database.database import SessionLocal
from database.models import (
    Recipe,
    MenuItem,
    Size,
    Ingredient
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)

st.title("🍝 Recipe Management")

st.caption(
    "Manage FIATO pasta recipes for Regular and Large sizes."
)


# =========================================================
# DATABASE
# =========================================================

db = SessionLocal()


# =========================================================
# LOAD DATA
# =========================================================

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


ingredients = db.query(
    Ingredient
).filter(
    Ingredient.is_active == True
).order_by(
    Ingredient.name
).all()


if not menu_items or not sizes or not ingredients:

    st.warning(
        "Menu items, sizes or ingredients are not configured."
    )

    db.close()
    st.stop()


# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs([
    "📋 View Recipes",
    "✏️ Manage Recipe"
])


# =========================================================
# TAB 1 — VIEW RECIPES
# =========================================================

with tab1:

    st.subheader("📋 Current Recipes")

    recipes = db.query(
        Recipe
    ).order_by(
        Recipe.menu_item_id,
        Recipe.size_id,
        Recipe.ingredient_id
    ).all()


    rows = []

    for recipe in recipes:

        rows.append({
            "Pasta": recipe.menu_item.name,
            "Size": recipe.size.name,
            "Ingredient": recipe.ingredient.name,
            "Quantity": recipe.quantity,
            "Unit": recipe.unit
        })


    if rows:

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No recipes found."
        )


# =========================================================
# TAB 2 — MANAGE RECIPE
# =========================================================

with tab2:

    st.subheader("✏️ Add / Update Recipe Ingredient")


    menu_options = {
        item.name: item
        for item in menu_items
    }

    size_options = {
        size.name: size
        for size in sizes
    }

    ingredient_options = {
        ingredient.name: ingredient
        for ingredient in ingredients
    }


    # -----------------------------------------------------
    # SELECT PASTA
    # -----------------------------------------------------

    selected_menu = st.selectbox(
        "🍝 Pasta",
        list(menu_options.keys()),
        key="recipe_menu"
    )


    # -----------------------------------------------------
    # SELECT SIZE
    # -----------------------------------------------------

    selected_size = st.selectbox(
        "📦 Size",
        list(size_options.keys()),
        key="recipe_size"
    )


    # -----------------------------------------------------
    # SELECT INGREDIENT
    # -----------------------------------------------------

    selected_ingredient = st.selectbox(
        "🥘 Ingredient",
        list(ingredient_options.keys()),
        key="recipe_ingredient"
    )


    menu_item = menu_options[selected_menu]
    size = size_options[selected_size]
    ingredient = ingredient_options[selected_ingredient]


    # -----------------------------------------------------
    # FIND EXISTING RECIPE
    # -----------------------------------------------------

    existing_recipe = db.query(
        Recipe
    ).filter(
        Recipe.menu_item_id == menu_item.id,
        Recipe.size_id == size.id,
        Recipe.ingredient_id == ingredient.id
    ).first()


    if existing_recipe:

        st.info(
            f"Existing quantity: "
            f"{existing_recipe.quantity:g} "
            f"{existing_recipe.unit}"
        )

        default_quantity = float(
            existing_recipe.quantity
        )

    else:

        st.info(
            "This ingredient is not currently "
            "in this recipe."
        )

        default_quantity = 0.0


    # -----------------------------------------------------
    # QUANTITY
    # -----------------------------------------------------

    quantity = st.number_input(
        "Quantity",
        min_value=0.0,
        value=default_quantity,
        step=0.01,
        format="%.3f"
    )


    # -----------------------------------------------------
    # UNIT
    # -----------------------------------------------------

    unit = ingredient.unit


    st.info(
        f"Ingredient base unit: {unit}"
    )


    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    if st.button(
        "💾 Save Recipe",
        use_container_width=True
    ):

        try:

            if quantity <= 0:

                st.error(
                    "Quantity must be greater than zero."
                )

            else:

                if existing_recipe:

                    # UPDATE
                    existing_recipe.quantity = quantity
                    existing_recipe.unit = unit

                    message = (
                        "Recipe ingredient updated successfully."
                    )

                else:

                    # ADD NEW
                    new_recipe = Recipe(
                        menu_item_id=menu_item.id,
                        size_id=size.id,
                        ingredient_id=ingredient.id,
                        quantity=quantity,
                        unit=unit
                    )

                    db.add(new_recipe)

                    message = (
                        "Recipe ingredient added successfully."
                    )


                db.commit()

                st.success(
                    f"✅ {message}"
                )

                st.rerun()


        except Exception as e:

            db.rollback()

            st.error(
                f"Unable to save recipe: {e}"
            )


# =========================================================
# CLOSE DATABASE
# =========================================================

db.close()