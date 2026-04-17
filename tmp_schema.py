import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db_connection import get_connection

def dump_schema():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print("=== Database Schema ===")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]} ({col[1]})")
            
    cursor.close()
    conn.close()

if __name__ == "__main__":
    dump_schema()
