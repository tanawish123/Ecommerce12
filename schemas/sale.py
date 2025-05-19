from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field


class RevenueResponse(BaseModel):
    revenue: float = Field(..., description="Total revenue")


class RevenueSummaryItem(BaseModel):
    period: str = Field(..., description="Period identifier (e.g., 2025-05 for monthly)")
    revenue: float = Field(..., description="Revenue in this period")


class RevenueComparisonPeriod(BaseModel):
    start_date: date
    end_date: date
    revenue: float


class RevenueComparisonResponse(BaseModel):
    period1: RevenueComparisonPeriod
    period2: RevenueComparisonPeriod


class SaleItem(BaseModel):
    sale_id: int
    product_id: int
    product_name: str
    category: str
    quantity: int
    sale_date: date
    price_per_unit: float
    total_price: float

class SalesQueryParams(BaseModel):
    start_date: Optional[date] = Field(None, description="Start date for filtering sales")
    end_date: Optional[date] = Field(None, description="End date for filtering sales")
    product_id: Optional[int] = Field(None, gt=0, description="Filter by product ID")
    category: Optional[str] = Field(None, description="Filter by product category")
    period: Optional[str] = Field("daily", pattern="^(daily|weekly|monthly|annual)$",
                                description="Aggregation period: daily, weekly, monthly, annual")
    
class RevenueComparisonRequest(BaseModel):
    period1_start: date = Field(..., description="Start date for the first comparison period")
    period1_end: date = Field(..., description="End date for the first comparison period")
    period2_start: date = Field(..., description="Start date for the second comparison period")
    period2_end: date = Field(..., description="End date for the second comparison period")
    category: Optional[str] = Field(None, description="Filter by product category")
    product_id: Optional[int] = Field(None, gt=0, description="Filter by product ID")