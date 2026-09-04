import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from api import (
    get_watchlist,
    get_stock_history,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MarketPulse History",
    page_icon="🕐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================
# NOTE: every line below starts at column 0 on purpose.
# Streamlit's st.markdown() runs content through a Markdown
# parser first. In Markdown, any line indented 4+ spaces is
# treated as a preformatted code block and printed as literal
# text instead of being rendered as HTML/CSS. Keeping every
# line flush-left (including nested rules) avoids that trap.

CUSTOM_CSS = """
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

.history-item {
padding: 15px 0;
border-bottom: 1px solid #1C1F2C;
}

.history-symbol {
color: #FFFFFF;
font-size: 14px;
font-weight: 700;
}

.history-date {
color: #777B8D;
font-size: 10px;
margin-top: 4px;
}

.history-description {
color: #A5A7B5;
font-size: 11px;
margin-top: 6px;
line-height: 1.5;
}

.positive {
color: #23D982;
}

.negative {
color: #FF456A;
}

.attention-high {
display: inline-block;
padding: 6px 12px;
border-radius: 20px;
border: 1px solid #9B5CFF;
color: #B47CFF;
background: rgba(155, 92, 255, 0.08);
font-size: 10px;
font-weight: 700;
}

.attention-medium {
display: inline-block;
padding: 6px 12px;
border-radius: 20px;
border: 1px solid #D89B35;
color: #E8B85C;
background: rgba(216, 155, 53, 0.08);
font-size: 10px;
font-weight: 700;
}

.attention-low {
display: inline-block;
padding: 6px 12px;
border-radius: 20px;
border: 1px solid #3B4356;
color: #85889A;
background: rgba(59, 67, 86, 0.10);
font-size: 10px;
font-weight: 700;
}

.stSelectbox > div > div {
background: #0B0E18;
border-color: #282B3B;
color: #FFFFFF;
}

.stDateInput > div > div > input {
background: #0B0E18;
color: #FFFFFF;
border-color: #282B3B;
}

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

footer {
visibility: hidden;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">'
        '<div class="brand-icon">〽</div>'
        '<div>'
        '<div class="brand-name">MarketPulse</div>'
        '<div class="brand-subtitle">Smart Market Intelligence</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-item">▦ &nbsp; Dashboard</div>'
        '<div class="side-item">☆ &nbsp; Watchlist</div>'
        '<div class="side-item">◔ &nbsp; Stock Details</div>'
        '<div class="side-item">♧ &nbsp; Alerts</div>'
        '<div class="side-item">▤ &nbsp; News</div>'
        '<div class="side-item active">◷ &nbsp; History</div>'
        '<div class="side-item">▥ &nbsp; Analytics</div>'
        '<hr style="border-color:#202333;">'
        '<div class="side-item">⚙ &nbsp; Settings</div>'
        '<div class="side-item">? &nbsp; Help &amp; Support</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="upgrade-card">'
        '<div style="font-size:30px;">♛</div>'
        '<div class="upgrade-title">Upgrade to Pro</div>'
        '<div class="upgrade-text">'
        'Unlock advanced analytics,<br>more alerts &amp; AI insights.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.toggle("Dark Mode", value=True)


# =========================================================
# MARKET STATUS
# =========================================================

st.markdown(
    '<div style="color:#35DB8A;font-size:12px;margin-bottom:8px;">'
    '● Market is Open'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# PAGE HEADER
# =========================================================

header_left, header_right = st.columns([3, 1])

with header_left:

    st.markdown(
        '<div class="page-title">Activity History</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'See what changed in your watchlist over time'
        '</div>',
        unsafe_allow_html=True,
    )


with header_right:

    st.button(
        "↻ Refresh",
        width="stretch",
    )


# =========================================================
# FILTERS
# =========================================================
watchlist = get_watchlist()
filter1, filter2, filter3 = st.columns([1, 1, 1])

with filter1:

    stock_options = ["All Stocks"]

    if isinstance(watchlist, list):
        stock_options += [
            stock.get("symbol")
            for stock in watchlist
            if stock.get("symbol")
        ]

    selected_stock = st.selectbox(
        "Stock",
        stock_options
    )

with filter2:

    selected_period = st.selectbox(
        "Period",
        [
            "Last 7 Days",
            "Last 30 Days",
            "Last 3 Months",
        ],
    )

with filter3:

    selected_event = st.selectbox(
        "Event Type",
        [
            "All Events",
            "Price Movement",
            "Volume Change",
            "News",
            "Attention Score",
        ],
    )


st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# LOAD HISTORY DATA
# =========================================================

HISTORY_ITEMS = []

if isinstance(watchlist, list):

    for stock in watchlist:

        symbol = stock.get("symbol")

        if not symbol:
            continue

        history = get_stock_history(symbol)

        if not isinstance(history, list):
            continue

        for snapshot in history:

            price = snapshot.get("price", 0)
            previous_close = snapshot.get("previous_close", 0)

            price_change = 0

            if previous_close:
                price_change = (
                    (price - previous_close)
                    / previous_close
                ) * 100

            HISTORY_ITEMS.append({
                "symbol": symbol,
                "time": snapshot.get("timestamp", ""),
                "change": round(price_change, 2),
                "volume": snapshot.get("volume", 0),
                "news_count": snapshot.get("news_count", 0),
                "attention": "MEDIUM"
            })


HISTORY_ITEMS.sort(
    key=lambda x: x["time"],
    reverse=True
)


if selected_stock != "All Stocks":

    HISTORY_ITEMS = [
        item
        for item in HISTORY_ITEMS
        if item["symbol"] == selected_stock
    ]


# =========================================================
# SUMMARY CARDS
# =========================================================

s1, s2, s3, s4 = st.columns(4)

total_events = len(HISTORY_ITEMS)

price_changes = sum(
    1 for item in HISTORY_ITEMS
    if item["change"] != 0
)

high_attention = sum(
    1 for item in HISTORY_ITEMS
    if abs(item["change"]) >= 5
)

summary = [

    ("Total Events", str(total_events), "Tracked changes"),
    ("Price Changes", str(price_changes), "Detected movements"),
    (
        "News Events",
        str(sum(item.get("news_count", 0) for item in HISTORY_ITEMS)),
        "New articles",
    ),
    ("High Attention", str(high_attention), "Important signals"),

]

for col, (title, number, description) in zip(
    [s1, s2, s3, s4],
    summary,
):

    with col:

        st.markdown(
            f'<div class="card">'
            f'<div style="color:#85889A;font-size:11px;">{title}</div>'
            f'<div style="color:#FFFFFF;font-size:27px;font-weight:700;'
            f'margin-top:8px;">{number}</div>'
            f'<div style="color:#9B5CFF;font-size:10px;margin-top:5px;">'
            f'{description}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# HISTORY + TREND
# =========================================================

history_col, trend_col = st.columns([1.15, 1])


# =========================================================
# HISTORY LIST
# =========================================================

# Load real history from PostgreSQL


with history_col:

    rows_html = '<div class="card"><div class="card-title">Recent Activity</div>'

    if not HISTORY_ITEMS:
        rows_html += (
            '<div class="history-item">'
            '<div class="history-description">'
            'No activity history available yet.'
            '</div>'
            '</div>'
        )

    for item in HISTORY_ITEMS[:10]:

        change = item["change"]

        if change > 0:
            change_class = "positive"
            change_text = f"+{change:.2f}%"
        elif change < 0:
            change_class = "negative"
            change_text = f"{change:.2f}%"
        else:
            change_class = ""
            change_text = "0.00%"

        timestamp = item["time"]

        try:
            from datetime import datetime

            dt = datetime.fromisoformat(timestamp)

            date_text = dt.strftime("%b %d • %I:%M %p")

        except Exception:
            date_text = str(timestamp)

        description = (
            f"Price changed by {change_text} "
            f"from the previous market close."
        )

        rows_html += (
            '<div class="history-item">'
            '<div style="display:flex;justify-content:space-between;">'
            '<div>'
            f'<div class="history-symbol">{item["symbol"]}</div>'
            f'<div class="history-date">{date_text}</div>'
            '</div>'
            f'<div class="{change_class}">{change_text}</div>'
            '</div>'
            f'<div class="history-description">{description}</div>'
            '<br>'
            '<span class="attention-medium">● MEDIUM ATTENTION</span>'
            '</div>'
        )

    rows_html += '</div>'

    st.markdown(rows_html, unsafe_allow_html=True)

# =========================================================
# ATTENTION TREND
# =========================================================

with trend_col:

    st.markdown(
        '<div class="card">'
        '<div class="card-title">Attention Score History</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Build attention trend from real history
    
    trend_x = []
    trend_y = []

    for item in HISTORY_ITEMS:
        timestamp = item.get("time", "")
        change = abs(item.get("change", 0))

        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp)
            time_label = dt.strftime("%b %d • %I:%M %p")
        except Exception:
            continue

        # Calculate attention score from price movement
        if change >= 5:
            score = 40
        elif change >= 2:
            score = 25
        elif change >= 1:
            score = 10
        else:
            score = 0

        trend_x.append(time_label)
        trend_y.append(score)

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
            hovertemplate="Score: %{y}<extra></extra>",
        )
    )

    trend.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "#85889A"
        },
        xaxis={
            "gridcolor": "#1A1D2A",
            "zeroline": False,
        },
        yaxis={
            "range": [0, 100],
            "gridcolor": "#1A1D2A",
            "zeroline": False,
        },
        showlegend=False,
    )

    st.plotly_chart(
        trend,
        width="stretch",
        config={"displayModeBar": False},
    )


# =========================================================
# CHANGE BREAKDOWN
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns(2)


# =========================================================
# EVENT BREAKDOWN
# =========================================================

BREAKDOWN_ROWS = [
    (
        "Price Movements",
        str(sum(1 for item in HISTORY_ITEMS if item.get("change", 0) != 0)),
        "#FFFFFF",
    ),
    (
        "Volume Changes",
        str(sum(1 for item in HISTORY_ITEMS if item.get("volume", 0) > 0)),
        "#FFFFFF",
    ),
    (
        "News Events",
        str(
            sum(
                item.get("news_count", 0)
                for item in HISTORY_ITEMS
            )
        ),
        "#FFFFFF",
    ),
    (
        "High Attention",
        str(sum(1 for item in HISTORY_ITEMS if abs(item.get("change", 0)) >= 5)),
        "#B47CFF",
    ),
]

with left:

    breakdown_html = '<div class="card"><div class="card-title">Event Breakdown</div><br>'

    for i, (label, value, color) in enumerate(BREAKDOWN_ROWS):
        border = "border-bottom:1px solid #1C1F2C;" if i < len(BREAKDOWN_ROWS) - 1 else ""
        breakdown_html += (
            f'<div style="display:flex;justify-content:space-between;'
            f'padding:13px 0;{border}">'
            f'<span style="color:#A5A7B5;">{label}</span>'
            f'<span style="color:{color};">{value}</span>'
            f'</div>'
        )

    breakdown_html += '</div>'

    st.markdown(breakdown_html, unsafe_allow_html=True)


# =========================================================
# LATEST CHANGE
# =========================================================

with right:

    st.markdown(
        '<div class="card">'
        '<div class="card-title">Latest Significant Change</div>',
        unsafe_allow_html=True,
    )

    if HISTORY_ITEMS:

        latest = max(
            HISTORY_ITEMS,
            key=lambda x: x.get("time", "")
        )

        symbol = latest.get("symbol", "N/A")
        change = latest.get("change", 0)

        if change > 0:
            change_text = f"+{change:.2f}%"
            change_color = "#23D982"
        elif change < 0:
            change_text = f"{change:.2f}%"
            change_color = "#FF5C5C"
        else:
            change_text = "0.00%"
            change_color = "#85889A"

        if abs(change) >= 5:
            attention = "HIGH"
            score = 40
            attention_class = "attention-high"
        elif abs(change) >= 2:
            attention = "MEDIUM"
            score = 25
            attention_class = "attention-medium"
        else:
            attention = "LOW"
            score = 10
            attention_class = "attention-low"

        st.markdown(
            f'<div style="color:#FFFFFF;font-size:19px;font-weight:700;">'
            f'{symbol}</div>'
            f'<div style="color:#85889A;font-size:11px;margin-top:4px;">'
            f'Recent market activity</div>'
            f'<br>'
            f'<div style="color:{change_color};font-size:25px;font-weight:700;">'
            f'{change_text}</div>'
            f'<div style="color:#85889A;font-size:11px;margin-top:4px;">'
            f'Price movement from previous market close</div>'
            f'<br>'
            f'<div style="background:#0B0E18;border:1px solid #202333;'
            f'border-radius:9px;padding:14px;color:#A5A7B5;font-size:11px;'
            f'line-height:1.6;">'
            f'{symbol} recorded a {change_text} price movement in the latest '
            f'snapshot.</div>'
            f'<br>'
            f'<span class="{attention_class}">● {attention} ATTENTION • '
            f'{score}/100</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            '<div style="color:#85889A;font-size:12px;'
            'padding:20px 0;">'
            'No significant changes available yet.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div style="text-align:center;color:#55596B;font-size:10px;'
    'margin-top:35px;padding-bottom:10px;">'
    'MarketPulse © 2026. Smart Market Intelligence.'
    '</div>',
    unsafe_allow_html=True,
)
