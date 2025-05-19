import asyncio
import aiomysql

products = [
    ("Echo Dot", "Electronics", 49.99, 100),
    ("Organic Shampoo", "Beauty", 12.49, 50),
    ("Gaming Mouse", "Electronics", 29.99, 80)
]

async def seed():
    conn = await aiomysql.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        db="ecommerce_db",
        autocommit=True
    )
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM products")
        await cursor.executemany(
            "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)",
            products
        )
    await conn.ensure_closed()

asyncio.run(seed())