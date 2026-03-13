from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

app = FastAPI()

# -------------------------
# Products (Day 1)
# -------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 120, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 999, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1499, "category": "Electronics", "in_stock": False}
]

# -------------------------
# Feedback & Orders Storage
# -------------------------
feedback = []
orders = []
order_counter = 1

# -------------------------
# DAY 1 ENDPOINTS
# -------------------------
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    filtered = [p for p in products if p["category"].lower() == category_name.lower()]
    if not filtered:
        return {"error": "No products found in this category"}
    return filtered

@app.get("/products/instock")
def instock_products():
    in_stock_items = [p for p in products if p["in_stock"]]
    return {"in_stock_products": in_stock_items, "count": len(in_stock_items)}

@app.get("/store/summary")
def store_summary():
    total = len(products)
    in_stock = len([p for p in products if p["in_stock"]])
    out_stock = total - in_stock
    categories = list(set(p["category"] for p in products))
    return {
        "store_name": "My E-commerce Store",
        "total_products": total,
        "in_stock": in_stock,
        "out_of_stock": out_stock,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    if not result:
        return {"message": "No products matched your search"}
    return {"matched_products": result, "count": len(result)}

@app.get("/products/deals")
def best_deals():
    cheapest = min(products, key=lambda x: x["price"])
    expensive = max(products, key=lambda x: x["price"])
    return {"best_deal": cheapest, "premium_pick": expensive}

# -------------------------
# DAY 2 ENDPOINTS
# -------------------------

# Q1: Filter products by category and min/max price
@app.get("/products/filter")
def filter_products(category: Optional[str] = None,
                    min_price: Optional[int] = None,
                    max_price: Optional[int] = None):
    result = products
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    return {"filtered_products": result, "count": len(result)}

# Q2: Return only product name and price
@app.get("/products/{product_id}/price")
def product_price(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"name": product["name"], "price": product["price"]}

# Q3: Customer feedback POST with validation
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

@app.post("/feedback")
def submit_feedback(fb: CustomerFeedback):
    feedback.append(fb.dict())
    return {
        "message": "Feedback submitted successfully",
        "feedback": fb,
        "total_feedback": len(feedback)
    }

# Q4: Product summary dashboard
@app.get("/products/summary")
def products_summary():
    total_products = len(products)
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = total_products - in_stock_count
    cheapest = min(products, key=lambda x: x["price"])
    most_expensive = max(products, key=lambda x: x["price"])
    categories = list(set(p["category"] for p in products))
    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]},
        "most_expensive": {"name": most_expensive["name"], "price": most_expensive["price"]},
        "categories": categories
    }

# Q5: Bulk order POST with validation
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: EmailStr
    items: List[OrderItem] = Field(..., min_items=1)

@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):
    global order_counter
    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
            continue
        if not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
            continue
        subtotal = product["price"] * item.quantity
        confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
        grand_total += subtotal

    orders.append({
        "order_id": order_counter,
        "company": order.company_name,
        "contact_email": order.contact_email,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total,
        "status": "pending"
    })

    order_counter += 1

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# Bonus: PATCH order to confirm
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["status"] = "confirmed"
    return {"order_id": order_id, "status": "confirmed"}

# Bonus: GET single order by ID
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order