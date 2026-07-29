import sqlite3

conn = sqlite3.connect("tennis.db")
cur = conn.cursor()

tables = ["categories", "competitions", "complexes", "venues", "competitors", "competitor_rankings"]

print("--- TABLE ROW COUNTS ---")
for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"{table.capitalize()}: {count} rows")

conn.close()