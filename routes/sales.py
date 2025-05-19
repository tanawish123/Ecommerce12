from fastapi import APIRouter, Depends ,Body
from database import get_db
from models import Sale
from typing import List
from datetime import date
from schemas.sale import SalesQueryParams,RevenueSummaryItem,RevenueComparisonPeriod,RevenueComparisonResponse,RevenueComparisonRequest,SaleItem

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/")
async def record_sale(sale: Sale, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO sales (product_id, quantity, sale_date) VALUES (%s, %s, %s)",
            (sale.product_id, sale.quantity, sale.sale_date)
        )
        await cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s",
                             (sale.quantity, sale.product_id))
    return {"message": "Sale recorded successfully"}

@router.get("/sales", response_model=List[SaleItem], summary="Retrieve sales data")
async def get_sales(params: SalesQueryParams = Depends(), db= Depends(get_db)):
    where_clauses = []
    values = []

    if params.start_date:
        where_clauses.append("s.sale_date >= %s")
        values.append(params.start_date)
    if params.end_date:
        where_clauses.append("s.sale_date <= %s")
        values.append(params.end_date)
    if params.product_id:
        where_clauses.append("p.id = %s")
        values.append(params.product_id)
    if params.category:
        where_clauses.append("p.category = %s")
        values.append(params.category)

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
        SELECT s.id, p.id, p.name, p.category, s.quantity, s.sale_date, p.price, s.quantity * p.price
        FROM sales s
        JOIN products p ON s.product_id = p.id
        {where_sql}
        ORDER BY s.sale_date DESC
        LIMIT 100
    """

    async with db.cursor() as cursor:
        await cursor.execute(query, tuple(values))
        rows = await cursor.fetchall()

    return [
        SaleItem(
            sale_id=row[0],
            product_id=row[1],
            product_name=row[2],
            category=row[3],
            quantity=row[4],
            sale_date=row[5],
            price_per_unit=float(row[6]),
            total_price=float(row[7])
        ) for row in rows
    ]


@router.get("/revenue", response_model=List[RevenueSummaryItem], summary="Get revenue aggregated by period")
async def get_revenue(params: SalesQueryParams = Depends(), db = Depends(get_db)):
    period_map = {
        "daily": "DATE(s.sale_date)",
        "weekly": "YEAR(s.sale_date), WEEK(s.sale_date)",
        "monthly": "DATE_FORMAT(s.sale_date, '%Y-%m')",
        "annual": "YEAR(s.sale_date)"
    }
    time_group = period_map.get(params.period.lower(), "DATE(s.sale_date)")

    where_clauses = []
    values = []

    if params.start_date:
        where_clauses.append("s.sale_date >= %s")
        values.append(params.start_date)
    if params.end_date:
        where_clauses.append("s.sale_date <= %s")
        values.append(params.end_date)
    if params.product_id:
        where_clauses.append("p.id = %s")
        values.append(params.product_id)
    if params.category:
        where_clauses.append("p.category = %s")
        values.append(params.category)

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    query = f"""
        SELECT
            {time_group} AS period,
            SUM(s.quantity * p.price) AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.id
        {where_sql}
        GROUP BY period
        ORDER BY period
    """

    async with db.cursor() as cursor:
        await cursor.execute(query, tuple(values))
        rows = await cursor.fetchall()

    return [RevenueSummaryItem(period=str(row[0]), revenue=float(row[1])) for row in rows]


@router.post("/revenue/compare", response_model=RevenueComparisonResponse, summary="Compare revenue across two periods")
async def compare_revenue(
    params: RevenueComparisonRequest = Body(...),
    db = Depends(get_db)
):
    def build_where(start: date, end: date):
        clauses = ["s.sale_date >= %s", "s.sale_date <= %s"]
        vals = [start, end]
        if params.category:
            clauses.append("p.category = %s")
            vals.append(params.category)
        if params.product_id:
            clauses.append("p.id = %s")
            vals.append(params.product_id)
        return " AND ".join(clauses), vals

    where1, vals1 = build_where(params.period1_start, params.period1_end)
    where2, vals2 = build_where(params.period2_start, params.period2_end)

    query = f"""
        SELECT SUM(s.quantity * p.price) FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE {{where_clause}}
    """

    async with db.cursor() as cursor:
        await cursor.execute(query.format(where_clause=where1), tuple(vals1))
        rev1 = await cursor.fetchone()
        await cursor.execute(query.format(where_clause=where2), tuple(vals2))
        rev2 = await cursor.fetchone()

    return RevenueComparisonResponse(
        period1=RevenueComparisonPeriod(
            start_date=params.period1_start,
            end_date=params.period1_end,
            revenue=float(rev1[0]) if rev1 and rev1[0] else 0.0
        ),
        period2=RevenueComparisonPeriod(
            start_date=params.period2_start,
            end_date=params.period2_end,
            revenue=float(rev2[0]) if rev2 and rev2[0] else 0.0
        )
    )