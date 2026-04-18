# Sales Intelligence Hub - Project Documentation

## 1. Project Overview
The **Sales Intelligence Hub** is a professional-grade Business Intelligence (BI) dashboard and multi-branch sales management system. It is designed to help businesses centralize their sales data, track branch performance, and manage customer payments with ease.

### Key Objectives
- **Centralized Management**: Manage sales across multiple branches from a single interface.
- **Real-time Analytics**: Gain instant insights into revenue, collection rates, and product performance.
- **Role-based Access**: Ensure data security with separate access levels for Super Admins and Branch Admins.
- **Payment Tracking**: Track partial payments and automate balance calculations.

---

## 2. Technical Architecture
The project follows a modular architecture separating the data layer, logic layer, and presentation layer.

- **Frontend**: [Streamlit](https://streamlit.io/) (Python-based web framework)
- **Backend/Logic**: Python (Pandas for data processing, MySQL Connector)
- **Database**: MySQL (Relational database for structured data)
- **Visualizations**: Plotly Express & Plotly Graph Objects
- **Exports**: FPDF (PDF), Pandas (CSV, Excel, JSON)

### Component Diagram
1. **`dashboard/streamlit_app.py`**: The entry point of the application. Handles UI rendering, session state, and user interactions.
2. **`app/queries.py`**: Contains all SQL-based business logic and data retrieval functions.
3. **`app/db_connection.py`**: Manages the MySQL connection pool and credentials.
4. **`database/`**: Contains SQL scripts for schema initialization, sample data, and triggers.
5. **`import_dataset.py`**: A utility script to seed the database from CSV files.

---

## 3. Database Design
The system uses a normalized relational schema to ensure data integrity.

### Tables
- **`branches`**: Stores branch details (Name, Admin Name).
- **`users`**: Manages authentication and roles (Super Admin vs Admin).
- **`customer_sales`**: The core table for sale records, includes generated columns for `pending_amount`.
- **`payment_splits`**: Stores individual payment transactions linked to a specific sale.

### Automation (Triggers)
The database includes a trigger `update_received_amount` that automatically updates the `received_amount` in the `customer_sales` table whenever a new entry is added to `payment_splits`.

---

## 4. Features & Functionality

### 🔐 Multi-level Authentication
- **Super Admin**: Full visibility into all branches, access to global analytics, and the ability to run custom SQL queries.
- **Branch Admin**: Access restricted to their specific branch's sales and analytics.

### 📊 Executive Dashboard
- **KPI Cards**: Real-time tracking of Total Sales, Total Received, Pending Amount, Collection Rate, and Average Order Value.
- **Dynamic Charts**: Interactive Sales Revenue Trends, Branch Breakdowns, Product Mix, and Payment Channel analysis.

### 📝 Sales Management
- **Add New Sale**: Comprehensive form to record customer details, product, and initial payment.
- **Interactive Sales Table**: Powered by `st.data_editor`, allowing direct inline editing and deletion of records with automatic database syncing.
- **Export Suite**: Download filtered sales data in CSV, Excel, JSON, or professional PDF formats.

### 💳 Payment Tracking
- Search for existing sales by ID.
- Record incremental payments.
- Automatic status switching (Open/Close) based on payment completion.

---

## 5. Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- `npm` (if using any frontend tools, though this is primarily Python)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd "Sales Intelligent Hub"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup
1. Open your MySQL client (e.g., MySQL Workbench or CLI).
2. Execute the scripts in order:
   - `database/schema.sql` (Creates DB and Tables)
   - `database/triggers.sql` (Sets up automation)
   - `database/sample_data.sql` (Optional: Adds initial data)

### Step 4: Configure Database Connection
Edit `app/db_connection.py` with your MySQL credentials:
```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="guvi_sms"
    )
```

---

## 6. How to Use

### Data Import
If you have CSV datasets ready, run the import script to seed the database:
```bash
python import_dataset.py
```

### Running the App
Start the Streamlit dashboard:
```bash
streamlit run dashboard/streamlit_app.py
```

---

## 7. Folder Structure
```text
├── .streamlit/             # Streamlit configuration
├── app/
│   ├── db_connection.py    # Database connection logic
│   ├── queries.py          # SQL Query logic
├── dashboard/
│   ├── streamlit_app.py    # Main UI script
├── database/
│   ├── schema.sql          # DB Schema definition
│   ├── triggers.sql        # DB Triggers
├── Sales Management System Datasets/ # Raw CSV data
├── documentation.md        # Full project documentation
├── import_dataset.py       # Data Seeding script
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
```

---

## 8. Developer Notes
- **Styling**: The UI uses custom CSS injected via `inject_dashboard_css()` using the Inter font family and a Modern/Minimalist aesthetic.
- **Adding Queries**: New analytics should be added to `app/queries.py` and then called within the `render_overview` or other render functions in `streamlit_app.py`.
- **Security**: Password hashing is recommended for production (currently uses plain text for demonstration/local use).
