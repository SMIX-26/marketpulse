# 📈 MarketPulse — Smart Market Watchlist

> **Groww Hackathon Submission — Smart & Explainable Stock Monitoring**

MarketPulse is an intelligent stock watchlist that helps users understand **what changed since their last visit and why it matters**.

Instead of simply displaying stock prices, MarketPulse monitors changes in **price, trading volume, news activity, and attention level**, then generates a concise AI-powered explanation using Google Gemini.

The goal is to reduce information overload and answer a simple question:

> **"What changed in my watchlist, and why should I pay attention?"**

---

## 🚀 Live Demo

**Frontend:** Deployed using Streamlit Community Cloud
**Backend:** Deployed using Render

> Add your final deployed URLs here before submission.

* 🌐 Frontend: `YOUR_STREAMLIT_URL`
* ⚡ Backend API: `YOUR_RENDER_URL`
* 📚 API Documentation: `YOUR_RENDER_URL/docs`

---

## 🎯 Problem Statement

Traditional stock watchlists mainly show current prices and percentage changes. Users still have to manually compare the current state with their previous visit and investigate multiple sources to understand what happened.

MarketPulse solves this by providing:

* Change detection since the user's previous visit
* Trading-volume anomaly detection
* New-news detection
* A transparent Attention Score
* AI-generated explanations
* Historical activity tracking

This transforms a passive watchlist into a **change-aware market monitoring system**.

---

# ✨ Key Features

### ⭐ Smart Watchlist

Users can add and remove stocks from their personal watchlist.

Each stock provides:

* Current price
* Daily price movement
* Price movement since last visit
* Trading volume
* Volume compared with normal levels
* New news events
* Attention Score
* AI-generated explanation

---

### 🔍 Change Detection

MarketPulse stores a snapshot when a stock is marked as viewed.

When the user returns, the system compares the latest market data with the previous snapshot.

```text
Previous Visit
      ↓
Snapshot Stored
      ↓
User Returns
      ↓
Fetch Current Data
      ↓
Compare With Previous Snapshot
      ↓
Detect Meaningful Changes
```

---

### 📊 Attention Score

A rule-based scoring engine combines multiple signals:

| Signal                     |     Condition | Score |
| -------------------------- | ------------: | ----: |
| Significant price movement |          ≥ 5% |   +40 |
| Notable price movement     |          ≥ 2% |   +25 |
| Small price movement       |          ≥ 1% |   +10 |
| Very high volume           |   ≥ 2× normal |   +35 |
| Higher volume              | ≥ 1.5× normal |   +20 |
| Increased volume           | ≥ 1.2× normal |   +10 |
| 3+ new news events         |           ≥ 3 |   +25 |
| New news event             |           > 0 |   +10 |

The final score is capped at **100**.

### Attention Levels

```text
0–39     → LOW
40–69    → MEDIUM
70–100   → HIGH
```

The scoring system is intentionally **rule-based and transparent**, so users can understand why a stock received a particular attention level.

---

## 🤖 AI-Powered Explanation

MarketPulse uses the **Google Gemini API** to convert detected signals into a simple explanation.

Example:

> "JPM experienced minimal price movement, edging down just 0.06% on light trading volume. With no new news events reported, overall attention on the stock is currently low."

The AI is instructed to:

* Use only the provided data
* Keep explanations concise
* Avoid inventing events
* Avoid investment advice
* Never recommend buying or selling

The AI acts as an **explanation layer**, not a financial decision-making system.

---

# 🏗️ Architecture

MarketPulse follows a simple **frontend → REST API → services/database** architecture.

```text
                         ┌─────────────────────┐
                         │  Streamlit Frontend │
                         │                     │
                         │  Dashboard          │
                         │  Watchlist          │
                         │  Stock Details      │
                         │  Activity History   │
                         └──────────┬──────────┘
                                    │
                               REST API
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         ├─────────────────────┤
                         │ Watchlist Routes    │
                         │ Stock Routes        │
                         │ Changes Routes      │
                         │ History Routes      │
                         └───────┬──────┬──────┘
                                 │      │
                    ┌────────────┘      └─────────────┐
                    ▼                                 ▼
          ┌──────────────────┐              ┌──────────────────┐
          │   PostgreSQL     │              │ External Services│
          │                  │              │                  │
          │ Users            │              │ Yahoo Finance    │
          │ Watchlists       │              │ Google Gemini    │
          │ Snapshots        │              │                  │
          │ News Events      │              └──────────────────┘
          └──────────────────┘
```

---

# 🧩 Project Structure

```text
marketpulse/
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── stocks.py
│   │       ├── watchlist.py
│   │       ├── changes.py
│   │       └── history.py
│   │
│   ├── services/
│   │   ├── market_service.py
│   │   ├── news_service.py
│   │   ├── news_storage.py
│   │   ├── snapshot_service.py
│   │   ├── change_detector.py
│   │   ├── attention_engine.py
│   │   └── ai_explanation.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── crud.py
│   │
│   └── schemas/
│       ├── stock.py
│       └── watchlist.py
│
├── frontend/
│   ├── app.py
│   ├── api.py
│   │
│   ├── pages/
│   │   ├── Dashboard.py
│   │   ├── Watchlist.py
│   │   ├── Stock_Details.py
│   │   └── History.py
│   │
│   └── components/
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

# 🗄️ Database Design

MarketPulse uses PostgreSQL for persistent storage.

### Users

Stores application users/devices.

```text
users
├── id
├── device_id
└── created_at
```

### Watchlists

Stores stocks associated with a user.

```text
watchlists
├── id
├── user_id
├── symbol
├── company_name
├── created_at
└── last_viewed_at
```

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

### News Events

Stores detected news events.

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

# 🔄 How MarketPulse Works

## 1. Add Stock

The user adds a stock such as:

```text
NVDA
AAPL
MSFT
TSLA
```

The stock is stored in PostgreSQL.

---

## 2. View Stock

When the user views/marks a stock as viewed:

```text
Market Data
     ↓
Create Snapshot
     ↓
Store Price
Store Volume
Store Timestamp
     ↓
Update last_viewed_at
```

This creates the reference point for future comparisons.

---

## 3. User Returns Later

MarketPulse fetches the latest information.

The system compares:

```text
Current Snapshot
       vs
Previous Snapshot
```

It calculates:

* Price change
* Volume change
* Volume ratio
* New news events

---

## 4. Attention Engine

The detected signals are passed to the rule-based Attention Engine.

```text
Price Movement
      +
Volume Activity
      +
News Activity
      ↓
Attention Score
      ↓
LOW / MEDIUM / HIGH
```

---

## 5. AI Explanation

The detected information is passed to Gemini.

```text
Stock Signals
     ↓
Gemini
     ↓
Simple Explanation
```

The user therefore sees both:

**What happened?**

and

**Why does it matter?**

---

# 🌐 API Endpoints

| Method | Endpoint                 | Purpose                               |
| ------ | ------------------------ | ------------------------------------- |
| GET    | `/health`                | Backend health check                  |
| GET    | `/stocks/{symbol}`       | Get current stock data                |
| GET    | `/watchlist/`            | Get user's watchlist                  |
| POST   | `/watchlist/`            | Add a stock                           |
| DELETE | `/watchlist/{symbol}`    | Remove a stock                        |
| GET    | `/changes/{symbol}`      | Detect changes and generate attention |
| POST   | `/changes/{symbol}/view` | Save snapshot and mark stock viewed   |
| GET    | `/history/{symbol}`      | Retrieve stock history                |

FastAPI automatically provides interactive API documentation at:

```text
/docs
```

---

# 🛡️ Edge Cases Considered

The application handles several practical edge cases.

### No Previous Snapshot

If a user views a stock for the first time, there is no previous state for comparison.

The system treats it as:

```text
First Visit
→ No historical comparison
→ Establish baseline snapshot
```

---

### Duplicate Stock

A stock cannot be added to the same user's watchlist twice.

```text
NVDA
NVDA
```

The second request returns an appropriate error instead of creating a duplicate.

---

### Invalid Stock Symbol

Invalid or unavailable market symbols are handled by the backend and returned as API errors.

---

### No New News

If there are no new articles since the user's previous visit:

```text
News Events = 0
```

The stock can still receive attention based on price or volume movement.

---

### Gemini API Failure

AI generation is treated as an additional explanation layer.

If Gemini is unavailable, MarketPulse falls back to a deterministic explanation based on the market data instead of breaking the entire application.

---

### Market Data Failure

External market-data failures are handled by the backend rather than exposing raw exceptions directly to the user.

---

### Empty Watchlist

The frontend supports an empty watchlist state rather than assuming that stocks always exist.

---

### Duplicate News

News events are checked against existing records before being stored to reduce duplicate entries.

---

# ⚖️ Design Decisions & Trade-offs

The challenge explicitly required decisions around architecture and trade-offs.

## Streamlit instead of React

**Decision:** Use Streamlit for the frontend.

**Why:**

* Faster development
* Native Python integration
* Easy data visualization
* Suitable for a hackathon prototype
* Simple deployment

**Trade-off:**

Streamlit provides less control over complex frontend interactions compared with React.

---

## FastAPI Backend

**Decision:** Separate the frontend from backend logic.

**Why:**

* Clear separation of responsibilities
* REST API can support other clients later
* Easier testing and deployment
* Business logic remains independent of UI

**Trade-off:**

This introduces additional deployment and API communication complexity compared with a single Streamlit application.

---

## PostgreSQL

**Decision:** Use PostgreSQL instead of storing history only in memory.

**Why:**

* Persistent storage
* Relational structure fits users, watchlists and snapshots
* Reliable historical tracking
* Supports future scalability

**Trade-off:**

Requires database configuration and deployment.

---

## Yahoo Finance / yfinance

**Decision:** Use Yahoo Finance data through `yfinance`.

**Why:**

* Easy integration
* No expensive market-data infrastructure
* Good fit for a hackathon prototype

**Trade-off:**

It is not intended to replace exchange-grade real-time market feeds. Data availability and latency can vary.

---

## Rule-Based Attention Score

**Decision:** Use a transparent scoring system instead of an ML model.

**Why:**

* Explainable
* Deterministic
* Easy to debug
* No training dataset required
* Users can understand the reason behind the score

**Trade-off:**

The scoring thresholds are manually designed and may not capture every subtle market condition.

---

## Gemini for Explanation, Not Prediction

**Decision:** Use Gemini only to explain already-detected signals.

**Why:**

This reduces hallucination risk and keeps financial reasoning deterministic.

The model receives structured information such as:

```text
Price change
Volume ratio
News count
Attention level
```

It does not independently invent market events.

**Trade-off:**

The explanation depends on an external AI service and therefore can fail or be rate-limited.

---

# 🔐 Security Considerations

Sensitive credentials are stored through environment variables.

```text
.env
```

is excluded from Git using:

```text
.gitignore
```

API keys and database credentials are never hardcoded into application source code.

For production use, additional authentication, authorization, secret management and rate limiting would be required.

---

# 🛠️ Tech Stack

### Frontend

* Python
* Streamlit
* Plotly
* Custom CSS

### Backend

* FastAPI
* Uvicorn
* Python

### Database

* PostgreSQL
* SQLAlchemy
* Psycopg2

### Market Data

* Yahoo Finance
* yfinance

### AI

* Google Gemini API
* google-genai

### Communication

* REST APIs
* Requests

### Deployment

* Streamlit Community Cloud
* Render

### Version Control

* Git
* GitHub

---

# 💻 Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/SMIX-26/marketpulse.git
cd marketpulse
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

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

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
GOOGLE_API_KEY=your_gemini_api_key
```

Do not commit `.env` to GitHub.

---

## 5. Start FastAPI

From the project root:

```bash
uvicorn backend.main:app --reload
```

Backend will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Start Streamlit

Open another terminal:

```bash
streamlit run frontend/app.py
```

The Streamlit application will open in the browser.

---

# ☁️ Deployment

## Backend

The FastAPI backend is deployed using **Render**.

The deployment uses:

```text
Build Command:
pip install -r requirements.txt
```

```text
Start Command:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

The deployed backend connects to a PostgreSQL database hosted on Render.

---

## Frontend

The Streamlit frontend is deployed using **Streamlit Community Cloud**.

The main application file is:

```text
frontend/app.py
```

The frontend communicates with the deployed FastAPI backend through REST APIs.

---

# 📌 Limitations

MarketPulse is designed as a hackathon prototype and has several limitations.

1. Market data depends on Yahoo Finance availability.
2. It is not an exchange-grade real-time trading system.
3. Attention thresholds are rule-based.
4. News coverage depends on the external news source.
5. Gemini responses depend on API availability and quotas.
6. The current user system is simplified for the prototype.
7. Authentication and authorization are not fully implemented.
8. Free-tier hosting may introduce cold starts or resource limitations.
9. Snapshot-based comparison does not provide tick-level market history.

---

# 🔮 Future Improvements

Potential future enhancements include:

* Real-time WebSocket market updates
* Stronger user authentication
* Personalized attention thresholds
* Sector-based watchlists
* Advanced volatility detection
* Earnings-event detection
* Sentiment analysis of news
* Intraday historical charts
* Portfolio integration
* Push notifications
* Mobile application
* More sophisticated anomaly-detection models
* Production-grade market-data providers

---

# 🧪 Testing Strategy

The system can be tested at multiple layers.

### Backend

* API endpoint testing
* Invalid symbol testing
* Duplicate watchlist testing
* Empty watchlist testing
* Snapshot creation testing
* Change detection testing

### Database

* Watchlist persistence
* Snapshot persistence
* News deduplication
* Historical retrieval

### AI

* Gemini availability
* Fallback explanation
* No fabricated news/events
* Concise output validation

### Frontend

* Watchlist addition/removal
* Dashboard rendering
* History filtering
* Stock details
* Empty states
* Backend unavailable state

---

# 🏆 Why MarketPulse?

MarketPulse focuses on a common problem in financial applications:

> **Users don't just need more market data — they need to know what changed and why it matters.**

Instead of overwhelming users with numbers, MarketPulse combines:

```text
Market Data
     +
Historical Context
     +
News Activity
     +
Explainable Scoring
     +
AI Explanation
     ↓
Actionable Awareness
```

The architecture is intentionally simple, explainable, and extensible, making it suitable as a foundation for a larger financial-market monitoring platform.

---

# 👩‍💻 Author

**Samikshya Jena**

B.Tech — Computer Science & Engineering

GitHub: `https://github.com/SMIX-26`

---

## 📄 License

This project was developed as a hackathon submission and educational prototype.
