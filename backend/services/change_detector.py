from sqlalchemy.orm import Session

from backend.database.models import StockSnapshot


def get_previous_snapshot(
    db: Session,
    watchlist_id: int
):
    snapshots = (
        db.query(StockSnapshot)
        .filter(
            StockSnapshot.watchlist_id == watchlist_id
        )
        .order_by(StockSnapshot.timestamp.desc())
        .all()
    )

    if not snapshots:
        return None

    return snapshots[0]


def detect_changes(
    db: Session,
    watchlist_id: int,
    current_price: float,
    current_volume: float
):
    previous_snapshot = get_previous_snapshot(
        db,
        watchlist_id
    )

    # No previous snapshot
    if not previous_snapshot:
        return {
            "has_previous_data": False,
            "previous_price": None,
            "current_price": current_price,
            "price_change_percent": 0,
            "previous_volume": None,
            "current_volume": current_volume,
            "volume_change_percent": 0
        }

    # -----------------------------
    # PRICE CHANGE
    # -----------------------------

    price_change_percent = 0

    if previous_snapshot.price:
        price_change_percent = (
            (current_price - previous_snapshot.price)
            / previous_snapshot.price
        ) * 100

    # -----------------------------
    # VOLUME CHANGE
    # -----------------------------

    volume_change_percent = 0

    if previous_snapshot.volume:
        volume_change_percent = (
            (current_volume - previous_snapshot.volume)
            / previous_snapshot.volume
        ) * 100

    return {
        "has_previous_data": True,
        "previous_price": previous_snapshot.price,
        "current_price": current_price,
        "price_change_percent": round(price_change_percent, 2),
        "previous_volume": previous_snapshot.volume,
        "current_volume": current_volume,
        "volume_change_percent": round(volume_change_percent, 2)
    }