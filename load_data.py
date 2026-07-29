import sqlite3
import json
import os

# Helper to find JSON file whether it's in root or 'data/' folder
def get_file_path(filename):
    if os.path.exists(filename):
        return filename
    elif os.path.exists(os.path.join("data", filename)):
        return os.path.join("data", filename)
    else:
        raise FileNotFoundError(f"Could not find {filename} in current folder or 'data/' folder.")

conn = sqlite3.connect("tennis.db")
cur = conn.cursor()

# ---------------------------------------------------------------------
# 1) COMPETITIONS + CATEGORIES
# ---------------------------------------------------------------------
with open(get_file_path("atp_competitions.json")) as f:
    comp_data = json.load(f)

categories_seen = {}
for c in comp_data.get("competitions", []):
    cat = c.get("category", {})
    cat_id = cat.get("id")
    if cat_id and cat_id not in categories_seen:
        categories_seen[cat_id] = cat.get("name")

for cat_id, cat_name in categories_seen.items():
    cur.execute("""
        INSERT OR REPLACE INTO categories (category_id, category_name)
        VALUES (?, ?)
    """, (cat_id, cat_name))

for c in comp_data.get("competitions", []):
    cat_id = c.get("category", {}).get("id")
    cur.execute("""
        INSERT OR REPLACE INTO competitions
        (competition_id, competition_name, parent_id, type, gender, level, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        c["id"], c["name"], c.get("parent_id"),
        c["type"], c["gender"], c.get("level"), cat_id
    ))

print(f"Loaded {len(categories_seen)} categories, {len(comp_data.get('competitions', []))} competitions")

# ---------------------------------------------------------------------
# 2) COMPLEXES + VENUES
# ---------------------------------------------------------------------
with open(get_file_path("complexes.json")) as f:
    complex_data = json.load(f)

venue_count = 0
for cx in complex_data.get("complexes", []):
    cur.execute("""
        INSERT OR REPLACE INTO complexes (complex_id, complex_name)
        VALUES (?, ?)
    """, (cx["id"], cx["name"]))

    for v in cx.get("venues", []):
        cur.execute("""
            INSERT OR REPLACE INTO venues
            (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            v["id"], v["name"], v.get("city_name", ""),
            v.get("country_name", ""), v.get("country_code", ""), v.get("timezone", ""), cx["id"]
        ))
        venue_count += 1

print(f"Loaded {len(complex_data.get('complexes', []))} complexes, {venue_count} venues")

# ---------------------------------------------------------------------
# 3) COMPETITORS + RANKINGS
# ---------------------------------------------------------------------
with open(get_file_path("doubles_competitor_rankings.json")) as f:
    rank_data = json.load(f)

competitors_seen = set()
ranking_count = 0

for block in rank_data.get("rankings", []):
    for entry in block.get("competitor_rankings", []):
        comp = entry["competitor"]

        if comp["id"] not in competitors_seen:
            cur.execute("""
                INSERT OR REPLACE INTO competitors
                (competitor_id, name, country, country_code, abbreviation)
                VALUES (?, ?, ?, ?, ?)
            """, (
                comp["id"], comp["name"], comp.get("country", ""),
                comp.get("country_code", ""), comp.get("abbreviation", "")
            ))
            competitors_seen.add(comp["id"])

        cur.execute("""
            INSERT INTO competitor_rankings
            (rank, movement, points, competitor_id)
            VALUES (?, ?, ?, ?)
        """, (
            entry.get("rank"), entry.get("movement"), entry.get("points"), comp["id"]
        ))
        ranking_count += 1

print(f"Loaded {len(competitors_seen)} competitors, {ranking_count} ranking records")

conn.commit()
conn.close()
print("✅ All data loaded into tennis.db")