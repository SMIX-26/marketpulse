from datetime import datetime

from sqlalchemy.orm import Session

from backend.database.models import NewsEvent
from backend.services.news_service import get_stock_news


def parse_published_at(value):
    """
    Convert Yahoo Finance publication timestamps
    into a Python datetime.
    """

    if not value:
        return None

    if isinstance(value, datetime):
        return value

    try:
        # Yahoo Finance may return Unix timestamp
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)

        # Handle ISO timestamps such as:
        # 2026-09-04T17:52:51Z
        if isinstance(value, str):
            value = value.strip()

            if value.endswith("Z"):
                value = value[:-1] + "+00:00"

            parsed = datetime.fromisoformat(value)

            # Database column is timestamp without timezone
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)

            return parsed

    except Exception:
        return None

    return None


def save_news_events(db: Session, symbol: str):
    symbol = symbol.strip().upper()

    news_items = get_stock_news(symbol)

    saved_events = []

    for item in news_items:

        title = item.get("title", "").strip()

        if not title:
            continue

        published_at = parse_published_at(
            item.get("published_at")
        )

        # Prevent duplicate news
        existing = db.query(NewsEvent).filter(
            NewsEvent.symbol == symbol,
            NewsEvent.title == title
        ).first()

        if existing:
            continue

        news_event = NewsEvent(
            symbol=symbol,
            title=title,
            description=item.get("description", ""),
            url=item.get("url", ""),
            published_at=published_at
        )

        db.add(news_event)
        saved_events.append(news_event)

    db.commit()

    return saved_events