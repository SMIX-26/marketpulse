from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User, Watchlist

router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"]
)


# =========================================================
# ADD STOCK TO WATCHLIST
# =========================================================

@router.post("/")
def add_to_watchlist(
    symbol: str,
    company_name: str = "",
    db: Session = Depends(get_db)
):
    symbol = symbol.strip().upper()

    user = (
        db.query(User)
        .filter(User.device_id == "demo-user")
        .first()
    )

    if not user:
        user = User(device_id="demo-user")
        db.add(user)
        db.commit()
        db.refresh(user)

    existing = (
        db.query(Watchlist)
        .filter(
            Watchlist.user_id == user.id,
            Watchlist.symbol == symbol
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"{symbol} is already in your watchlist"
        )

    stock = Watchlist(
        user_id=user.id,
        symbol=symbol,
        company_name=company_name
    )

    db.add(stock)
    db.commit()
    db.refresh(stock)

    return {
        "message": f"{symbol} added to watchlist",
        "id": stock.id,
        "symbol": stock.symbol,
        "company_name": stock.company_name
    }


# =========================================================
# GET WATCHLIST
# =========================================================

@router.get("/")
def get_watchlist(
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.device_id == "demo-user")
        .first()
    )

    if not user:
        return []

    stocks = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user.id)
        .all()
    )

    return [
        {
            "id": stock.id,
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "created_at": stock.created_at
        }
        for stock in stocks
    ]


# =========================================================
# REMOVE STOCK FROM WATCHLIST
# =========================================================

@router.delete("/{symbol}")
def remove_from_watchlist(
    symbol: str,
    db: Session = Depends(get_db)
):
    symbol = symbol.strip().upper()

    user = (
        db.query(User)
        .filter(User.device_id == "demo-user")
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    stock = (
        db.query(Watchlist)
        .filter(
            Watchlist.user_id == user.id,
            Watchlist.symbol == symbol
        )
        .first()
    )

    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"{symbol} is not in your watchlist"
        )

    db.delete(stock)
    db.commit()

    return {
        "message": f"{symbol} removed from watchlist"
    }