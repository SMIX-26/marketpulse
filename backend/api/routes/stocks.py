from fastapi import APIRouter, HTTPException

from backend.services.market_service import get_stock_data


router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)


@router.get("/{symbol}")
def get_stock(symbol: str):
    try:
        return get_stock_data(symbol)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )