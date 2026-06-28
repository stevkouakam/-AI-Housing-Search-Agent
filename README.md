# NestIQ — AI-Housing Search Agent

> Your personal real estate scout — an AI agent that crawls every Quebec rental platform, analyzes thousands of listings in seconds, and delivers only the ones worth your time.

---

## The Problem

Finding a rental in Montreal or Quebec City as a student or young professional is brutal:
- Listings disappear within hours
- Scams are everywhere
- Prices are opaque with no market reference
- You have to manually check Kijiji, Facebook Marketplace, and LogisFinder separately

NestIQ centralizes, analyzes, and filters listings for you — so you only see what actually matches your needs.

---

## What It Does

You type a natural language request like:

> *"Furnished shared apartment in Montreal, max $700/month, near a metro station"*

NestIQ runs a full pipeline:

1. **Understands** your request and extracts structured search criteria
2. **Scrapes** real listings from Quebec rental platforms in real time
3. **Scores** each listing against market prices and fraud signals using RAG
4. **Displays** results as visual cards ranked by relevance

---

## Architecture — 3 Agents + RAG Pipeline

```
User request (natural language)
        ↓
[Extractor Agent] → structured JSON criteria
        ↓
[Collector Agent] → raw listings (Kijiji, Marketplace, LogisFinder)
        ↓
[Analyst Agent] ← queries ChromaDB (neighborhood price data)
        ↓
Scored + ranked listings
        ↓
React Frontend (visual cards)
```

### Agent 0 — Extractor
Receives the user's free text, sends it to GPT-4o-mini, and returns a validated JSON object with structured criteria (city, type, budget, proximity, etc.).

### Agent 1 — Collector
Takes the JSON criteria and uses Playwright to scrape real listings from Kijiji (and later Marketplace, LogisFinder). Returns raw listing objects with title, price, address, description, link, date, and source.

### Agent 2 — Analyst
Receives each raw listing, queries ChromaDB for neighborhood price context (RAG), then asks GPT-4o to evaluate relevance, compare price to market median, detect scam signals, and assign a score from 0 to 100.

### Orchestrator — LangGraph
Connects the 3 agents into a state graph. Manages execution order, shared state between agents, error handling, and conditional branching. Exposes a single endpoint: `POST /api/search`.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Backend framework | FastAPI + Uvicorn |
| AI orchestration | LangGraph >= 0.2 |
| LLM | OpenAI GPT-4o / GPT-4o-mini |
| Web scraping | Playwright + BeautifulSoup4 |
| Vector database | ChromaDB (RAG on neighborhood prices) |
| Embeddings | sentence-transformers (multilingual FR/EN) |
| Data validation | Pydantic v2 |
| Database | PostgreSQL + SQLAlchemy |
| Cache | Redis (recent scraping results) |
| Frontend | React 18 + TypeScript |
| Styling | Tailwind CSS |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Railway |

---

## Project Structure

```
nestiq/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── extractor.py       ← Extractor Agent
│   │   │   ├── collector.py       ← Collector Agent
│   │   │   └── analyst.py         ← Analyst Agent
│   │   ├── models/
│   │   │   └── schemas.py         ← Pydantic schemas
│   │   ├── routes/
│   │   │   └── search.py          ← /api/search endpoint
│   │   ├── rag/
│   │   │   └── vector_store.py    ← ChromaDB + embeddings
│   │   ├── orchestrator/
│   │   │   └── graph.py           ← LangGraph pipeline
│   │   └── main.py                ← FastAPI entry point
│   ├── tests/
│   │   ├── test_stack.py          ← Stack validation (Sprint 0)
│   │   ├── test_extractor.py
│   │   ├── test_collector.py
│   │   └── test_analyst.py
│   ├── .env                       ← secrets (never committed)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.tsx
│   │   │   ├── ResultsGrid.tsx
│   │   │   └── ListingCard.tsx
│   │   ├── types/
│   │   │   └── listing.ts
│   │   ├── api/
│   │   │   └── search.ts
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Data Models

### SearchCriteria
Structured output of the Extractor Agent.

```json
{
  "ville": "Montréal",
  "type_logement": "colocation",
  "meuble": true,
  "budget_max": 700,
  "proximite": ["métro"],
  "quartiers_preferes": [],
  "disponibilite": null,
  "criteres_speciaux": []
}
```

### ScoredListing
Output of the Analyst Agent for each listing.

```json
{
  "listing": { "titre": "...", "prix": 650, "adresse": "...", "lien": "..." },
  "score_pertinence": 87,
  "prix_vs_marche": "12% below neighborhood median",
  "signaux_arnaque": [],
  "verdict": "recommended",
  "explication": "Price is competitive, furnished, 5 min walk from Laurier metro."
}
```

---

## Getting Started

### Prerequisites
- Python 3.12
- Node.js 18+
- Docker + Docker Compose (for full stack)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/stevkouakam/-AI-Housing-Search-Agent.git
cd -AI-Housing-Search-Agent/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables

```bash
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/nestiq
REDIS_URL=redis://localhost:6379
CHROMA_PERSIST_DIR=./chroma_db
PLAYWRIGHT_HEADLESS=true
```

### Validate the Stack

```bash
python tests/test_stack.py
# Expected output:
#  OpenAI API : OK
#  ChromaDB : OK
#  Tous les tests passés — Sprint 0 complété !
```

### Run the Backend

```bash
uvicorn app.main:app --reload
# API available at http://localhost:8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:5173
```

---

## API

### `POST /api/search`

Single endpoint for the full pipeline.

**Request:**
```json
{
  "query": "Furnished shared apartment in Montreal, max $700/month, near metro"
}
```

**Response:**
```json
{
  "criteres": { ... },
  "resultats": [ { "listing": {...}, "score_pertinence": 87, ... } ],
  "total_trouve": 24,
  "total_retenu": 8,
  "duree_recherche_sec": 4.2
}
```

---

## Development Roadmap

| Sprint | Focus | Status |
|---|---|---|
| Sprint 0 | Setup — stack validation | ✅ Done |
| Sprint 1 | Extractor Agent + `/api/extract` | 🔄 In progress |
| Sprint 2 | Collector Agent — Kijiji scraping | ⏳ Upcoming |
| Sprint 3 | RAG + Analyst Agent | ⏳ Upcoming |
| Sprint 4 | LangGraph integration + React UI | ⏳ Upcoming |
| Sprint 5 | Docker + Railway deployment | ⏳ Upcoming |

---

## Target Users

Students and young professionals in Quebec — especially newcomers who don't know the local rental market and need help finding housing fast before listings disappear.

---

## Author

**Steeve junix** — Computer Science student at Université Laval, specializing in software development and agentic AI.

- GitHub: [@stevkouakam](https://github.com/stevkouakam)
