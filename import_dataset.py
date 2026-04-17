import os
import pandas as pd
import numpy as np
from app.db_connection import get_connection

def import_table(conn, table_name, csv_filename, columns=None):
    print(f"Importing {table_name}...")
    df = pd.read_csv(csv_filename)
    df = df.replace({np.nan: None})
    
    cursor = conn.cursor()
    if columns is None:
        columns = df.columns.tolist()
        
    cols = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
    
    values = [tuple(x) for x in df[columns].values]
    
    try:
        cursor.executemany(query, values)
        conn.commit()
        print(f"Successfully imported {len(df)} rows into {table_name}.")
    except Exception as e:
        print(f"Failed to import {table_name}: {e}")
        conn.rollback()
    finally:
        cursor.close()

def main():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Disabling foreign key checks...")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    
    print("Truncating tables...")
    cursor.execute("TRUNCATE TABLE payment_splits;")
    cursor.execute("TRUNCATE TABLE customer_sales;")
    cursor.execute("TRUNCATE TABLE users;")
    cursor.execute("TRUNCATE TABLE branches;")
    conn.commit()
    
    base_dir = "Sales Management System Datasets"
    
    import_table(conn, "branches", os.path.join(base_dir, "branches.csv"))
    import_table(conn, "users", os.path.join(base_dir, "users.csv"))
    import_table(conn, "customer_sales", os.path.join(base_dir, "customer_sales.csv"))
    import_table(conn, "payment_splits", os.path.join(base_dir, "payment_splits.csv"))
    
    print("Enabling foreign key checks...")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    conn.commit()
    cursor.close()
    conn.close()
    print("Import complete!")

if __name__ == "__main__":
    main()
