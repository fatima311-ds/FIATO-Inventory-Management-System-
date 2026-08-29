import streamlit as st

from database.database import SessionLocal
from services.inventory_service import get_current_stock
from database.models import (
    Ingredient,
    MenuItem,
    Size
)
from pathlib import Path

st.logo(
    "assets/fiato_logo.png.jpeg",
    size="large"
)

# =========================================================
# PAGE HEADER
# =========================================================

st.title("⚙️ System Settings")

st.caption(
    "Manage ingredients, menu items, serving sizes, "
    "and inventory configuration."
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🥕 Ingredients",
        "🍝 Menu Items",
        "📏 Sizes",
        "ℹ️ System Info"
    ]
)


# =========================================================
# INGREDIENTS
# =========================================================

with tab1:

    st.subheader("🥕 Ingredient Management")

    db = SessionLocal()

    ingredients = db.query(
        Ingredient
    ).order_by(
        Ingredient.name
    ).all()

    db.close()

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Ingredients",
            len(ingredients)
        )

    with col2:

        active_count = sum(
            1
            for item in ingredients
            if item.is_active
        )

        st.metric(
            "Active",
            active_count
        )

    with col3:

        inactive_count = sum(
            1
            for item in ingredients
            if not item.is_active
        )

        st.metric(
            "Inactive",
            inactive_count
        )

    st.divider()

    # -----------------------------------------------------
    # ADD INGREDIENT
    # -----------------------------------------------------

    st.subheader("➕ Add Ingredient")

    with st.form("add_ingredient_form"):

        col1, col2 = st.columns(2)

        with col1:

            ingredient_name = st.text_input(
                "Ingredient Name"
            )

        with col2:

            unit = st.selectbox(
                "Base Unit",
                [
                    "g",
                    "ml",
                    "pcs"
                ]
            )

        col1, col2 = st.columns(2)

        with col1:

            rate = st.number_input(
                "Rate per Base Unit (PKR)",
                min_value=0.0,
                step=0.01
            )

        with col2:

            minimum_level = st.number_input(
                "Minimum Stock Level",
                min_value=0.0,
                step=1.0
            )

        add_ingredient = st.form_submit_button(
            "➕ Add Ingredient",
            use_container_width=True
        )

    if add_ingredient:

        name = ingredient_name.strip()

        if not name:

            st.error(
                "Ingredient name is required."
            )

        else:

            db = SessionLocal()

            try:

                existing = db.query(
                    Ingredient
                ).filter(
                    Ingredient.name == name
                ).first()

                if existing:

                    st.error(
                        "An ingredient with this "
                        "name already exists."
                    )

                else:

                    ingredient = Ingredient(

                        name=name,

                        unit=unit,

                        rate=rate,

                        minimum_level=
                            minimum_level,

                        current_stock=0,

                        is_active=True
                    )

                    db.add(ingredient)
                    db.commit()

                    st.success(
                        f"✅ {name} added successfully!"
                    )

                    st.rerun()

            except Exception as e:

                db.rollback()

                st.error(
                    f"Error: {e}"
                )

            finally:

                db.close()

    st.divider()

    # -----------------------------------------------------
    # MANAGE INGREDIENT
    # -----------------------------------------------------

    st.subheader("✏️ Manage Ingredients")

    if ingredients:

        ingredient_options = {
            item.name: item.id
            for item in ingredients
        }

        selected_name = st.selectbox(
            "Select Ingredient",
            list(ingredient_options.keys()),
            key="settings_ingredient"
        )

        selected_id = ingredient_options[
            selected_name
        ]

        db = SessionLocal()

        ingredient = db.query(
            Ingredient
        ).filter(
            Ingredient.id == selected_id
        ).first()

        db.close()

        if ingredient:

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Base Unit",
                    ingredient.unit
                )
            with col2:

                db_stock = SessionLocal()

                current_stock = get_current_stock(
                    db_stock,
                    ingredient.id
                )

                db_stock.close()

                st.metric(
                    "Current Stock",
                    f"{current_stock:g} "
                    f"{ingredient.unit}"
                )
            
            with col3:

                st.metric(
                    "Status",
                    "Active"
                    if ingredient.is_active
                    else "Inactive"
                )

            with st.form("edit_ingredient_form"):

                new_rate = st.number_input(
                    "Rate per Base Unit",
                    min_value=0.0,
                    value=float(
                        ingredient.rate or 0
                    ),
                    step=0.01
                )

                new_minimum = st.number_input(
                    "Minimum Stock Level",
                    min_value=0.0,
                    value=float(
                        ingredient.minimum_level or 0
                    ),
                    step=1.0
                )

                new_active = st.checkbox(
                    "Ingredient is Active",
                    value=bool(
                        ingredient.is_active
                    )
                )

                save_ingredient = st.form_submit_button(
                    "💾 Save Changes",
                    use_container_width=True
                )

            if save_ingredient:

                db = SessionLocal()

                try:

                    item = db.query(
                        Ingredient
                    ).filter(
                        Ingredient.id ==
                        selected_id
                    ).first()

                    item.rate = new_rate

                    item.minimum_level = (
                        new_minimum
                    )

                    item.is_active = (
                        new_active
                    )

                    db.commit()

                    st.success(
                        "✅ Ingredient settings updated!"
                    )

                    st.rerun()

                except Exception as e:

                    db.rollback()

                    st.error(
                        f"Error: {e}"
                    )

                finally:

                    db.close()

    # -----------------------------------------------------
    # INGREDIENT TABLE
    # -----------------------------------------------------

    st.divider()

    rows = []

    for item in ingredients:

        rows.append({

            "Ingredient":
                item.name,

            "Unit":
                item.unit,

            "Rate":
                item.rate,

            "Minimum Level":
                item.minimum_level,

            "Status":
                "Active"
                if item.is_active
                else "Inactive"

        })

    if rows:

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# MENU ITEMS
# =========================================================

with tab2:

    st.subheader("🍝 Menu Item Management")

    db = SessionLocal()

    menu_items = db.query(
        MenuItem
    ).order_by(
        MenuItem.name
    ).all()

    db.close()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Menu Items",
            len(menu_items)
        )

    with col2:

        st.metric(
            "Active Menu Items",
            sum(
                1
                for item in menu_items
                if item.is_active
            )
        )

    st.divider()

    # -----------------------------------------------------
    # ADD MENU ITEM
    # -----------------------------------------------------

    st.subheader("➕ Add Menu Item")

    with st.form("add_menu_item_form"):

        menu_name = st.text_input(
            "Pasta Name"
        )

        description = st.text_area(
            "Description",
            placeholder=
            "Example: Creamy Alfredo pasta "
            "with chicken and herbs."
        )

        add_menu = st.form_submit_button(
            "➕ Add Menu Item",
            use_container_width=True
        )

    if add_menu:

        name = menu_name.strip()

        if not name:

            st.error(
                "Pasta name is required."
            )

        else:

            db = SessionLocal()

            try:

                existing = db.query(
                    MenuItem
                ).filter(
                    MenuItem.name == name
                ).first()

                if existing:

                    st.error(
                        "This menu item already exists."
                    )

                else:

                    item = MenuItem(
                        name=name,
                        description=
                            description.strip()
                            or None,
                        is_active=True
                    )

                    db.add(item)
                    db.commit()

                    st.success(
                        f"✅ {name} added successfully!"
                    )

                    st.rerun()

            except Exception as e:

                db.rollback()

                st.error(
                    f"Error: {e}"
                )

            finally:

                db.close()

    st.divider()

    # -----------------------------------------------------
    # MANAGE MENU ITEM
    # -----------------------------------------------------

    st.subheader("✏️ Manage Menu Items")

    if menu_items:

        menu_options = {
            item.name: item.id
            for item in menu_items
        }

        selected_menu_name = st.selectbox(
            "Select Menu Item",
            list(menu_options.keys()),
            key="settings_menu"
        )

        selected_menu_id = menu_options[
            selected_menu_name
        ]

        db = SessionLocal()

        menu_item = db.query(
            MenuItem
        ).filter(
            MenuItem.id ==
            selected_menu_id
        ).first()

        db.close()

        if menu_item:

            with st.form("edit_menu_form"):

                new_description = st.text_area(
                    "Description",
                    value=
                    menu_item.description or ""
                )

                new_active = st.checkbox(
                    "Menu Item is Active",
                    value=bool(
                        menu_item.is_active
                    )
                )

                save_menu = st.form_submit_button(
                    "💾 Save Changes",
                    use_container_width=True
                )

            if save_menu:

                db = SessionLocal()

                try:

                    item = db.query(
                        MenuItem
                    ).filter(
                        MenuItem.id ==
                        selected_menu_id
                    ).first()

                    item.description = (
                        new_description.strip()
                        or None
                    )

                    item.is_active = new_active

                    db.commit()

                    st.success(
                        "✅ Menu item updated!"
                    )

                    st.rerun()

                except Exception as e:

                    db.rollback()

                    st.error(
                        f"Error: {e}"
                    )

                finally:

                    db.close()

    # -----------------------------------------------------
    # MENU TABLE
    # -----------------------------------------------------

    st.divider()

    rows = []

    for item in menu_items:

        rows.append({

            "Pasta":
                item.name,

            "Description":
                item.description or "-",

            "Status":
                "Active"
                if item.is_active
                else "Inactive"

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# SIZES
# =========================================================

with tab3:

    st.subheader("📏 Size Management")

    db = SessionLocal()

    sizes = db.query(
        Size
    ).order_by(
        Size.volume_ml
    ).all()

    db.close()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Sizes",
            len(sizes)
        )

    with col2:

        largest_volume = max(
            [s.volume_ml for s in sizes],
            default=0
        )

        st.metric(
             "Largest Volume",
             f"{largest_volume} ml"
        )
        

    st.divider()

    # -----------------------------------------------------
    # ADD SIZE
    # -----------------------------------------------------

    st.subheader("➕ Add Size")

    with st.form("add_size_form"):

        size_name = st.text_input(
            "Size Name",
            placeholder="Example: Regular"
        )

        volume_ml = st.number_input(
            "Container Volume (ml)",
            min_value=1,
            value=700,
            step=50
        )

        multiplier = st.number_input(
            "Recipe Multiplier",
            min_value=0.01,
            value=1.0,
            step=0.05
        )

        add_size = st.form_submit_button(
            "➕ Add Size",
            use_container_width=True
        )

    if add_size:

        name = size_name.strip()

        if not name:

            st.error(
                "Size name is required."
            )

        else:

            db = SessionLocal()

            try:

                existing = db.query(
                    Size
                ).filter(
                    Size.name == name
                ).first()

                if existing:

                    st.error(
                        "This size already exists."
                    )

                else:

                    size = Size(

                        name=name,

                        volume_ml=volume_ml,

                        multiplier=multiplier
                    )

                    db.add(size)
                    db.commit()

                    st.success(
                        f"✅ {name} size added!"
                    )

                    st.rerun()

            except Exception as e:

                db.rollback()

                st.error(
                    f"Error: {e}"
                )

            finally:

                db.close()

    st.divider()

    # -----------------------------------------------------
    # MANAGE SIZE
    # -----------------------------------------------------

    st.subheader("✏️ Manage Sizes")

    if sizes:

        size_options = {
            size.name: size.id
            for size in sizes
        }

        selected_size_name = st.selectbox(
            "Select Size",
            list(size_options.keys()),
            key="settings_size"
        )

        selected_size_id = size_options[
            selected_size_name
        ]

        db = SessionLocal()

        selected_size = db.query(
            Size
        ).filter(
            Size.id ==
            selected_size_id
        ).first()

        db.close()

        if selected_size:

            with st.form("edit_size_form"):

                new_volume = st.number_input(
                    "Container Volume (ml)",
                    min_value=1,
                    value=int(
                        selected_size.volume_ml
                    ),
                    step=50
                )

                new_multiplier = st.number_input(
                    "Recipe Multiplier",
                    min_value=0.01,
                    value=float(
                        selected_size.multiplier
                    ),
                    step=0.05
                )

                save_size = st.form_submit_button(
                    "💾 Save Size",
                    use_container_width=True
                )

            if save_size:

                db = SessionLocal()

                try:

                    size = db.query(
                        Size
                    ).filter(
                        Size.id ==
                        selected_size_id
                    ).first()

                    size.volume_ml = new_volume

                    size.multiplier = (
                        new_multiplier
                    )

                    db.commit()

                    st.success(
                        "✅ Size updated successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    db.rollback()

                    st.error(
                        f"Error: {e}"
                    )

                finally:

                    db.close()

    # -----------------------------------------------------
    # SIZE TABLE
    # -----------------------------------------------------

    st.divider()

    rows = []

    for size in sizes:

        rows.append({

            "Size":
                size.name,

            "Volume":
                f"{size.volume_ml} ml",

            "Recipe Multiplier":
                size.multiplier

        })

    if rows:

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# SYSTEM INFO
# =========================================================

with tab4:

    st.subheader("ℹ️ FIATO Inventory System")

    st.info(
        """
        **FIATO Inventory Management System**

        This system manages:

        • Ingredient inventory  
        • Purchases  
        • Stock transactions  
        • Pasta recipes  
        • Menu items  
        • Serving sizes  
        • Order capacity  
        • Actual orders  
        • Wastage  
        • Recipe costing  
        • Stock monitoring
        """
    )

    st.divider()

    st.subheader("🔄 How the System Works")

    st.markdown(
        """
        **1. Ingredients**

        Ingredients define the basic stock units and rates.

        **2. Recipes**

        Recipes define how much of each ingredient
        is required for one pasta serving.

        **3. Purchases**

        Purchases increase inventory.

        **4. Actual Orders**

        Orders consume ingredients according
        to the recipe.

        **5. Wastage**

        Wastage removes unused/damaged stock.

        **6. Capacity**
        Capacity calculates how much pasta orders 
                                     can be produced from 
                            current inventory.         
                                     """
                             )   
    st.success(
        "System configuration is ready."
    )