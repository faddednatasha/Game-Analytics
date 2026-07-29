# 🎾 Tennis Rankings & Competition Explorer

An end-to-end data analytics project built on the **SportRadar Tennis API** — extracting competition, venue, and doubles-ranking data, storing it in a relational SQLite database, analyzing it with SQL, and presenting it through an interactive **Streamlit** dashboard.

---

## 📌 Project Overview

This project pulls tennis data from three SportRadar endpoints, flattens the nested JSON into a normalized relational schema, runs analytical SQL queries against it, and visualizes the results — both as static charts and as a live, filterable web dashboard.

**Domain:** Sports / Data Analytics
**Skills demonstrated:** Python scripting, API data extraction, relational database design (SQL), data visualization, Streamlit application development

---

## 🗂️ Project Structure

```
tennis-game-analytics/
├── data/
│   ├── atp_competitions.json
│   ├── complexes.json
│   └── doubles_competitor_rankings.json
├── .streamlit/
│   └── config.toml            # Streamlit theme (colors, font)
├── schema.py                   # Creates the SQLite database + 6 tables
├── load_data.py                 # Parses JSON, loads data into the database
├── queries.sql                   # All 25 SQL analysis queries
├── graphs.py                      # Generates 14 exploratory charts (matplotlib)
├── app.py                          # Streamlit dashboard (multi-page)
├── tennis.db                        # Generated SQLite database (not committed — see below)
└── README.md
```

---

## 🏗️ Database Schema

One SQLite database, six related tables:

| Table | Description | Key Relationships |
|---|---|---|
| `categories` | Tour categories (ATP, WTA, ITF, etc.) | — |
| `competitions` | Tournaments/events | `category_id → categories`, self-referencing `parent_id` for sub-competitions |
| `complexes` | Sports complexes | — |
| `venues` | Individual venues/courts | `complex_id → complexes` |
| `competitors` | Player profiles | — |
| `competitor_rankings` | Doubles ranking snapshots | `competitor_id → competitors` |



---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/tennis-game-analytics.git
cd tennis-game-analytics
```

### 2. Install dependencies
```bash
pip install streamlit pandas matplotlib
```

### 3. Add your data
Place your SportRadar JSON exports inside a `data/` folder:
```
data/atp_competitions.json
data/complexes.json
data/doubles_competitor_rankings.json
```
### 4. Build the database
```bash
python schema.py       # creates tennis.db with all 6 tables
python load_data.py    # parses the JSON and populates the tables
```

### 5. (Optional) Generate the static charts
```bash
python graphs.py
```

### 6. Launch the dashboard
```bash
streamlit run app.py
```

---

## 📊 Dashboard Features

- **Home** — headline stats (total competitors, countries represented, highest points), country-wise analysis, and leaderboards (top-ranked / highest points)
- **Rankings** — search competitors by name, filter by country / rank range / minimum points threshold, and a detailed competitor profile viewer
- **Competitions** — browse all competitions, filter by type and category
- **Venues** — browse all venues, filter by country
- **Graphs** — all 14 exploratory charts (category breakdowns, top-10 leaderboards, rank movement, points distribution, and more)

---

## 🔍 SQL Analysis

All 25 required queries are documented in [`queries.sql`](./queries.sql), covering:
- **Competitions & Categories** (7 queries) — hierarchy, type distribution, category breakdowns
- **Complexes & Venues** (7 queries) — venue counts, country/timezone groupings
- **Competitors & Rankings** (6 queries) — leaderboards, rank stability, country totals
- **Bonus insights** (5 queries) — average points by country, rank movement summary, and more

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| Database | SQLite (via `sqlite3`) |
| Data source | [SportRadar Tennis API](https://developer.sportradar.com/tennis/reference) |
| Analysis | SQL, pandas |
| Visualization | matplotlib |
| Web App | Streamlit |

---
~ AAYUSHI TEWARI
