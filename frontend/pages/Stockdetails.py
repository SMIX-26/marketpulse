import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from frontend.api import (
    get_stock,
    get_stock_changes,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MarketPulse Stock Details",
    page_icon="📈",
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
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #E8E8F0 !important;
        opacity: 1 !important;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1600px;
    }

    .stButton > button {
        background: #111421;
        color: #E9E9ED;
        border: 1px solid #282B3B;
        border-radius: 9px;
    }

    .stButton > button:hover {
        border-color: #8D55FF;
        color: white;
    }

    div[data-baseweb="select"] > div {
        background: #0B0E18;
        border-color: #282B3B;
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
    st.write("☆  Watchlist")
    st.write("◔  **Stock Details**")
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
# STOCK SELECTOR
# =========================================================

left, right = st.columns([3, 1])

with left:
    st.title("Stock Details")
    st.caption("Detailed market intelligence and recent changes")

with right:
    selected_stock = st.selectbox(
        "Select Stock",
        ["NVDA", "AAPL", "TSLA", "AMZN", "META"],
    )

symbol = selected_stock.strip().upper()


# =========================================================
# LOAD STOCK DATA
# =========================================================

stock_data = get_stock(symbol)
changes = get_stock_changes(symbol)


if "error" in stock_data:
    st.error(stock_data["error"])
    st.stop()

if "error" in changes:
    st.error(changes["error"])
    st.stop()


# =========================================================
# BASIC DATA
# =========================================================

current_price = stock_data.get("price", 0)
previous_close = stock_data.get("previous_close", 0)
volume = stock_data.get("volume", 0)

daily_change = stock_data.get(
    "price_change_percent",
    0
)

attention = changes.get("attention", {})

attention_score = attention.get("score", 0)
attention_level = attention.get("level", "LOW")
attention_reasons = attention.get("reasons", [])

news_count = changes.get("news_count", 0)
volume_change = changes.get("volume_change_percent", 0)

previous_snapshot_price = changes.get("previous_price")


# =========================================================
# COMPANY NAMES
# =========================================================

company_names = {
    "NVDA": "NVIDIA Corporation",
    "AAPL": "Apple Inc.",
    "TSLA": "Tesla, Inc.",
    "AMZN": "Amazon.com, Inc.",
    "META": "Meta Platforms, Inc.",
}

company_name = company_names.get(symbol, symbol)


# =========================================================
# STOCK HEADER
# =========================================================

st.subheader(f"{symbol} — {company_name}")

price_col, change_col, attention_col = st.columns([2, 2, 1])

with price_col:
    st.metric(
        "Current Price",
        f"${current_price:,.2f}",
    )

with change_col:
    st.metric(
        "Today's Change",
        f"{daily_change:+.2f}%",
    )

with attention_col:

    if attention_level == "HIGH":
        st.metric(
            "Attention",
            f"{attention_score}/100",
            "HIGH",
        )
    elif attention_level == "MEDIUM":
        st.metric(
            "Attention",
            f"{attention_score}/100",
            "MEDIUM",
        )
    else:
        st.metric(
            "Attention",
            f"{attention_score}/100",
            "LOW",
        )


st.divider()


# =========================================================
# KEY METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Attention Score",
        f"{attention_score}/100",
        attention_level,
    )

with m2:

    if previous_snapshot_price:
        st.metric(
            "Price Since Last Visit",
            f"${previous_snapshot_price:,.2f}",
            f"{changes.get('price_change_percent', 0):+.2f}%",
        )
    else:
        st.metric(
            "Previous Close",
            f"${previous_close:,.2f}",
        )

with m3:

    if volume_change:
        st.metric(
            "Volume Change",
            f"{volume_change:+.1f}%",
        )
    else:
        st.metric(
            "Volume",
            f"{volume:,.0f}",
        )

with m4:
    st.metric(
        "New News Events",
        news_count,
        "Since last visit",
    )


st.write("")


# =========================================================
# GET CHART DATA
# =========================================================

try:

    ticker = yf.Ticker(symbol)

    history = ticker.history(
        period="1mo",
        interval="1d",
    )

except Exception as e:

    history = None


# =========================================================
# PRICE CHART + ATTENTION
# =========================================================

chart_col, attention_col = st.columns([1.7, 1])


# =========================================================
# PRICE PERFORMANCE
# =========================================================

with chart_col:

    st.subheader("Price Performance")

    if history is not None and not history.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["Close"],
                mode="lines",
                name=symbol,
                line={
                    "color": "#FF4C99",
                    "width": 3,
                },
                fill="tozeroy",
                fillcolor="rgba(255,76,153,0.12)",
                hovertemplate="$%{y:.2f}<extra></extra>",
            )
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={
                "color": "#85889A",
            },
            xaxis={
                "showgrid": True,
                "gridcolor": "#1A1D2A",
                "zeroline": False,
            },
            yaxis={
                "showgrid": True,
                "gridcolor": "#1A1D2A",
                "zeroline": False,
                "tickprefix": "$",
            },
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False,
            },
        )

    else:
        st.warning("Unable to load chart data.")


# =========================================================
# ATTENTION EXPLANATION
# =========================================================

with attention_col:

    st.subheader(f"Why is {symbol} on your radar?")

    st.metric(
        "Attention Score",
        f"{attention_score}/100",
    )

    if attention_level == "HIGH":
        st.error("🔥 HIGH ATTENTION")
    elif attention_level == "MEDIUM":
        st.warning("⚡ MEDIUM ATTENTION")
    else:
        st.info("LOW ATTENTION")

    st.write("**Main signals**")

    if attention_reasons:

        for reason in attention_reasons:
            st.write(f"🟣 {reason}")

    else:
        st.write("No significant changes detected.")

    explanation = attention.get(
        "explanation",
        "No significant changes detected.",
    )

    st.info(explanation)


# =========================================================
# NEWS + MARKET STATISTICS
# =========================================================

st.write("")

news_col, stats_col = st.columns([1.5, 1])


# =========================================================
# NEWS
# =========================================================

with news_col:

    st.subheader("Recent News")

    try:

        news = ticker.news

        if news:

            displayed_news = 0

            for item in news[:5]:

                content = item.get(
                    "content",
                    {},
                )

                title = content.get(
                    "title",
                    "No title",
                )

                publisher = content.get(
                    "provider",
                    {},
                ).get(
                    "displayName",
                    "Yahoo Finance",
                )

                url = content.get(
                    "canonicalUrl",
                    {},
                ).get(
                    "url",
                    "",
                )

                st.write(f"**{title}**")

                st.caption(
                    f"{publisher}"
                )

                if url:
                    st.link_button(
                        "Read article",
                        url,
                    )

                st.divider()

                displayed_news += 1

            if displayed_news == 0:
                st.info("No recent news available.")

        else:
            st.info("No recent news available.")

    except Exception:
        st.info("Unable to load recent news.")


# =========================================================
# MARKET STATISTICS
# =========================================================

with stats_col:

    st.subheader("Market Statistics")

    if history is not None and not history.empty:

        latest = history.iloc[-1]

        day_high = latest.get(
            "High",
            0,
        )

        day_low = latest.get(
            "Low",
            0,
        )

    else:

        day_high = 0
        day_low = 0

    st.metric(
        "Previous Close",
        f"${previous_close:,.2f}",
    )

    st.metric(
        "Day High",
        f"${day_high:,.2f}",
    )

    st.metric(
        "Day Low",
        f"${day_low:,.2f}",
    )

    st.metric(
        "Volume",
        f"{volume:,.0f}",
    )

    if daily_change > 0:
        sentiment = "Bullish"
    elif daily_change < 0:
        sentiment = "Bearish"
    else:
        sentiment = "Neutral"

    st.metric(
        "Sentiment",
        sentiment,
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MarketPulse © 2026 • Smart Market Intelligence"
)