# FastAPI - Day 4 Assignment

This directory contains the code for the **FastAPI Day 4 Assignment**, which focuses on building and interacting with CRUD (Create, Read, Update, Delete) APIs.

## 🚀 How to Run

1. Open your terminal and navigate to this directory (`ASSIGNMENT 3`).
2. Run the FastAPI application using the following command:
   ```bash
   uvicorn main:app --reload
   ```
   *Alternatively, you can run `python -m uvicorn main:app --reload`*
3. Open your browser and go to the **Swagger UI** for testing:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📋 Features Implemented

The application manages a mock inventory of products and provides endpoints to modify them. Here are the tasks that were accomplished:

### Q1: Add New Products (POST)
- **Endpoint**: `POST /products`
- **Description**: Adds new products to the inventory. Validates to ensure duplicate products (by name) return a `400 Bad Request`.
- **Action Performed**: Added `Laptop Stand` and `Sticky Notes`.

### Q2: Restock and Update Products (PUT)
- **Endpoint**: `PUT /products/{product_id}`
- **Description**: Updates specific fields (`price` and `in_stock` status) for an existing product.
- **Action Performed**: Updated the USB Hub (ID: 3) to be in stock and updated its price simultaneously.

### Q3: Delete a Product (DELETE)
- **Endpoint**: `DELETE /products/{product_id}`
- **Description**: Removes a product from the inventory permanently. Handles cases gracefully where a non-existent ID yields a `404 Not Found` error.
- **Action Performed**: Removed the `Pen Set` (ID: 4).

### Q4: Full CRUD Sequence
- Demonstrated the entire lifecycle of a product:
  1. **POST**: Added a `Smart Watch`.
  2. **GET**: Retrieved the new auto-generated ID.
  3. **PUT**: Corrected a pricing error.
  4. **GET**: Verified the price change.
  5. **DELETE**: Removed the product after the launch got cancelled.

### Q5: Inventory Audit (GET)
- **Endpoint**: `GET /products/audit`
- **Description**: Generates an inventory summary dashboard containing:
  - Total number of products
  - Breakdown of in-stock items
  - Names of out-of-stock items
  - The total value of all in-stock inventory (simulating 10 units each)
  - The most expensive product details

### ⭐ Bonus: Category-Wide Discount (PUT)
- **Endpoint**: `PUT /products/discount`
- **Description**: Applies a percentage discount to all products belonging to a specific category simultaneously.
- **Action Performed**: Slashed prices across all `Electronics` dynamically.

---

## 🛠 Project Structure

- `main.py` - Contains the full FastAPI app and the CRUD endpoints.
- `Assignmnet3_FASTAPI_DAY4.html` - The original assignment instruction file.
- `*.png` - Output and test screenshots confirming endpoint successes on Swagger UI.
