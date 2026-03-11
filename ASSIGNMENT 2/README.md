# FastAPI — Day 2 Assignment

This repository contains the implementation for the **FastAPI Day 2 Practice Tasks**. It builds upon the Day 1 e-commerce application by adding advanced features like query parameters, path variables, Pydantic validation, and data manipulation logic.

## 🚀 How to Run the App

1. Open your terminal and navigate to the `ASSIGNMENT 2` folder.
2. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser and go to the Swagger UI to test the endpoints:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📂 Detailed Code Breakdown

Here is a detailed explanation of what each endpoint in `main.py` does.

### Products Data Structure
The app uses an in-memory `products` list.
```python
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]
```

### 1️⃣ Q1: Filter Products by Minimum Price
**Endpoint:** `GET /products/filter`
- **What it does:** Allows users to filter products by category, maximum price, and **minimum price**.
- **How it works:** Uses `Optional` query parameters (`category`, `max_price`, `min_price`). It filters the `products` list returning only products that meet *all* provided conditions. For example, if `min_price=400` is passed, it only returns items priced 400 or above.

### 2️⃣ Q2: Get Only the Price of a Product
**Endpoint:** `GET /products/{product_id}/price`
- **What it does:** Returns a lightweight response containing only the `name` and `price` of a specific product.
- **How it works:** It uses `{product_id}` as a **path parameter**. The function loops through the products list. If the `id` matches, it returns a new dictionary with just the name and price. If the loop finishes without finding the product, it returns a `{"error": "Product not found"}` message.

### 3️⃣ Q3: Accept Customer Feedback
**Endpoint:** `POST /feedback`
- **What it does:** Allows users to submit a product review.
- **Pydantic Model:** Uses a `CustomerFeedback` model to validate incoming JSON.
  - `customer_name`: Must be at least 2 characters.
  - `product_id`: Must be greater than 0.
  - `rating`: Must be between 1 and 5.
  - `comment`: Optional string.
- **How it works:** If the data passes validation, it appends the feedback to a global `feedback` list and returns a success message along with the total feedback count.

### 4️⃣ Q4: Build a Product Summary Dashboard
**Endpoint:** `GET /products/summary`
- **What it does:** Returns a single dashboard-style JSON object containing statistics about the entire store.
- **How it works:** 
  - Uses basic Python list comprehensions to count `in_stock` and `out_of_stock` items.
  - Uses Python's built in `max()` and `min()` functions with standard lambda functions to find the most expensive and cheapest products based on the `price` key.
  - Extracts unique categories using `set()` and converts them back to a list.

### 5️⃣ Q5: Validate & Place a Bulk Order
**Endpoint:** `POST /orders/bulk`
- **What it does:** Allows a corporate client to order multiple items at once. Calculates the subtotal and checks stock availability for each item.
- **Pydantic Model:** Uses a `BulkOrder` model which contains a list of nested `OrderItem` models.
  - `OrderItem` ensures the product ID is valid and the quantity is between 1 and 50.
  - `BulkOrder` ensures valid company email and name.
- **How it works:** Loops through each requested `OrderItem`. It attempts to find the corresponding product in the database.
  - **Failures:** If the product doesn't exist or `in_stock` is false, it gets added to a `failed` list with a reason.
  - **Successes:** If valid, it multiplies price by quantity to get a `subtotal`, adds that to `grand_total`, and appends the item to the `confirmed` list.
- **Return:** Returns a mix of both confirmed and failed items in a single response, allowing partial fulfillment.

### ⭐ BONUS: Order Status Tracker
**Endpoints:** `POST /orders`, `GET /orders/{order_id}`, `PATCH /orders/{order_id}/confirm`
- **What it does:** Introduces an order fulfillment workflow.
- **How it works:**
  - `POST /orders`: Creates a new order. The status is intentionally set to `"pending"` initially.
  - `GET /orders/{order_id}`: Retrieves the order state using the path parameter.
  - `PATCH /orders/{order_id}/confirm`: Finds the specific order, updates its `status` field from `"pending"` to `"confirmed"`, and returns the updated order data.
