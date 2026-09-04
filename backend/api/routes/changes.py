from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Watchlist, NewsEvent
from backend.services.market_service import get_stock_data
from backend.services.change_detector import detect_changes
from backend.services.attention_engine import calculate_attention_score
from backend.services.snapshot_service import save_stock_snapshot
from backend.services.news_storage import save_news_events
from backend.services.ai_explanation import generate_ai_explanation


router = APIRouter(
    prefix="/changes",
    tags=["Changes"]
)


@router.get("/{symbol}")
def get_stock_changes(
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

    current_data = get_stock_data(symbol)

    # Save latest news
    try:
        save_news_events(db, symbol)
    except Exception:
        pass

    # Detect changes since last visit
    changes = detect_changes(
        db=db,
        watchlist_id=stock.id,
        current_price=current_data["price"],
        current_volume=current_data["volume"]
    )

    # Count news published after last visit
    news_count = 0

    if stock.last_viewed_at:
        news_count = db.query(NewsEvent).filter(
            NewsEvent.symbol == symbol,
            NewsEvent.published_at.isnot(None),
            NewsEvent.published_at > stock.last_viewed_at
        ).count()

    # Calculate attention score
    attention = calculate_attention_score(
        price_change_percent=changes["price_change_percent"],
        volume_change_percent=current_data["volume_change_percent"],
        volume_ratio=current_data["volume_ratio"],
        news_count=news_count
    )

    # Generate AI explanation
    ai_explanation = generate_ai_explanation(
        symbol=symbol,
        price_change_percent=changes["price_change_percent"],
        volume_ratio=current_data["volume_ratio"],
        news_count=news_count,
        attention_level=attention["level"]
    )

    return {
        "symbol": symbol,
        "current_price": current_data["price"],
        "daily_price_change_percent": current_data["price_change_percent"],

        "price_change_percent": changes["price_change_percent"],
        "volume_change_percent": current_data["volume_change_percent"],
        "volume_ratio": current_data["volume_ratio"],

        "previous_price": changes["previous_price"],
        "previous_volume": changes["previous_volume"],

        "news_count": news_count,

        "attention": attention,

        "ai_explanation": ai_explanation,

        "last_viewed_at": stock.last_viewed_at
    }


@router.post("/{symbol}/view")
def mark_stock_as_viewed(
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

    snapshot = save_stock_snapshot(
        db=db,
        watchlist_id=stock.id,
        symbol=symbol
    )

    stock.last_viewed_at = datetime.utcnow()

    db.commit()

    return {
        "message": f"{symbol} marked as viewed",
        "symbol": symbol,
        "snapshot_id": snapshot.id,
        "last_viewed_at": stock.last_viewed_at
    }