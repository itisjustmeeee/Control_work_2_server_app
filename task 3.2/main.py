from fastapi import FastAPI, Query
from typing import List, Dict, Any, Optional

app = FastAPI()

product_bd = {
    123: {"name": "Smartphone", "category": "Electronics", "price": 599.99},
    456: {"name": "Phone Case", "category": "Accessories", "price": 19.99},
    789: {"name": "Iphone", "category": "Electronics", "price": 1299.99},
    101: {"name": "Headphones", "category": "Accessories", "price": 99.99},
    202: {"name": "Smartwatch", "category": "Electronics", "price": 299.99}
}

@app.get('/product/{product_id}')
async def get_product_by_id(search_product_id: int):
    if search_product_id in product_bd:
        return product_bd[search_product_id]
    return {"error": "пользователь не найден"}

@app.get('/products/search')
async def search_product(
    keyword: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(10, ge = 1, le = 100)):
    results: List[Dict[str, Any]] = []

    for product in product_bd.values():
        if category is not None and product["category"] != category:
            continue

        if keyword is not None:
            if keyword.lower() not in product["name"].lower():
                continue

        results.append(product)

        if len(results) >= limit:
            break
    return results