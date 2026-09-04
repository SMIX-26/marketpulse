import requests


API_BASE_URL = "https://marketpulse-backend-pumf.onrender.com"


def _request(method, endpoint, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.request(
            method,
            url,
            timeout=15,
            **kwargs
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "error": "Backend is not running. Start FastAPI first."
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Backend request timed out."
        }

    except requests.exceptions.HTTPError as e:
        try:
            detail = response.json().get("detail", str(e))
        except Exception:
            detail = str(e)

        return {
            "error": detail
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def check_backend():
    return _request("GET", "/health")


def get_stock(symbol):
    return _request(
        "GET",
        f"/stocks/{symbol.strip().upper()}"
    )


def get_watchlist():
    return _request(
        "GET",
        "/watchlist/"
    )


def add_to_watchlist(symbol, company_name=""):
    return _request(
        "POST",
        "/watchlist/",
        params={
            "symbol": symbol.strip().upper(),
            "company_name": company_name
        }
    )


def remove_from_watchlist(symbol):
    return _request(
        "DELETE",
        f"/watchlist/{symbol.strip().upper()}"
    )


def get_stock_changes(symbol):
    return _request(
        "GET",
        f"/changes/{symbol.strip().upper()}"
    )


def mark_stock_as_viewed(symbol):
    return _request(
        "POST",
        f"/changes/{symbol.strip().upper()}/view"
    )

def get_stock_history(symbol):
    return _request(
        "GET",
        f"/history/{symbol.strip().upper()}"
    )