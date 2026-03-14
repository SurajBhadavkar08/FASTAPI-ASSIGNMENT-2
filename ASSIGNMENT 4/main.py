from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

cart = []
orders = []
order_id_counter = 1

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

def calculate_total(product, quantity):
    return product["price"] * quantity

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int):
    product = find_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    if not product["in_stock"]:
        raise HTTPException(
            status_code=400,
            detail=f"{product['name']} is out of stock"
        )
        
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])
            return {"message": "Cart updated", "cart_item": item}
            
    # Add new item
    item = {
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": calculate_total(product, quantity)
    }
    cart.append(item)
    return {"message": "Added to cart", "cart_item": item}

@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}
        
    grand_total = sum(item["subtotal"] for item in cart)
    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    for i, item in enumerate(cart):
        if item["product_id"] == product_id:
            cart.pop(i)
            return {"message": f"Product id {product_id} removed from cart"}
    raise HTTPException(status_code=404, detail="Item not found in cart")

@app.post("/cart/checkout")
def checkout(request: CheckoutRequest):
    global order_id_counter
    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty — add items first"
        )
        
    grand_total = sum(item["subtotal"] for item in cart)
    orders_placed = []
    
    for item in cart:
        order = {
            "order_id": order_id_counter,
            "customer_name": request.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "subtotal": item["subtotal"],
            "delivery_address": request.delivery_address
        }
        orders.append(order)
        orders_placed.append(order)
        order_id_counter += 1
        
    cart.clear()
    
    return {
        "message": "Checkout successful",
        "orders_placed": orders_placed,
        "grand_total": grand_total
    }

@app.get("/orders")
def get_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }
