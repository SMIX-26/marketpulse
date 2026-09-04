# 📈 MarketPulse — Smart Market Watchlist

> **An intelligent stock watchlist that detects meaningful market changes, monitors news and trading activity, and uses AI to explain why a stock deserves your attention.**

MarketPulse is a full-stack **Smart Market Watchlist** application designed to help users monitor stocks without constantly checking charts and financial websites.

Instead of simply displaying stock prices, MarketPulse focuses on **what changed since the user's last visit**.

It combines:

* 📊 Real-time stock market data
* 📈 Price movement detection
* 📉 Trading volume analysis
* 📰 News monitoring
* 🎯 Attention Score
* 🤖 AI-powered explanations
* 🕐 Historical activity tracking
* ⭐ Personalized watchlist management

The goal is simple:

> **Don't just show me the market. Tell me what changed and why it matters.**

---

## ✨ Key Features

### ⭐ Smart Watchlist

Users can create a personalized list of stocks they want to monitor.

Each watchlist stock provides:

* Current price
* Daily price movement
* Price movement since the previous visit
* Trading volume
* Volume compared with normal activity
* New news events
* Attention Score
* AI-generated explanation

---

### 📊 Real-Time Market Data

MarketPulse uses **Yahoo Finance (`yfinance`)** to retrieve market information.

The application tracks:

* Current stock price
* Previous closing price
* Current trading volume
* Historical average volume
* Price percentage change
* Volume ratio

Example:

```text
NVDA

Current Price: $XXX.XX
Price Change: +6.8%
Volume: 2.4× normal
News Events: 3

Attention: HIGH
Score: 100/100
```

---

### 🔍 Change Detection

MarketPulse doesn't only look at the current stock price.

It stores snapshots of stocks when users view them and compares the latest market information with the previous snapshot.

This allows the application to identify:

* Significant price movement
* Changes in trading activity
* Increased market attention
* New events since the user's previous visit

---

### 📈 Unusual Volume Detection

Trading volume is compared against recent historical market activity.

MarketPulse calculates:

```text
Volume Ratio = Current Volume / Average Historical Volume
```

For example:

```text
2.0× normal volume
```

means the stock is currently trading at approximately twice its normal volume.

Volume signals contribute to the stock's overall Attention Score.

---

### 📰 News Monitoring

MarketPulse retrieves stock-related news using Yahoo Finance.

News events are stored in PostgreSQL so that the application can determine how many new articles appeared since the user's previous visit.

The system tracks:

* News title
* Description
* Source URL
* Publication timestamp
* Associated stock symbol

---

### 🎯 Attention Score

Every stock receives an **Attention Score from 0–100**.

The score combines multiple signals:

| Signal                     | Condition     | Score |
| -------------------------- | ------------- | ----: |
| Significant price movement | ≥ 5%          |   +40 |
| Notable price movement     | ≥ 2%          |   +25 |
| Small price movement       | ≥ 1%          |   +10 |
| Unusually high volume      | ≥ 2× normal   |   +35 |
| Higher volume              | ≥ 1.5× normal |   +20 |
| Increased volume           | ≥ 1.2× normal |   +10 |
| 3+ news events             | New events    |   +25 |
| News event                 | 1–2 events    |   +10 |

The final score is capped at **100**.

### Attention Levels

```text
70–100 → HIGH
40–69  → MEDIUM
0–39   → LOW
```

The score is designed as an **attention signal**, not an investment recommendation.

---

### 🤖 AI-Powered Market Explanation

MarketPulse uses the **Google Gemini API** to generate simple explanations of detected market activity.

The AI receives structured information such as:

```text
Stock
Price change
Volume ratio
Number of new news events
Attention level
```

It then generates a concise explanation.

Example:

> JPM experienced minimal price movement with trading volume below its normal level. With no new news events detected, overall market attention remains low.

The AI is explicitly instructed to:

* Explain the available data
* Use simple language
* Avoid inventing events
* Avoid investment advice
* Never recommend buying or selling stocks

---

### 🕐 Activity History

MarketPulse maintains a historical record of stock snapshots.

The History page provides:

* Total tracked events
* Price changes
* News events
* High-attention events
* Recent activity
* Attention score history
* Event breakdown
* Latest significant market change

The attention trend is visualized using an interactive Plotly chart.

---

### 📊 Stock Details

The Stock Details page provides a deeper view of an individual stock.

It includes:

* Current price
* Daily change
* Attention information
* Historical price chart
* Stock-related news

---

### 🎨 Dark FinTech UI

The frontend uses a dark financial dashboard design with:

* Charcoal/black background
* Purple accents
* Green positive indicators
* Red negative indicators
* Interactive charts
* Responsive Streamlit layout
* Clean financial dashboard cards

The application is built using **native Streamlit components** with custom CSS for visual styling.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │       User / Browser    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Streamlit Frontend    │
                    │                         │
                    │ Dashboard               │
                    │ Watchlist               │
                    │ Stock Details           │
                    │ Activity History        │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP Requests
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │                         │
                    │ Stock APIs              │
                    │ Watchlist APIs          │
                    │ Change Detection        │
                    │ Attention Engine        │
                    │ Snapshot Service        │
                    │ News Service            │
                    │ AI Explanation          │
                    └──────┬─────────┬────────┘
                           │         │
                 ┌─────────┘         └──────────┐
                 ▼                              ▼
      ┌─────────────────────┐        ┌─────────────────────┐
      │ PostgreSQL Database │        │   External APIs     │
      │                     │        │                     │
      │ Users               │        │ Yahoo Finance       │
      │ Watchlists          │        │ Google Gemini       │
      │ Snapshots           │        │                     │
      │ News Events         │        └─────────────────────┘
      └─────────────────────┘
```

---

# 🧠 How MarketPulse Works

The application follows a simple pipeline.

### 1. User adds a stock

Example:

```text
AAPL
```

The stock is added to the user's watchlist.

---

### 2. Market data is retrieved

MarketPulse retrieves:

```text
Current Price
Previous Close
Current Volume
Historical Volume
```

---

### 3. News is retrieved

Yahoo Finance news is checked for new stock-related events.

---

### 4. Previous snapshot is retrieved

MarketPulse checks the PostgreSQL database for the stock's previous snapshot.

---

### 5. Changes are calculated

The system calculates:

```text
Price Change
Volume Change
Volume Ratio
New News Count
```

---

### 6. Attention Score is calculated

The Attention Engine combines the signals.

```text
Price Movement
       +
Volume Activity
       +
News Events
       ↓
Attention Score
       ↓
LOW / MEDIUM / HIGH
```

---

### 7. AI explanation is generated

Gemini receives the detected signals and generates a short human-readable explanation.

---

### 8. User sees the result

The user gets a concise explanation instead of having to manually analyze multiple data sources.

---

# 🗂️ Project Structure

```text
marketpulse/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── stocks.py
│   │       ├── watchlist.py
│   │       ├── changes.py
│   │       └── history.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── market_service.py
│   │   ├── news_service.py
│   │   ├── news_storage.py
│   │   ├── change_detector.py
│   │   ├── attention_engine.py
│   │   ├── snapshot_service.py
│   │   └── ai_explanation.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── crud.py
│   │
│   └── schemas/
│       ├── __init__.py
│       ├── stock.py
│       └── watchlist.py
│
├── frontend/
│   ├── app.py
│   ├── api.py
│   │
│   ├── pages/
│   │   ├── 1_📊_Dashboard.py
│   │   ├── 2_⭐_Watchlist.py
│   │   ├── 3_📈_Stock_Details.py
│   │   └── 4_🕐_History.py
│   │
│   └── components/
│       ├── __init__.py
│       ├── stock_card.py
│       ├── metrics.py
│       └── charts.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

## Frontend

* **Streamlit**
* **Python**
* **Plotly**
* **CSS**

## Backend

* **FastAPI**
* **Python**
* **Uvicorn**
* **Requests**

## Database

* **PostgreSQL**
* **SQLAlchemy**
* **psycopg2**

## Market Data

* **Yahoo Finance**
* **yfinance**

## Artificial Intelligence

* **Google Gemini API**
* **google-genai**

## Development & Deployment

* **Git**
* **GitHub**
* **Render**
* **Streamlit Community Cloud**

---

# 🗄️ Database Design

MarketPulse uses PostgreSQL with the following core tables.

### Users

Stores application users/devices.

```text
users
├── id
├── device_id
└── created_at
```

---

### Watchlists

Stores stocks associated with users.

```text
watchlists
├── id
├── user_id
├── symbol
├── company_name
├── created_at
└── last_viewed_at
```

A unique constraint prevents the same stock from being added multiple times for a user.

---

### Stock Snapshots

Stores market information captured when a stock is viewed.

```text
stock_snapshots
├── id
├── watchlist_id
├── symbol
├── price
├── previous_close
├── volume
└── timestamp
```

---

### News Events

Stores detected stock-related news.

```text
news_events
├── id
├── symbol
├── title
├── description
├── url
├── published_at
└── created_at
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /health
```

Returns:

```json
{
  "status": "healthy"
}
```

---

## Get Stock Data

```http
GET /stocks/{symbol}
```

Example:

```http
GET /stocks/AAPL
```

Returns current market information including:

* Price
* Previous close
* Volume
* Daily price change
* Average volume
* Volume ratio
* Volume change

---

## Get Watchlist

```http
GET /watchlist/
```

Returns the user's watchlist.

---

## Add Stock

```http
POST /watchlist/
```

Parameters:

```text
symbol
company_name
```

---

## Remove Stock

```http
DELETE /watchlist/{symbol}
```

Example:

```http
DELETE /watchlist/AAPL
```

---

## Get Stock Changes

```http
GET /changes/{symbol}
```

Returns:

* Current price
* Price movement
* Volume movement
* Volume ratio
* Previous snapshot
* News count
* Attention Score
* Attention level
* AI explanation
* Last viewed timestamp

---

## Mark Stock as Viewed

```http
POST /changes/{symbol}/view
```

Creates a stock snapshot and updates the last-viewed timestamp.

---

## Get Stock History

```http
GET /history/{symbol}
```

Returns historical snapshots stored for the stock.

---

# ⚙️ Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/SMIX-26/marketpulse.git
cd marketpulse
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_string
GOOGLE_API_KEY=your_gemini_api_key
```

### Important

Never commit `.env` to GitHub.

The repository already includes `.env` in `.gitignore`.

---

# ▶️ Running the Application Locally

## Start FastAPI

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start Streamlit

Open another terminal:

```bash
streamlit run frontend/app.py
```

The Streamlit application will open in your browser.

---

# 🌐 Deployment

MarketPulse uses separate deployment services for the backend and frontend.

### Backend

The FastAPI backend is deployed on:

**Render**

The backend connects to:

* Render PostgreSQL
* Google Gemini API
* Yahoo Finance

---

### Frontend

The Streamlit frontend is deployed using:

**Streamlit Community Cloud**

The frontend communicates with the deployed FastAPI backend through the backend API URL.

---

# 🔐 Environment Variables

The backend requires:

```text
DATABASE_URL
GOOGLE_API_KEY
```

These values should be configured through the deployment platform's environment/secrets settings.

Never expose API keys in source code.

---

# 📊 Example MarketPulse Insight

Suppose a stock has:

```text
Price Change: +6.8%
Volume Ratio: 2.4× normal
New News Events: 3
```

The Attention Engine detects:

```text
+40 → Significant price movement
+35 → Unusually high volume
+25 → Multiple new news events
--------------------------------
100 → HIGH ATTENTION
```

The user then receives an AI explanation based strictly on those signals.

This allows the user to understand **why the stock is being highlighted** without manually analyzing several indicators.

---

# 🎯 Design Philosophy

MarketPulse is built around three principles.

### 1. Signal over noise

Instead of overwhelming users with financial data, the application highlights meaningful changes.

### 2. Explainability

Every attention signal should have a reason.

Users should understand:

```text
What changed?
       ↓
How significant was it?
       ↓
Why is it getting attention?
```

### 3. No investment advice

MarketPulse is designed as a **market monitoring and information tool**, not a financial advisor.

It does not make:

* Buy recommendations
* Sell recommendations
* Hold recommendations
* Price predictions

---

# ⚠️ Limitations

### 1. Yahoo Finance Dependency

Market data and news depend on Yahoo Finance availability and the behavior of the `yfinance` library.

API behavior can change over time.

---

### 2. Snapshot-Based Change Detection

The current implementation compares the latest market information against stored snapshots.

It is not a professional-grade tick-by-tick market monitoring system.

---

### 3. Free-Tier Deployment

The application uses free deployment infrastructure.

The backend can sleep after inactivity, which may cause a delay when the first request wakes the service.

---

### 4. News Detection

News detection depends on the availability and timestamps of Yahoo Finance news data.

A missing or unavailable publication timestamp may prevent an article from being counted as a new event.

---

### 5. AI Reliability

AI-generated explanations are based on the structured information provided to Gemini.

Although prompts are designed to prevent fabricated information and financial recommendations, AI output should still be treated as an explanation layer rather than authoritative financial analysis.

---

### 6. Demo User Model

The current implementation uses a demo device/user identifier for watchlist management rather than a full authentication system.

---

# 🚀 Future Improvements

Possible future enhancements include:

* 🔐 User authentication and account management
* 🔔 Push/email notifications
* 📱 Mobile-friendly PWA
* 🧠 More advanced anomaly detection
* 📊 Technical indicators such as RSI, MACD and moving averages
* 📰 Better news sentiment analysis
* 🧩 Multiple news providers
* ⚡ WebSocket-based live market updates
* 🗃️ Improved historical event storage
* 🧠 AI-generated event summaries using actual article content
* 📈 Portfolio tracking
* 🔔 Custom user-defined alerts
* 🌎 Multiple market support
* 📊 Advanced comparative stock analysis
* 🧪 Automated backend/API tests
* 📦 Production-grade database migrations

---

# 🧪 Testing

The backend can be tested through FastAPI's interactive documentation:

```text
/docs
```

Example:

```http
GET /health
GET /stocks/AAPL
GET /watchlist/
GET /changes/AAPL
GET /history/AAPL
```

The application was also tested against PostgreSQL database operations including:

* Creating watchlists
* Removing watchlist stocks
* Saving stock snapshots
* Retrieving history
* Storing news events
* Detecting price changes
* Calculating attention scores
* Generating AI explanations

---

# 🏆 Hackathon Value Proposition

Traditional stock watchlists mostly answer:

> **"What is the current price?"**

MarketPulse aims to answer a more useful question:

> **"What changed since I last checked, and why should I pay attention?"**

By combining market data, volume analysis, news monitoring, historical snapshots, scoring logic, and generative AI, MarketPulse turns raw financial information into a concise and explainable market-monitoring experience.

---

# 👩‍💻 Author

**Samikshya Jena**

B.Tech — Computer Science & Engineering

---

# 📄 License

This project is intended for educational, experimental, and hackathon purposes.

---

## ⭐ If you find MarketPulse interesting

Give the repository a ⭐ on GitHub and feel free to explore or extend the project.

**MarketPulse — Smart Market Intelligence, explained simply.**

