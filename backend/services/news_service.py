import yfinance as yf


def get_stock_news(symbol: str):
    ticker = yf.Ticker(symbol)

    news = ticker.news

    results = []

    for item in news:
        content = item.get("content", {})

        title = content.get("title", "No title")
        description = content.get("summary", "")

        url = content.get(
            "canonicalUrl",
            {}
        ).get("url", "")

        published_at = content.get("pubDate")

        results.append({
            "symbol": symbol.upper(),
            "title": title,
            "description": description,
            "url": url,
            "published_at": published_at
        })

    return results