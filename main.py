import os
import sqlite3
import csv
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from validator import validate_products
from ebay_formatter import fetch_draft_products, generate_inventory_payload

# Initialize SQLite database on startup
init_db()

app = FastAPI(title="eBay Automation Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "API active. Place index.html in directory to load dashboard."}

@app.get("/api/products")
def get_products():
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"products": products}

@app.post("/api/import-csv")
async def import_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    
    conn = sqlite3.connect("catalog.db")
    cursor = conn.cursor()
    imported_count = 0
    
    for row in reader:
        cursor.execute("""
            INSERT OR REPLACE INTO products (sku, title, description, price, quantity, image_url, status)
            VALUES (?, ?, ?, ?, ?, ?, 'draft')
        """, (
            row.get('sku'),
            row.get('title'),
            row.get('description', ''),
            float(row.get('price', 0)),
            int(row.get('quantity', 1)),
            row.get('image_url', '')
        ))
        imported_count += 1
        
    conn.commit()
    conn.close()
    return {"message": f"Successfully imported {imported_count} products."}

@app.post("/api/validate")
def run_validation():
    results = validate_products()
    return {"status": "completed", "results": results}

@app.get("/api/payload/{sku}")
def get_ebay_payload(sku: str):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        raise HTTPException(status_code=404, detail="SKU not found")
        
    payload = generate_inventory_payload(dict(product))
    return {"sku": sku, "ebay_payload": payload}