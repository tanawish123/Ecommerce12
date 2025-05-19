
from fastapi import APIRouter, Depends, Query,HTTPException
from database import get_db
from typing import List
from schemas.inventory import InventoryChange,InventoryStatus
import aiomysql

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/")
async def get_inventory(db=Depends(get_db)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM products")
        products = await cursor.fetchall()
    return products

@router.get("/status/{product_id}", response_model=InventoryStatus)
async def get_inventory_status(product_id: int, db=Depends(get_db)):
    query = """
        SELECT stock, change_date 
        FROM inventory 
        WHERE product_id=%s AND change_type IS NULL
        LIMIT 1
    """
    async with db.cursor() as cursor:
        await cursor.execute(query, (product_id,))
        result = await cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Inventory status not found")
    return InventoryStatus(
        product_id=product_id,
        stock=result[0],
        last_updated=result[1]
    )


@router.get("/low-stock", response_model=List[InventoryStatus])
async def get_low_stock(threshold: int = Query(5, gt=0), db=Depends(get_db)):
    query = """
        SELECT product_id, stock, change_date 
        FROM inventory 
        WHERE change_type IS NULL AND stock < %s
    """
    async with db.cursor() as cursor:
        await cursor.execute(query, (threshold,))
        rows = await cursor.fetchall()
    return [InventoryStatus(product_id=r[0], stock=r[1], last_updated=r[2]) for r in rows]


@router.post("/update", status_code=201)
async def update_inventory(change: InventoryChange, db=Depends(get_db)):
    async with db.cursor() as cursor:
        # Get current stock
        await cursor.execute(
            "SELECT stock FROM inventory WHERE product_id=%s AND change_type IS NULL LIMIT 1",
            (change.product_id,)
        )
        current = await cursor.fetchone()
        current_stock = current[0] if current else 0

        # Calculate new stock depending on change type
        if change.change_type == "IN" or change.change_type == "ADJUSTMENT":
            new_stock = current_stock + change.quantity
        elif change.change_type == "OUT":
            new_stock = current_stock - change.quantity
            if new_stock < 0:
                raise HTTPException(status_code=400, detail="Insufficient stock for this operation")
        else:
            raise HTTPException(status_code=400, detail="Invalid change_type")

        # Insert new inventory change record
        await cursor.execute(
            """
            INSERT INTO inventory (product_id, change_type, quantity, change_date, reference, stock)
            VALUES (%s, %s, %s, NOW(), %s, %s)
            """,
            (change.product_id, change.change_type, change.quantity, change.reference, new_stock)
        )

        # Update current stock record (change_type IS NULL)
        if current:
            await cursor.execute(
                "UPDATE inventory SET stock=%s, change_date=NOW() WHERE product_id=%s AND change_type IS NULL",
                (new_stock, change.product_id)
            )
        else:
            # If no current stock row, create one
            await cursor.execute(
                "INSERT INTO inventory (product_id, stock, change_type, change_date) VALUES (%s, %s, NULL, NOW())",
                (change.product_id, new_stock)
            )
        await db.commit()
    return {"message": "Inventory updated successfully", "new_stock": new_stock}