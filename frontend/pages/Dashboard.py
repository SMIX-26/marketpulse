import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

sys.path.append(str(Path(__file__).resolve().parents[2]))

from frontend.api import (
    get_watchlist,
    get_stock,
    get_stock_changes,
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MarketPulse Dashboard",
    page_icon="📊",
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

[data-testid="stSidebar"] > div:first-child {
padding-top: 1rem;
}

.block-container {
padding-top: 1.2rem;
padding-left: 2rem;
padding-right: 2rem;
max-width: 1600px;
}


/* =========================================================
SIDEBAR
========================================================= */

.brand {
display: flex;
align-items: center;
gap: 10px;
padding: 5px 10px 25px 10px;
}

.brand-icon {
font-size: 31px;
color: #9B5CFF;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #E8E8F0 !important;
    opacity: 1 !important;
}

.brand-name {
font-size: 20px;
font-weight: 700;
color: #FFFFFF;
}

.brand-subtitle {
font-size: 10px;
color: #85889A;
}

.side-item {
padding: 12px 14px;
margin: 5px 0;
border-radius: 9px;
color: #A5A7B5;
font-size: 14px;
}

.side-item.active {
background: linear-gradient(
90deg,
rgba(111, 59, 255, 0.30),
rgba(111, 59, 255, 0.08)
);
color: white;
border-left: 3px solid #8D55FF;
}

.upgrade-card {
margin-top: 65px;
padding: 20px 15px;
border: 1px solid #342064;
border-radius: 12px;
background:
radial-gradient(
circle at top,
rgba(118, 63, 255, 0.20),
transparent 65%
),
#0A0915;
text-align: center;
}

.upgrade-title {
font-size: 15px;
font-weight: 700;
margin-bottom: 8px;
}

.upgrade-text {
font-size: 11px;
color: #85889A;
line-height: 1.5;
}


/* =========================================================
MARKET TICKERS
========================================================= */

.ticker-container {
display: flex;
gap: 8px;
width: 100%;
overflow-x: auto;
margin-bottom: 24px;
scrollbar-width: none;
}

.ticker-container::-webkit-scrollbar {
display: none;
}

.ticker {
min-width: 145px;
padding: 9px 12px;
background: #0B0E18;
border: 1px solid #202333;
border-radius: 9px;
font-size: 12px;
}

.ticker-symbol {
font-weight: 700;
color: #F5F5F7;
margin-right: 7px;
}

.positive {
color: #23D982;
}

.negative {
color: #FF456A;
}


/* =========================================================
HEADER
========================================================= */

.page-title {
font-size: 28px;
font-weight: 700;
color: #FFFFFF;
}

.page-subtitle {
color: #85889A;
font-size: 13px;
margin-top: 3px;
margin-bottom: 25px;
}


/* =========================================================
CARDS
========================================================= */

.card {
background:
linear-gradient(
145deg,
rgba(18, 21, 34, 0.98),
rgba(9, 11, 20, 0.98)
);
border: 1px solid #202333;
border-radius: 13px;
padding: 20px;
height: 100%;
box-shadow: 0 8px 30px rgba(0, 0, 0, 0.20);
}

.card-title {
font-size: 13px;
font-weight: 600;
color: #E5E5EA;
}


/* =========================================================
KPI
========================================================= */

.metric-number {
font-size: 32px;
font-weight: 700;
margin-top: 12px;
color: #FFFFFF;
}

.metric-description {
font-size: 12px;
color: #9B5CFF;
margin-top: 5px;
}


/* =========================================================
ATTENTION
========================================================= */

.attention-badge {
display: inline-block;
padding: 7px 14px;
border-radius: 20px;
border: 1px solid #9B5CFF;
color: #B47CFF;
background: rgba(155, 92, 255, 0.08);
font-size: 11px;
font-weight: 700;
}


/* =========================================================
NEWS
========================================================= */

.news-item {
padding: 13px 0;
border-bottom: 1px solid #1C1F2C;
}

.news-title {
font-size: 13px;
color: #E9E9ED;
}

.news-source {
font-size: 10px;
color: #777B8D;
margin-top: 5px;
}


/* =========================================================
BUTTONS
========================================================= */

.stButton > button {
background: #111421;
color: #E9E9ED;
border: 1px solid #282B3B;
border-radius: 9px;
font-size: 12px;
min-height: 40px;
}

.stButton > button:hover {
border-color: #8D55FF;
color: white;
}


/* =========================================================
FOOTER
========================================================= */

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

    st.markdown(
        """
<div class="brand">
<div class="brand-icon">〽</div>

<div>
<div class="brand-name">
MarketPulse
</div>

<div class="brand-subtitle">
Smart Market Intelligence
</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="side-item active">▦ &nbsp; Dashboard</div>
<div class="side-item">☆ &nbsp; Watchlist</div>
<div class="side-item">◔ &nbsp; Market Overview</div>
<div class="side-item">♧ &nbsp; Alerts</div>
<div class="side-item">▤ &nbsp; News</div>
<div class="side-item">◷ &nbsp; History</div>
<div class="side-item">▥ &nbsp; Analytics</div>

<hr style="border-color:#202333;">

<div class="side-item">⚙ &nbsp; Settings</div>
<div class="side-item">? &nbsp; Help & Support</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="upgrade-card">

<div style="font-size:30px;">
♛
</div>

<div class="upgrade-title">
Upgrade to Pro
</div>

<div class="upgrade-text">
Unlock advanced analytics,<br>
more alerts & AI insights.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.toggle("Dark Mode", value=True)


# =========================================================
# MARKET STATUS
# =========================================================

st.markdown(
    """
<div style="
color:#35DB8A;
font-size:12px;
margin-bottom:8px;
">
● Market is Open
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# TICKERS
# =========================================================

watchlist_data = get_watchlist()

if isinstance(watchlist_data, dict) and "error" in watchlist_data:
    watchlist_data = []

tickers = []

for stock in watchlist_data:
    symbol = stock.get("symbol", "").strip().upper()

    if not symbol:
        continue

    market = get_stock(symbol)

    if isinstance(market, dict) and "error" in market:
        continue

    price = market.get("price", 0)
    change = market.get("price_change_percent", 0)

    css_class = "positive" if change >= 0 else "negative"
    change_text = f"{change:+.2f}%"

    tickers.append(
        (
            symbol,
            f"${price:,.2f}",
            change_text,
            css_class,
        )
    )

ticker_html = '<div class="ticker-container">'

for symbol, price, change, css_class in tickers:

    ticker_html += (
        f'<div class="ticker">'
        f'<span class="ticker-symbol">{symbol}</span>'
        f'<span style="color:#777B8D;">{price}</span>'
        f'<span class="{css_class}" style="margin-left:8px;">'
        f'{change}'
        f'</span>'
        f'</div>'
    )

ticker_html += "</div>"

st.markdown(
    ticker_html,
    unsafe_allow_html=True,
)


# =========================================================
# PAGE HEADER
# =========================================================

header_left, header_right = st.columns([3, 1])

with header_left:

    st.markdown(
        '<div class="page-title">Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        "Here's what changed since your last visit"
        "</div>",
        unsafe_allow_html=True,
    )


with header_right:

    st.button(
        "＋ Add Watchlist",
        width="stretch",
    )


# =========================================================
# KPI CARDS
# =========================================================

# Get current watchlist
watchlist_data = get_watchlist()

if isinstance(watchlist_data, dict) and "error" in watchlist_data:
    watchlist_data = []

# Count watchlist stocks
watchlist_count = len(watchlist_data)

# Calculate attention and news
high_attention_count = 0
new_news_count = 0

for stock in watchlist_data:

    symbol = stock.get("symbol", "").strip().upper()

    if not symbol:
        continue

    changes = get_stock_changes(symbol)

    if isinstance(changes, dict) and "error" not in changes:

        attention = changes.get("attention", {})

        if attention.get("level") == "HIGH":
            high_attention_count += 1

        new_news_count += changes.get("news_count", 0)


c1, c2, c3, c4 = st.columns(4)

kpis = [
    ("☆", "Watchlist Stocks", str(watchlist_count), "Your current watchlist"),
    ("♨", "High Attention", str(high_attention_count), "View all  ›"),
    ("▣", "New News", str(new_news_count), "Since last visit"),
    ("♧", "Alerts Triggered", "0", "View all  ›"),
]

for col, (icon, title, number, desc) in zip(
    [c1, c2, c3, c4],
    kpis,
):

    with col:

        st.markdown(
            f"""
<div class="card">

<div class="card-title">

<span style="
color:#9B5CFF;
font-size:19px;
">
{icon}
</span>

&nbsp; {title}

</div>

<div class="metric-number">
{number}
</div>

<div class="metric-description">
{desc}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# MAIN CONTENT
# =========================================================

left, right = st.columns([1, 1.65])


# =========================================================
# ATTENTION SCORE
# =========================================================

with left:

    st.markdown(
        """
<div class="card">

<div class="card-title">
Market Pulse Overview
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=82,
            number={
                "font": {
                    "size": 42,
                    "color": "#FFFFFF",
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 0,
                    "tickcolor": "rgba(0,0,0,0)",
                },
                "bar": {
                    "color": "#9B5CFF",
                    "thickness": 0.25,
                },
                "bgcolor": "#10121E",
                "borderwidth": 0,
            },
        )
    )

    gauge.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=5, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#FFFFFF"},
    )

    st.plotly_chart(
        gauge,
        width="stretch",
        config={"displayModeBar": False},
    )

    st.markdown(
        """
<div style="
text-align:center;
margin-top:-15px;
">

<span class="attention-badge">
♨ HIGH ATTENTION
</span>

</div>
""",
        unsafe_allow_html=True,
    )

    reasons = [
        ("↗", "Strong price movement", "+6.82% today"),
        ("▥", "Unusually high volume", "2.4x normal"),
        ("▣", "3 new news events", "Since your last visit"),
        ("↗", "Market sentiment", "Bullish"),
    ]

    for icon, title, subtitle in reasons:

        st.markdown(
            f"""
<div style="
display:flex;
gap:12px;
margin:13px 0;
align-items:center;
">

<div style="
width:32px;
height:32px;
border-radius:50%;
background:#151325;
border:1px solid #30244B;
display:flex;
align-items:center;
justify-content:center;
color:#9B5CFF;
">
{icon}
</div>

<div>

<div style="
font-size:12px;
color:#E8E8ED;
">
{title}
</div>

<div style="
font-size:10px;
color:#85889A;
margin-top:3px;
">
{subtitle}
</div>

</div>

</div>
""",
            unsafe_allow_html=True,
        )


# =========================================================
# NVDA GRAPH
# =========================================================

with right:

    dashboard_stock = None

    if watchlist_data:
        first_stock = watchlist_data[0]
        symbol = first_stock.get("symbol", "").strip().upper()

        if symbol:
            market = get_stock(symbol)

            if isinstance(market, dict) and "error" not in market:
                dashboard_stock = {
                    "symbol": symbol,
                    "company": first_stock.get("company_name") or symbol,
                    "price": market.get("price", 0),
                    "change": market.get("price_change_percent", 0),
                }

    if dashboard_stock:

        symbol = dashboard_stock["symbol"]
        company = dashboard_stock["company"]
        price = dashboard_stock["price"]
        change = dashboard_stock["change"]

        change_class = "#23D982" if change >= 0 else "#FF456A"

        st.markdown(
            f"""
<div class="card">

<div style="
font-size:12px;
color:#FFFFFF;
font-weight:700;
">

{symbol}

<span style="
color:#85889A;
font-weight:400;
">
• {company}
</span>

</div>

<div style="
font-size:30px;
font-weight:700;
margin-top:8px;
">

${price:,.2f}

<span style="
color:{change_class};
font-size:13px;
margin-left:10px;
">
{change:+.2f}%
</span>

</div>

</div>
""",
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
<div class="card">

<div style="
font-size:13px;
color:#85889A;
text-align:center;
padding:35px;
">
No watchlist data available.
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    # Get real historical prices

    if dashboard_stock:

        chart_symbol = dashboard_stock["symbol"]

        ticker = yf.Ticker(chart_symbol)

        history = ticker.history(period="1mo")

        if not history.empty:
            x = history.index
            y = history["Close"].tolist()
        else:
            x = list(range(30))
            y = [dashboard_stock["price"]] * 30

    else:
        x = list(range(30))
        y = [0] * 30

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
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
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#85889A"},
        xaxis={
            "showgrid": True,
            "gridcolor": "#1A1D2A",
            "zeroline": False,
            "showticklabels": False,
        },
        yaxis={
            "showgrid": True,
            "gridcolor": "#1A1D2A",
            "zeroline": False,
        },
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
    )


# =========================================================
# BOTTOM SECTION
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

bottom1, bottom2, bottom3 = st.columns([1, 1, 1])


# =========================================================
# TOP MOVERS
# =========================================================

with bottom1:

    st.markdown(
        """
<div class="card">

<div class="card-title">
Top Movers in Watchlist
</div>

<br>

<div style="
padding:10px 0;
border-bottom:1px solid #1C1F2C;
">

<b>🟢 NVDA</b>

<span style="
float:right;
color:#23D982;
">
+6.82%
</span>

<br>

<small style="color:#777B8D;">
NVIDIA Corporation
</small>

</div>

<div style="
padding:10px 0;
border-bottom:1px solid #1C1F2C;
">

<b>⚪ AAPL</b>

<span style="
float:right;
color:#23D982;
">
+1.25%
</span>

<br>

<small style="color:#777B8D;">
Apple Inc.
</small>

</div>

<div style="
padding:10px 0;
border-bottom:1px solid #1C1F2C;
">

<b>🔴 TSLA</b>

<span style="
float:right;
color:#FF456A;
">
-3.42%
</span>

<br>

<small style="color:#777B8D;">
Tesla, Inc.
</small>

</div>

<div style="padding:10px 0;">

<b>🟠 AMZN</b>

<span style="
float:right;
color:#23D982;
">
+2.18%
</span>

<br>

<small style="color:#777B8D;">
Amazon.com, Inc.
</small>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# ATTENTION TREND
# =========================================================

with bottom2:

    st.markdown(
        """
<div class="card">

<div class="card-title">
Attention Score Trend
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    trend_x = [
        "May 10",
        "May 11",
        "May 12",
        "May 13",
        "May 14",
        "May 15",
        "May 16",
        "May 17",
        "May 18",
        "May 20",
    ]

    trend_y = [
        75, 52, 27, 66, 58,
        64, 44, 59, 76, 70
    ]

    trend = go.Figure()

    trend.add_trace(
        go.Scatter(
            x=trend_x,
            y=trend_y,
            mode="lines+markers",
            line={
                "color": "#FF4C99",
                "width": 3,
            },
            marker={
                "color": "#FF4C99",
                "size": 7,
            },
            fill="tozeroy",
            fillcolor="rgba(255,76,153,0.10)",
        )
    )

    trend.update_layout(
        height=260,
        margin=dict(l=5, r=5, t=15, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#85889A"},
        xaxis={
            "gridcolor": "#1A1D2A",
        },
        yaxis={
            "range": [0, 100],
            "gridcolor": "#1A1D2A",
        },
        showlegend=False,
    )

    st.plotly_chart(
        trend,
        width="stretch",
        config={"displayModeBar": False},
    )


# =========================================================
# LATEST NEWS
# =========================================================

with bottom3:

    st.markdown(
        """
<div class="card">

<div class="card-title">

Latest News

<span style="
float:right;
color:#9B5CFF;
font-size:11px;
">
View all →
</span>

</div>

<div class="news-item">

<div class="news-title">
NVIDIA Surges on Strong Q1 Earnings
</div>

<div class="news-source">
Reuters • 2m ago
</div>

</div>

<div class="news-item">

<div class="news-title">
AI Chip Demand Drives NVIDIA Stock Higher
</div>

<div class="news-source">
Bloomberg • 45m ago
</div>

</div>

<div class="news-item">

<div class="news-title">
NVIDIA Partners with Tech Giants for AI...
</div>

<div class="news-source">
CNBC • 1h ago
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div style="
text-align:center;
color:#55596B;
font-size:10px;
margin-top:25px;
padding-bottom:10px;
">
MarketPulse © 2026. Smart Market Intelligence.
</div>
""",
    unsafe_allow_html=True,
)
