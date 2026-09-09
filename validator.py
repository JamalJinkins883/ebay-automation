import sqlite3

def validate_products():
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE status = 'draft'")
    products = cursor.fetchall()
    
    validation_results = {"valid": [], "invalid": []}
    
    for prod in products:
        sku = prod['sku']
        title = prod['title']
        price = prod['price']
        qty = prod['quantity']
        issues = []
        
        if not title or len(title.strip()) == 0:
            issues.append("Title is required.")
        elif len(title) > 80:
            issues.append(f"Title exceeds 80-character limit ({len(title)} chars).")
            
        if price is None or price <= 0:
            issues.append(f"Invalid price (${price}). Must be greater than 0.")
            
        if qty is None or qty < 1:
            issues.append(f"Invalid quantity ({qty}). Must be at least 1.")
            
        if issues:
            validation_results["invalid"].append({"sku": sku, "issues": issues})
            cursor.execute("UPDATE products SET status = 'invalid' WHERE sku = ?", (sku,))
        else:
            validation_results["valid"].append(sku)
            
    conn.commit()
    conn.close()
    return validation_results

if __name__ == "__main__":
    print(validate_products())