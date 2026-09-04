from fastapi import FastAPI

from backend.api.routes.stocks import router as stocks_router
from backend.database.connection import Base, engine
from backend.api.routes.watchlist import router as watchlist_router
from backend.api.routes.changes import router as changes_router
from backend.api.routes.history import router as history_router
from backend.database import models


app = FastAPI(
    title="MarketPulse API",
    description="Smart Market Watchlist Backend",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)

# Register stock routes
app.include_router(stocks_router)

# Register watchlist routes
app.include_router(watchlist_router)

# Register changes routes
app.include_router(changes_router)

app.include_router(history_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to MarketPulse API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
