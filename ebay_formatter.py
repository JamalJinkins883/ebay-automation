import sqlite3

def fetch_draft_products():
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE status = 'draft'")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def generate_inventory_payload(product):
    return {
        "sku": product["sku"],
        "product": {
            "title": product["title"],
            "description": product["description"],
            "imageUrls": [product["image_url"]] if product["image_url"] else []
        },
        "availability": {
            "shipToLocationAvailability": {
                "quantity": product["quantity"]
            }
        }
    }