import pandas as pd
from app.db_connection import get_connection

def add_sale(branch_id, sale_date, name, mobile, product, gross_amount, received_amount, payment_method):
    conn = get_connection()
    cursor = conn.cursor()

    status = 'Close' if received_amount >= gross_amount else 'Open'

    query = """
    INSERT INTO customer_sales 
    (branch_id, date, name, mobile_number, product_name, gross_sales, received_amount, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (branch_id, sale_date, name, mobile, product, gross_amount, received_amount, status))
    sale_id = cursor.lastrowid

    if received_amount > 0:
        payment_query = """
        INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(payment_query, (sale_id, sale_date, received_amount, payment_method))

    conn.commit()
    cursor.close()
    conn.close()
    return sale_id

def get_sale_by_id(sale_id, user):
    conn = get_connection()
    query = """
        SELECT sale_id, branch_id, date, name, mobile_number, product_name, gross_sales, 
               received_amount, pending_amount, status 
        FROM customer_sales 
        WHERE sale_id = %s
    """
    params = [sale_id]
    
    if user["role"] != "super_admin":
        query += " AND branch_id = %s"
        params.append(user["branch_id"])
        
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def record_payment(sale_id, amount, method, payment_date):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Insert into payment_splits
    cursor.execute("""
        INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s)
    """, (sale_id, payment_date, amount, method))
    
    # 2. Update customer_sales received_amount
    cursor.execute("""
        UPDATE customer_sales 
        SET received_amount = received_amount + %s 
        WHERE sale_id = %s
    """, (amount, sale_id))
    
    # 3. Check for closure
    cursor.execute("SELECT gross_sales, received_amount FROM customer_sales WHERE sale_id = %s", (sale_id,))
    row = cursor.fetchone()
    if row and row[1] >= row[0]:
        cursor.execute("UPDATE customer_sales SET status = 'Close' WHERE sale_id = %s", (sale_id,))
        
    conn.commit()
    cursor.close()
    conn.close()

def get_sales(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("branch_id = %s")
        params.append(user["branch_id"])
        
    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("product_name = %s")
        params.append(product_filter)

    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    query = f"""
        SELECT sale_id, branch_id, date, name, mobile_number, product_name, gross_sales, 
               received_amount, pending_amount, status FROM customer_sales
        {where_stmt}
    """
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def get_branch_list():
    conn = get_connection()
    df = pd.read_sql("SELECT branch_id, branch_name FROM branches ORDER BY branch_name", conn)
    conn.close()
    return df.to_dict("records")

def get_branch_sales(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("c.branch_id = %s")
        params.append(user["branch_id"])
    
    if start_date:
        where_clauses.append("c.date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("c.date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("c.product_name = %s")
        params.append(product_filter)
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT b.branch_name, SUM(c.gross_sales) AS total_sales
    FROM customer_sales c
    JOIN branches b ON c.branch_id = b.branch_id
    {where_stmt}
    GROUP BY b.branch_name
    """
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT u.user_id, u.username, u.role, u.branch_id, b.branch_name
    FROM users u
    LEFT JOIN branches b ON u.branch_id = b.branch_id
    WHERE u.username=%s AND u.password=%s
    """
    cursor.execute(query, (username, password))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        role_str = str(row[2]).lower().replace(" ", "_")
        return {
            "id": row[0],
            "username": row[1],
            "role": role_str,
            "branch_id": row[3],
            "branch_name": row[4]
        }

    return None

def get_kpis(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    cursor = conn.cursor()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("branch_id = %s")
        params.append(user["branch_id"])
        
    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("product_name = %s")
        params.append(product_filter)
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT
        SUM(gross_sales),
        SUM(received_amount),
        SUM(pending_amount),
        COUNT(*)
    FROM customer_sales
    {where_stmt}
    """
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return tuple(value or 0 for value in result)
    return 0, 0, 0, 0

def get_payment_analysis(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("c.branch_id = %s")
        params.append(user["branch_id"])
        
    if start_date:
        where_clauses.append("p.payment_date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("p.payment_date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("c.product_name = %s")
        params.append(product_filter)
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT p.payment_method, SUM(p.amount_paid) AS total
    FROM payment_splits p
    JOIN customer_sales c ON p.sale_id = c.sale_id
    {where_stmt}
    GROUP BY p.payment_method
    """
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def update_sale(sale_id, update_data):
    if not update_data:
        return
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
    values = list(update_data.values())
    values.append(sale_id)
    query = f"UPDATE customer_sales SET {set_clause} WHERE sale_id = %s"
    cursor.execute(query, tuple(values))
    conn.commit()
    cursor.close()
    conn.close()

def delete_sale(sale_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payment_splits WHERE sale_id = %s", (sale_id,))
    cursor.execute("DELETE FROM customer_sales WHERE sale_id = %s", (sale_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_sales_trend(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("branch_id = %s")
        params.append(user["branch_id"])
        
    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("product_name = %s")
        params.append(product_filter)
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT date as sale_date, SUM(gross_sales) as daily_sales
    FROM customer_sales
    {where_stmt}
    GROUP BY date
    ORDER BY date
    """
    df = pd.read_sql(query, conn, params=params)
    
    if not df.empty:
        df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.strftime('%Y-%m-%d')
        
    conn.close()
    return df


def get_product_performance(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("branch_id = %s")
        params.append(user["branch_id"])
        
    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("product_name = %s")
        params.append(product_filter)
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT product_name, SUM(gross_sales) as total_sales, COUNT(*) as count
    FROM customer_sales
    {where_stmt}
    GROUP BY product_name
    ORDER BY total_sales DESC
    """
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def get_status_analysis(user, start_date=None, end_date=None, product_filter=None):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("branch_id = %s")
        params.append(user["branch_id"])
        
    if start_date:
        where_clauses.append("date >= %s")
        params.append(start_date)
    if end_date:
        where_clauses.append("date <= %s")
        params.append(end_date)
    if product_filter:
        where_clauses.append("product_name = %s")
        params.append(product_filter)
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT status, SUM(gross_sales) as total_value, COUNT(*) as count
    FROM customer_sales
    {where_stmt}
    GROUP BY status
    """
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def get_recent_activity(user, limit=5):
    conn = get_connection()
    where_clauses = []
    params = []

    if user["role"] != "super_admin":
        where_clauses.append("c.branch_id = %s")
        params.append(user["branch_id"])
        
    where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
    SELECT c.date, c.name as customer, c.product_name as product, c.gross_sales, b.branch_name
    FROM customer_sales c
    JOIN branches b ON c.branch_id = b.branch_id
    {where_stmt}
    ORDER BY c.date DESC, c.sale_id DESC
    LIMIT %s
    """
    params.append(limit)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def execute_custom_query(query_string):
    conn = get_connection()
    try:
        df = pd.read_sql(query_string, conn)
    except Exception as e:
        df = pd.DataFrame({'Error': [str(e)]})
    finally:
        conn.close()
    return df