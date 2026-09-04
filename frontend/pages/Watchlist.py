import sys
from pathlib import Path

import streamlit as st

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from frontend.api import (
    get_watchlist,
    get_stock,
    get_stock_changes,
    add_to_watchlist,
    remove_from_watchlist,
    mark_stock_as_viewed,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MarketPulse Watchlist",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #050711;
        color: #F5F5F7;
    }

    [data-testid="stHeader"] {
        background: #050711;
    }

    [data-testid="stSidebar"] {
        background: #060812;
        border-right: 1px solid #1B1D2B;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1600px;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #E8E8F0 !important;
        opacity: 1 !important;
    }

    .stButton > button {
        background: #111421;
        color: #E9E9ED;
        border: 1px solid #282B3B;
        border-radius: 9px;
        min-height: 40px;
    }

    .stButton > button:hover {
        border-color: #8D55FF;
        color: white;
    }

    div[data-baseweb="select"] > div {
        background: #0B0E18;
        border-color: #282B3B;
        color: white;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("〽 MarketPulse")
    st.caption("Smart Market Intelligence")

    st.divider()

    st.write("▦  Dashboard")
    st.write("☆  **Watchlist**")
    st.write("◔  Stock Details")
    st.write("♧  Alerts")
    st.write("▤  News")
    st.write("◷  History")
    st.write("▥  Analytics")

    st.divider()

    st.write("⚙  Settings")
    st.write("?  Help & Support")

    st.divider()

    st.info(
        "♛ **Upgrade to Pro**\n\n"
        "Unlock advanced analytics, more alerts & AI insights."
    )

    st.toggle("Dark Mode", value=True)


# =========================================================
# MARKET STATUS
# =========================================================

st.success("● Market is Open")


# =========================================================
# HEADER
# =========================================================

header_col, button_col = st.columns([3, 1])

with header_col:

    st.title("My Watchlist")
    st.caption(
        "Track stocks and see what changed since your last visit"
    )

with button_col:

    if st.button("↻ Refresh", width="stretch"):
        st.rerun()


# =========================================================
# ADD STOCK
# =========================================================

with st.expander("＋ Add Stock to Watchlist"):

    add_col1, add_col2, add_col3 = st.columns([1, 2, 1])

    with add_col1:

        new_symbol = st.text_input(
            "Symbol",
            placeholder="e.g. NVDA",
        )

    with add_col2:

        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. NVIDIA Corporation",
        )

    with add_col3:

        st.write("")

        if st.button(
            "Add Stock",
            width="stretch",
        ):

            if not new_symbol.strip():

                st.warning(
                    "Please enter a stock symbol."
                )

            else:

                result = add_to_watchlist(
                    new_symbol,
                    company_name,
                )

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        f"{result['symbol']} added to your watchlist."
                    )

                    st.rerun()


# =========================================================
# LOAD WATCHLIST
# =========================================================

watchlist = get_watchlist()

if isinstance(watchlist, dict) and "error" in watchlist:

    st.error(
        f"Could not connect to MarketPulse backend: "
        f"{watchlist['error']}"
    )

    st.stop()


# =========================================================
# SEARCH + FILTER
# =========================================================

search_col, filter_col = st.columns([2, 1])

with search_col:

    search = st.text_input(
        "Search stocks",
        placeholder="Search stocks...",
    )

with filter_col:

    attention_filter = st.selectbox(
        "Attention",
        [
            "All Stocks",
            "High Attention",
            "Medium Attention",
            "Low Attention",
        ],
    )


# =========================================================
# PROCESS STOCKS
# =========================================================

stock_results = []

for stock in watchlist:

    symbol = stock["symbol"].strip().upper()

    company_name = (
        stock.get("company_name")
        or symbol
    )

    # Search filter
    if search and search.upper() not in symbol:

        continue

    stock_data = get_stock(symbol)

    if (
        isinstance(stock_data, dict)
        and "error" in stock_data
    ):

        stock_results.append(
            {
                "stock": stock,
                "error": stock_data["error"],
            }
        )

        continue

    changes = get_stock_changes(symbol)

    if (
        isinstance(changes, dict)
        and "error" in changes
    ):

        changes = {}

    attention = changes.get(
        "attention",
        {},
    )

    level = attention.get(
        "level",
        "LOW",
    )

    # Attention filter
    if attention_filter != "All Stocks":

        expected_level = (
            attention_filter
            .replace(" Attention", "")
            .upper()
        )

        if level != expected_level:

            continue

    stock_results.append(
        {
            "stock": stock,
            "stock_data": stock_data,
            "changes": changes,
            "symbol": symbol,
            "company_name": company_name,
        }
    )


# =========================================================
# EMPTY STATE
# =========================================================

if not stock_results:

    st.info(
        "☆ No stocks match your current filter."
    )

    st.stop()


# =========================================================
# STOCK CARDS
# =========================================================

for item in stock_results:

    # Backend error
    if "error" in item:

        stock = item["stock"]

        st.warning(
            f"{stock['symbol']}: {item['error']}"
        )

        continue

    stock = item["stock"]
    stock_data = item["stock_data"]
    changes = item["changes"]

    symbol = item["symbol"]
    company_name = item["company_name"]


    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    price = stock_data.get(
        "price",
        0,
    )

    daily_change = stock_data.get(
        "price_change_percent",
        0,
    )

    price_change = changes.get(
        "price_change_percent",
        0,
    )

    volume_change = changes.get(
        "volume_change_percent",
        0,
    )

    volume_ratio = changes.get(
        "volume_ratio",
        stock_data.get("volume_ratio", 0),
    )

    attention = changes.get(
        "attention",
        {},
    )

    score = attention.get(
        "score",
        0,
    )

    level = attention.get(
        "level",
        "LOW",
    )

    explanation = attention.get(
        "explanation",
        "No significant changes detected.",
    )

    # AI-generated explanation from Gemini
    ai_explanation = changes.get(
        "ai_explanation",
        "AI explanation is currently unavailable.",
    )


    # =====================================================
    # STOCK CONTAINER
    # =====================================================

    with st.container(border=True):

        top_left, top_middle, top_right = st.columns(
            [2, 2, 1]
        )


        # -------------------------------------------------
        # STOCK INFORMATION
        # -------------------------------------------------

        with top_left:

            st.subheader(symbol)

            st.caption(company_name)

            st.metric(
                "Current Price",
                f"${price:,.2f}",
                f"{daily_change:+.2f}%",
            )


        # -------------------------------------------------
        # CHANGES
        # -------------------------------------------------

        with top_middle:

            st.write("**Since Last Visit**")

            change_col1, change_col2 = st.columns(2)

            with change_col1:

                st.metric(
                    "Price",
                    f"{price_change:+.2f}%",
                )

            with change_col2:

                st.metric(
                    "Volume",
                    f"{volume_change:+.1f}%",
                    help=f"{volume_ratio:.2f}× normal trading volume",
                )


        # -------------------------------------------------
        # ATTENTION
        # -------------------------------------------------

        with top_right:

            st.write("**Attention**")

            if level == "HIGH":

                st.error(
                    "🔥 HIGH"
                )

            elif level == "MEDIUM":

                st.warning(
                    "⚡ MEDIUM"
                )

            else:

                st.info(
                    "LOW"
                )

            st.metric(
                "Score",
                f"{score}/100",
            )


        # -------------------------------------------------
        # AI INSIGHT
        # -------------------------------------------------

        st.write("")

        st.info(
            f"🤖 **AI Insight**\n\n{ai_explanation}"
        )


        # -------------------------------------------------
        # ACTION BUTTONS
        # -------------------------------------------------

        action_col1, action_col2 = st.columns(2)

        with action_col1:

            if st.button(
                "✓ Mark as Viewed",
                key=f"view_{symbol}",
                width="stretch",
            ):

                result = mark_stock_as_viewed(
                    symbol
                )

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        f"{symbol} marked as viewed."
                    )

                    st.rerun()


        with action_col2:

            if st.button(
                "🗑 Remove",
                key=f"remove_{symbol}",
                width="stretch",
            ):

                result = remove_from_watchlist(
                    symbol
                )

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        f"{symbol} removed from watchlist."
                    )

                    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MarketPulse © 2026 • Smart Market Intelligence"
)

