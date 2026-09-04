import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MarketPulse",
    page_icon="📈",
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
# line flush-left avoids that trap entirely.

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

.home-icon {
font-size: 55px;
color: #9B5CFF;
text-align: center;
margin-top: 45px;
}

.home-title {
font-size: 48px;
font-weight: 800;
color: #FFFFFF;
text-align: center;
margin-top: 10px;
}

.home-highlight {
color: #9B5CFF;
}

.home-subtitle {
color: #85889A;
font-size: 16px;
max-width: 650px;
margin: 15px auto 45px auto;
line-height: 1.7;
text-align: center;
}

.feature-card {
background:
linear-gradient(
145deg,
rgba(18, 21, 34, 0.98),
rgba(9, 11, 20, 0.98)
);
border: 1px solid #202333;
border-radius: 13px;
padding: 25px;
min-height: 180px;
}

.feature-icon {
color: #9B5CFF;
font-size: 25px;
}

.feature-title {
color: #FFFFFF;
font-size: 15px;
font-weight: 700;
margin-top: 12px;
}

.feature-text {
color: #85889A;
font-size: 12px;
line-height: 1.6;
margin-top: 7px;
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

    # Brand
    st.markdown(
        '<div class="brand">'
        '<div class="brand-icon">〽</div>'
        '<div class="brand-name">MarketPulse</div>'
        '<div class="brand-subtitle">Smart Market Intelligence</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Navigation
    if st.button("▦  Dashboard", width="stretch"):
        st.switch_page("pages/1_📊_Dashboard.py")

    if st.button("☆  Watchlist", width="stretch"):
        st.switch_page("pages/Watchlist.py")

    if st.button("◔  Stock Details", width="stretch"):
        st.switch_page("pages/3_📈_Stock_Details.py")

    if st.button("◷  History", width="stretch"):
        st.switch_page("pages/4_🕐_History.py")

    st.markdown("---")

    # Other sections
    st.markdown("**More**")

    st.write("♧  Alerts")
    st.write("▤  News")
    st.write("▥  Analytics")

    st.markdown("---")

    st.write("⚙  Settings")
    st.write("?  Help & Support")

    # Upgrade card
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
# HOME HEADER
# =========================================================

st.markdown('<div class="home-icon">〽</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="home-title">'
    'Welcome to <span class="home-highlight">MarketPulse</span>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="home-subtitle">'
    'Smart market intelligence that watches your stocks, '
    'detects meaningful changes, and explains '
    'what deserves your attention.'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# FEATURES
# =========================================================

c1, c2, c3 = st.columns(3)


# -------------------------
# FEATURE 1
# -------------------------

with c1:
    st.markdown(
        '<div class="feature-card">'
        '<div class="feature-icon">♧</div>'
        '<div class="feature-title">Smart Watchlist</div>'
        '<div class="feature-text">'
        'Track your favorite stocks and automatically detect '
        'important changes since your last visit.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# -------------------------
# FEATURE 2
# -------------------------

with c2:
    st.markdown(
        '<div class="feature-card">'
        '<div class="feature-icon">♨</div>'
        '<div class="feature-title">Attention Score</div>'
        '<div class="feature-text">'
        'Understand which stocks deserve attention using '
        'price movement, volume and news signals.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# -------------------------
# FEATURE 3
# -------------------------

with c3:
    st.markdown(
        '<div class="feature-card">'
        '<div class="feature-icon">▣</div>'
        '<div class="feature-title">Market Intelligence</div>'
        '<div class="feature-text">'
        'Get a clear explanation of why a stock is appearing '
        'on your radar.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# QUICK START
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 🚀 Get Started")

st.write(
    "Add stocks to your watchlist and let MarketPulse "
    "track meaningful changes for you."
)

if st.button("☆  Open Watchlist", width="stretch"):
    st.switch_page("pages/Watchlist.py")

# =========================================================
# MARKET IMAGES
# =========================================================

st.markdown(
    "<div style='margin-top:55px;margin-bottom:25px;'>"
    "<h3 style='color:#FFFFFF;text-align:center;'>MarketPulse</h3>"
    "<p style='color:#85889A;text-align:center;font-size:12px;'>"
    "Stay informed. Track smarter. Understand the market."
    "</p>"
    "</div>",
    unsafe_allow_html=True,
)

img1, img2, img3 = st.columns(3)

with img1:
    st.image("frontend/assets/stock1.jpg", width="stretch")

with img2:
    st.image("frontend/assets/stock2.jpg", width="stretch")

with img3:
    st.image("frontend/assets/stock3.jpg", width="stretch")




# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div style="text-align:center;color:#55596B;font-size:10px;'
    'margin-top:70px;padding:25px 10px 15px 10px;'
    'border-top:1px solid #1C1F2C;">'
    
    '<div style="color:#85889A;font-size:12px;margin-bottom:8px;">'
    '<b style="color:#FFFFFF;">MarketPulse</b> '
    '• Smart Market Intelligence'
    '</div>'
    
    '<div style="color:#55596B;font-size:10px;line-height:1.8;">'
    'Track meaningful market changes • Monitor volume • '
    'Stay informed with AI-powered insights'
    '</div>'
    
    '<div style="margin-top:12px;">'
    'MarketPulse © 2026. Smart Market Intelligence.'
    '</div>'
    
    '</div>',
    unsafe_allow_html=True,
)
