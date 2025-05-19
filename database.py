import aiomysql
from fastapi import Request

async def get_db():
    conn = await aiomysql.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        db="ecommerce_db",
        autocommit=True
    )
    return conn