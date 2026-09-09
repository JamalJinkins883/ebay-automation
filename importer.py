import csv
import sqlite3
from database import init_db

def import_csv_to_db(csv_file_path):
    init_db()
    conn = sqlite3.connect("catalog.db")
    cursor = conn.cursor()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT OR REPLACE INTO products (sku, title, description, price, quantity, image_url, status)
                VALUES (?, ?, ?, ?, ?, ?, 'draft')
            """, (
                row['sku'],
                row['title'],
                row['description'],
                float(row['price']),
                int(row['quantity']),
                row['image_url']
            ))
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_csv_to_db("products.csv")
    print("CSV imported successfully.")