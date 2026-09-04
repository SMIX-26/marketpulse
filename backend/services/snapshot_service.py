from sqlalchemy.orm import Session

from backend.database.models import StockSnapshot
from backend.services.market_service import get_stock_data


def save_stock_snapshot(
    db: Session,
    watchlist_id: int,
    symbol: str
):
    data = get_stock_data(symbol)

    snapshot = StockSnapshot(
        watchlist_id=watchlist_id,
        symbol=data["symbol"],
        price=data["price"],
        previous_close=data["previous_close"],
        volume=data["volume"]
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot