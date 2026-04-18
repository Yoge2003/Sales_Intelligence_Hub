# Sales Intelligence Hub - Project Documentation

## 1. Abstract
In the modern business landscape, managing sales operations across multiple branches presents significant challenges, including fragmented data, delayed reporting, and inconsistencies in payment tracking. The **Sales Intelligence Hub** is a comprehensive Business Intelligence (BI) and management solution designed to bridge these gaps. Developed using **Python**, **Streamlit**, and **MySQL**, the system provides a centralized platform for real-time sales monitoring, automated financial tracking, and granular branch management.

The project features a multi-tiered **Role-Based Access Control (RBAC)** system, allowing Super Admins to oversee global performance while providing Branch Admins with localized management tools. Key functionalities include an **Executive Dashboard** with interactive Key Performance Indicators (KPIs), dynamic data visualizations for trend analysis, and a specialized **Payment Tracking System** that automates balance calculations through database-level triggers. 

By integrating robust data processing with a high-performance, responsive user interface, the Sales Intelligence Hub transforms raw sales data into actionable business insights. The system not only streamlines administrative workflows but also enhances decision-making accuracy, improves collection efficiency, and provides a scalable foundation for growing retail and service-oriented enterprises.

---

## 2. Declaration
I hereby declare that the project titled **"Sales Intelligence Hub"** is a genuine work carried out by me. This project was developed to provide an integrated solution for multi-branch sales management and business intelligence. 

I further declare that the code, database design, and documentation submitted herewith are my original work, and to the best of my knowledge, it has not been submitted previously for the award of any degree, diploma, or other similar titles in any other University or Institution.

All resources, libraries, and external tools used during the development of this project have been appropriately acknowledged and used in accordance with their respective licenses.

<br>

**Station:** [Your City/Location]  
**Date:** [Current Date]

<br>

**[Your Name]**  
[Your Registration Number/Roll No]  
[Department Name]  
[Institution Name]

---

## 3. Introduction
In today’s data-driven business environment, the ability to monitor and analyze sales performance in real-time is no longer a luxury but a necessity for sustainable growth. Organizations with multiple branches often struggle with "data silos," where information is scattered across different locations, making it difficult for management to get a unified view of the business. The **Sales Intelligence Hub** was developed to address these specific challenges by providing a centralized, high-performance Business Intelligence (BI) dashboard.

#### **Purpose and Scope**
The primary goal of this project is to create a seamless interface where sales transactions, customer data, and payment histories from various branches are consolidated into a single MySQL database. By leveraging **Streamlit** for the frontend and **Python** for the analytical backend, the system offers an intuitive way to track Key Performance Indicators (KPIs) such as total revenue, collection efficiency, and product-wise sales distribution. 

The scope of the project extends beyond simple data entry; it includes:
- **Financial Integrity**: Ensuring accurate balance tracking through automated database triggers.
- **Strategic Insights**: Providing visual trends that help managers identify peak sales periods and best-selling products.
- **Operational Efficiency**: Streamlining the payment recording process to reduce manual errors and overhead.

#### **Value Proposition**
By transforming raw transactional data into meaningful visual analytics, the Sales Intelligence Hub empowers business owners to make informed, data-backed decisions. Whether it is identifying underperforming branches, managing pending customer collections, or optimizing inventory based on sales trends, this tool serves as a "command center" for modern sales management.

---

## 4. Project Overview
The **Sales Intelligence Hub** is a professional-grade Business Intelligence (BI) dashboard and multi-branch sales management system. It is designed to help businesses centralize their sales data, track branch performance, and manage customer payments with ease.

### Key Objectives
- **Centralized Management**: Manage sales across multiple branches from a single interface.
- **Real-time Analytics**: Gain instant insights into revenue, collection rate, and product performance.
- **Role-based Access**: Ensure data security with separate access levels for Super Admins and Branch Admins.
- **Payment Tracking**: Track partial payments and automate balance calculations.

---

## 5. System Requirements
To ensure the **Sales Intelligence Hub** runs efficiently, the following minimum hardware and software configurations are required:

#### **1. Software Requirements**
- **Operating System**: Windows 10/11, macOS, or any Linux distribution.
- **Python Version**: Python 3.8 or higher.
- **Database**: MySQL Server 8.0 or higher.
- **Web Browser**: Google Chrome, Mozilla Firefox, or Microsoft Edge (Latest versions).
- **Libraries**: Streamlit, Pandas, Plotly, MySQL-Connector.

#### **2. Hardware Requirements**
- **Processor**: Dual-Core 2.0GHz or higher (Intel Core i3 / AMD Ryzen 3 minimum).
- **Memory (RAM)**: 4.0 GB minimum (8.0 GB recommended for optimal performance).
- **Disk Space**: At least 500 MB of free space (for application code and local database storage).
- **Internet Connectivity**: Required for the initial installation of Python libraries.

---

## 6. Technologies Used
The system is built using a modern open-source technology stack focused on performance and scalability:

- **Python**: The core programming language used for all business logic, data processing, and integration.
- **Streamlit**: A powerful Python framework used to build the interactive web dashboard and user interface.
- **MySQL**: A robust relational database management system (RDBMS) used for secure and organized data storage.
- **Pandas**: A high-performance library used for data manipulation, cleaning, and transformation.
- **Plotly**: Used to create interactive, professional-grade charts and data visualizations.
- **Custom CSS**: Integrated into Streamlit for a premium, modern design aesthetic.
- **MySQL Connector**: Facilitates seamless communication between the Python application and the MySQL database.
- **FPDF**: A specialized library used to generate professional PDF sales reports.

---

## 7. Technical Architecture
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

## 8. Folder Structure
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

## 9. Database Design
The system uses a normalized relational schema to ensure data integrity.

### Tables
- **`branches`**: Stores branch details (Name, Admin Name).
- **`users`**: Manages authentication and roles (Super Admin vs Admin).
- **`customer_sales`**: The core table for sale records, includes generated columns for `pending_amount`.
- **`payment_splits`**: Stores individual payment transactions linked to a specific sale.

### Automation (Triggers)
The database includes a trigger `update_received_amount` that automatically updates the `received_amount` in the `customer_sales` table whenever a new entry is added to `payment_splits`.

---

## 10. About Datasets
The **Sales Intelligence Hub** relies on four primary datasets that work together to manage sales and branch performance. These datasets are initially stored in CSV format and then imported into the MySQL database:

1.  **Branches Dataset**: Includes a list of all physical branch locations along with their names and assigned managers.
2.  **Users Dataset**: Contains login credentials, email addresses, and access levels (Super Admin or Branch Admin).
3.  **Customer Sales Dataset**: Tracks every transaction, including customer names, products, total sale amounts, and current status (Open/Closed).
4.  **Payment Splits Dataset**: A detailed history of all payments made toward specific sales, supporting tracking of partial payments and remaining balances.

---

## 11. Features & Functionality

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

## 12. Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server

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

## 13. How to Use

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

## 14. Developer Notes
- **Styling**: The UI uses custom CSS injected via `inject_dashboard_css()` using the Inter font family and a Modern/Minimalist aesthetic.
- **Adding Queries**: New analytics should be added to `app/queries.py` and then called within the `render_overview` or other render functions in `streamlit_app.py`.
- **Security**: Password hashing is recommended for production (currently uses plain text for demonstration/local use).

---

## 15. Future Enhancements
The **Sales Intelligence Hub** is designed with scalability in mind. Future versions of the system could include:

1.  **Predictive Analytics**: Using Machine Learning models to forecast future sales trends and revenue based on historical data.
2.  **Inventory Management Integration**: Connecting sales data to real-time stock levels for automated restocking alerts.
3.  **Advanced Security**: Implementing Two-Factor Authentication (2FA) and password hashing for enterprise-grade protection.
4.  **Mobile Companion App**: Developing a lightweight mobile application for managers to track KPIs and receive alerts on the go.
5.  **Automated Notifications**: Setting up email or WhatsApp alerts for weekly summaries and pending payment reminders.
6.  **AI Chatbot**: Integrating an AI-powered assistant for natural language querying of sales performance.
7.  **Cloud Deployment**: Migrating to a cloud-native platform (AWS/GCP/Azure) to ensure global 24/7 availability.
