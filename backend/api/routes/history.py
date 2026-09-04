from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Watchlist, StockSnapshot, NewsEvent

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/{symbol}")
def get_stock_history(
    symbol: str,
    db: Session = Depends(get_db)
):
    symbol = symbol.strip().upper()

    stock = db.query(Watchlist).filter(
        Watchlist.symbol == symbol
    ).first()

    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"{symbol} is not in your watchlist"
        )

    snapshots = (
        db.query(StockSnapshot)
        .filter(
            StockSnapshot.watchlist_id == stock.id
        )
        .order_by(
            StockSnapshot.timestamp.desc()
        )
        .all()
    )

    history = []

    for snapshot in snapshots:

        news_count = db.query(NewsEvent).filter(
            NewsEvent.symbol == symbol,
            NewsEvent.published_at.isnot(None),
            NewsEvent.published_at <= snapshot.timestamp
        ).count()

        history.append({
            "id": snapshot.id,
            "symbol": snapshot.symbol,
            "price": snapshot.price,
            "previous_close": snapshot.previous_close,
            "volume": snapshot.volume,
            "timestamp": snapshot.timestamp,
            "news_count": news_count
        })

    return history