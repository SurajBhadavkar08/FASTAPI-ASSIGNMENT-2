from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 499},
    {"id": 2, "name": "USB Hub", "category": "Electronics", "price": 799},
    {"id": 3, "name": "Pen Set", "category": "Stationery", "price": 49},
    {"id": 4, "name": "Notebook", "category": "Stationery", "price": 99}
]

orders = []

@app.get('/products/search')
def search_products(keyword: str = Query(...)):
    results = [p for p in products if keyword.lower() in p['name'].lower()]
    if not results:
         return {"message": f"No products found for: {keyword}"}
    return {"keyword": keyword, "total_found": len(results), "products": results}

@app.get('/products/sort')
def sort_products(sort_by: str = Query('price'), order: str = Query('asc')):
    if sort_by not in ['price', 'name']:
        return {"error": "sort_by must be 'price' or 'name'"}
    reverse = (order == 'desc')
    result = sorted(products, key=lambda p: p[sort_by], reverse=reverse)
    return {"sort_by": sort_by, "order": order, "products": result}

@app.get('/products/page')
def paginate_products(page: int = Query(1, ge=1), limit: int = Query(2, ge=1)):
    start = (page - 1) * limit
    paged = products[start : start + limit]
    return {
        "page": page,
        "limit": limit,
        "total_pages": -(-len(products) // limit),
        "products": paged
    }

@app.post('/orders')
def create_order(order: dict):
    new_id = len(orders) + 1
    new_order = {"order_id": new_id, **order}
    orders.append(new_order)
    return new_order

# Q4
@app.get('/orders/search')
def search_orders(customer_name: str = Query(...)):
    results = [
        o for o in orders
        if customer_name.lower() in o.get('customer_name', '').lower()
    ]
    if not results:
        return {'message': f'No orders found for: {customer_name}'}
    return {'customer_name': customer_name, 'total_found': len(results), 'orders': results}

# Q5
@app.get('/products/sort-by-category')
def sort_by_category():
    result = sorted(products, key=lambda p: (p['category'], p['price']))
    return {'products': result, 'total': len(result)}

# Q6
@app.get('/products/browse')
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query('price'),
    order:   str = Query('asc'),
    page:    int = Query(1, ge=1),
    limit:   int = Query(4, ge=1, le=20),
):
    # Step 1: Search
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    # Step 2: Sort
    if sort_by in ['price', 'name']:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order=='desc'))

    # Step 3: Paginate
    total  = len(result)
    start  = (page - 1) * limit
    paged  = result[start : start + limit]

    return {
        'keyword':     keyword, 'sort_by': sort_by, 'order': order,
        'page': page,  'limit': limit, 'total_found': total,
        'total_pages': -(-total // limit) if limit else 0,
        'products':    paged,
    }

# Bonus
@app.get('/orders/page')
def get_orders_paged(
    page:  int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):
    start = (page - 1) * limit
    return {
        'page':        page,
        'limit':       limit,
        'total':       len(orders),
        'total_pages': -(-len(orders) // limit) if limit else 0,
        'orders':      orders[start : start + limit],
    }

@app.get('/products/{product_id}')
def get_product(product_id: int):
    for p in products:
        if p['id'] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")
