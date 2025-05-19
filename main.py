from fastapi import FastAPI
from routes import products, inventory, sales

app = FastAPI(title="E-commerce Admin API")

app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(sales.router)