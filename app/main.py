from fastapi import FastAPI

from app.api import orders, products

app = FastAPI(title="Inventory & Order Management")

app.include_router(products.router)
app.include_router(orders.router)
