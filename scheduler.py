import sqlite3
import time
from datetime import datetime
from ebay_formatter import fetch_draft_products, generate_inventory_payload

def process_pending_drafts():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    drafts = fetch_draft_products()
    
    if not drafts:
        print(f"[{timestamp}] No pending draft products found.")
        return

    print(f"[{timestamp}] Found {len(drafts)} draft(s) to process.")
    
    for product in drafts:
        payload = generate_inventory_payload(product)
        print(f" -> Queueing SKU '{product['sku']}' for release.")
        
        # Mark item as 'ready' in SQLite database
        conn = sqlite3.connect("catalog.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET status = 'ready' WHERE sku = ?", (product['sku'],))
        conn.commit()
        conn.close()

def run_scheduler(interval_seconds=15):
    print(f"Local listing scheduler active (checking every {interval_seconds} seconds). Press Ctrl+C to stop.\n")
    try:
        while True:
            process_pending_drafts()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

if __name__ == "__main__":
    run_scheduler()