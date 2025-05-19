
from fastapi import APIRouter, Depends
from database import get_db
from models import Product

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
async def register_product(product: Product, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute(
            """INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)""",
            (product.name, product.category, product.price, product.stock)
        )
    return {"message": "Product registered successfully"}