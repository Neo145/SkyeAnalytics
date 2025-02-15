# F:\SkyeAnalytics\db_test.py
import psycopg2
from dotenv import load_dotenv
import os

def test_connection():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname="skye_analytics",
            user="postgres",
            password="skye",  # The new password we just set
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM test_connection")
        rows = cur.fetchall()
        
        for row in rows:
            print(f"ID: {row[0]}, Data: {row[1]}")
        
        cur.close()
        conn.close()
        print("Database connection test successful!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()