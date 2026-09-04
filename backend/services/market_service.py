import yfinance as yf


def get_stock_data(symbol: str):
    symbol = symbol.strip().upper()

    ticker = yf.Ticker(symbol)

    # ---------------------------------------------
    # CURRENT MARKET DATA
    # ---------------------------------------------

    info = ticker.fast_info

    current_price = info.get("lastPrice")
    previous_close = info.get("previousClose")
    current_volume = info.get("lastVolume")

    if current_price is None:
        raise ValueError(f"Could not fetch data for {symbol}")

    # ---------------------------------------------
    # DAILY PRICE CHANGE
    # ---------------------------------------------

    price_change = 0

    if previous_close:
        price_change = (
            (current_price - previous_close)
            / previous_close
        ) * 100

    # ---------------------------------------------
    # HISTORICAL VOLUME
    # ---------------------------------------------

    average_volume = 0
    volume_ratio = 0
    volume_change_percent = 0

    try:
        history = ticker.history(period="1mo")

        if not history.empty and "Volume" in history.columns:

            # Remove today's incomplete volume
            historical_volume = history["Volume"].iloc[:-1]

            if not historical_volume.empty:
                average_volume = float(
                    historical_volume.mean()
                )

                if average_volume > 0 and current_volume:
                    volume_ratio = (
                        current_volume / average_volume
                    )

                    volume_change_percent = (
                        (current_volume - average_volume)
                        / average_volume
                    ) * 100

    except Exception:
        average_volume = 0
        volume_ratio = 0
        volume_change_percent = 0

    # ---------------------------------------------
    # RETURN DATA
    # ---------------------------------------------

    return {
        "symbol": symbol,
        "price": current_price,
        "previous_close": previous_close,
        "volume": current_volume,

        "price_change_percent": round(
            price_change,
            2
        ),

        "average_volume": round(
            average_volume,
            2
        ),

        "volume_ratio": round(
            volume_ratio,
            2
        ),

        "volume_change_percent": round(
            volume_change_percent,
            2
        )
    }