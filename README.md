# FIATO Inventory Management System 🍝

A practical inventory management system built for FIATO Pastas to manage ingredients, recipes, stock, purchases, orders, and recipe costing in one place.

The system helps track inventory levels, monitor stock usage, calculate production capacity, and manage recipe-based costs through a simple Streamlit interface.

## 🚀 Features

- 📊 Inventory dashboard and stock monitoring
- 🧾 Ingredient and inventory management
- 💰 Recipe costing based on current ingredient rates
- 🍝 Editable recipes for different pasta sizes
- 📦 Packaging item management
- 🛒 Purchase and stock management
- 📋 Order management and production capacity
- ⚠️ Minimum stock level monitoring
- 📈 Stock history tracking
- 🗑️ Wastage tracking
- ⚙️ Settings for managing system data

## 🛠️ Tech Stack

- Python
- Streamlit
- SQLAlchemy
- SQLite
- Pandas

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/fatima311-ds/FIATO-Inventory-Management-System-.git
cd fiato-inventory-management-system
```
2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the virtual environment
```bash
Windows: 
venv\Scripts\
```

4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Run the application
```bash
streamlit run app.py
```
The application will open in your browser.

📂 Project Structure
```bash
fiato_inventory_system/
```bash
│
├── assets/          # Brand assets and logo
├── database/        # Database models and database configuration
├── pages/           # Streamlit application pages
├── services/        # Business logic and calculations
├── utils/           # Helper and validation functions
│
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md        # Project documentation
└── .gitignore       # Files excluded from Git
```
📈 Results

The system provides a centralized interface for:
Monitoring current inventory
Managing ingredient purchases
Updating recipes and ingredient quantities
Calculating recipe costs
Checking production capacity
Monitoring low-stock items
Tracking stock history and wastage

🧠 What I Learned
Building this project helped me strengthen my understanding of Python application development, database integration, Streamlit interfaces, inventory logic, recipe-based calculations, and organizing a complete project into reusable modules and services.

⭐ If you found this useful, consider giving it a star!



