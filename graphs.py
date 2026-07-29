import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("tennis.db")


def run_query(sql):
    return pd.read_sql_query(sql, conn)


def save_and_show(filename):
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


# =====================================================================
# CHART 1: Competitions per category (bar) -> query #2
# =====================================================================
df1 = run_query("""
    SELECT cat.category_name, COUNT(*) AS competition_count
    FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
    GROUP BY cat.category_name
""")
plt.figure(figsize=(6, 4))
plt.bar(df1["category_name"], df1["competition_count"], color="seagreen")
plt.title("Competitions per Category")
plt.xlabel("Category")
plt.ylabel("Number of Competitions")
save_and_show("chart1_competitions_per_category.png")


# =====================================================================
# CHART 2: Competition type distribution (grouped bar) -> query #6
# =====================================================================
df2 = run_query("""
    SELECT cat.category_name, c.type, COUNT(*) AS total
    FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
    GROUP BY cat.category_name, c.type
""")
pivot2 = df2.pivot(index="category_name", columns="type", values="total").fillna(0)
pivot2.plot(kind="bar", figsize=(8, 5))
plt.title("Competition Types by Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.legend(title="Type")
save_and_show("chart2_types_by_category.png")


# =====================================================================
# CHART 3: Top 10 countries by competitor count (horizontal bar) -> query #19
# =====================================================================
df3 = run_query("""
    SELECT country, COUNT(*) AS competitor_count
    FROM competitors GROUP BY country
    ORDER BY competitor_count DESC LIMIT 10
""")
plt.figure(figsize=(7, 5))
plt.barh(df3["country"], df3["competitor_count"], color="steelblue")
plt.title("Top 10 Countries by Competitor Count")
plt.xlabel("Number of Competitors")
plt.gca().invert_yaxis()
save_and_show("chart3_top_countries.png")


# =====================================================================
# CHART 4: Top 10 competitors by points (horizontal bar) -> query #15/16
# =====================================================================
df4 = run_query("""
    SELECT co.name, r.points
    FROM competitor_rankings r JOIN competitors co ON r.competitor_id = co.competitor_id
    ORDER BY r.points DESC LIMIT 10
""")
plt.figure(figsize=(7, 5))
plt.barh(df4["name"], df4["points"], color="darkorange")
plt.title("Top 10 Competitors by Points")
plt.xlabel("Points")
plt.gca().invert_yaxis()
save_and_show("chart4_top_points.png")


# =====================================================================
# CHART 5: Rank movement summary (pie) -> query #24
# =====================================================================
df5 = run_query("""
    SELECT
        CASE WHEN movement > 0 THEN 'Moved Up'
             WHEN movement < 0 THEN 'Moved Down'
             ELSE 'No Change' END AS movement_status,
        COUNT(*) AS competitor_count
    FROM competitor_rankings
    GROUP BY movement_status
""")
plt.figure(figsize=(5, 5))
plt.pie(df5["competitor_count"], labels=df5["movement_status"], autopct="%1.1f%%",
        colors=["mediumseagreen", "tomato", "lightgray"])
plt.title("Rank Movement Summary")
save_and_show("chart5_movement_summary.png")


# =====================================================================
# CHART 6: Competitions per level (bar) -> query #22
# =====================================================================
df6 = run_query("""
    SELECT level, COUNT(*) AS competition_count
    FROM competitions WHERE level IS NOT NULL
    GROUP BY level ORDER BY competition_count DESC
""")
plt.figure(figsize=(7, 4))
plt.bar(df6["level"], df6["competition_count"], color="mediumpurple")
plt.title("Competitions per Level")
plt.xlabel("Level")
plt.ylabel("Count")
plt.xticks(rotation=30, ha="right")
save_and_show("chart6_competitions_per_level.png")


# =====================================================================
# CHART 7: Venue count per complex, top 10 (bar) -> query #9
# =====================================================================
df7 = run_query("""
    SELECT cx.complex_name, COUNT(*) AS venue_count
    FROM venues v JOIN complexes cx ON v.complex_id = cx.complex_id
    GROUP BY cx.complex_name
    ORDER BY venue_count DESC LIMIT 10
""")
plt.figure(figsize=(8, 5))
plt.bar(df7["complex_name"], df7["venue_count"], color="teal")
plt.title("Top 10 Complexes by Venue Count")
plt.xlabel("Complex")
plt.ylabel("Number of Venues")
plt.xticks(rotation=40, ha="right")
save_and_show("chart7_venues_per_complex.png")


# =====================================================================
# CHART 8: Top 10 countries by venue count (horizontal bar) -> query #13
# =====================================================================
df8 = run_query("""
    SELECT country_name, COUNT(*) AS venue_count
    FROM venues GROUP BY country_name
    ORDER BY venue_count DESC LIMIT 10
""")
plt.figure(figsize=(7, 5))
plt.barh(df8["country_name"], df8["venue_count"], color="indianred")
plt.title("Top 10 Countries by Venue Count")
plt.xlabel("Number of Venues")
plt.gca().invert_yaxis()
save_and_show("chart8_venues_per_country.png")


# =====================================================================
# CHART 9: Top 10 timezones by venue count (bar) -> query #25
# =====================================================================
df9 = run_query("""
    SELECT timezone, COUNT(*) AS venue_count
    FROM venues GROUP BY timezone
    ORDER BY venue_count DESC LIMIT 10
""")
plt.figure(figsize=(8, 5))
plt.bar(df9["timezone"], df9["venue_count"], color="goldenrod")
plt.title("Top 10 Timezones by Venue Count")
plt.xlabel("Timezone")
plt.ylabel("Number of Venues")
plt.xticks(rotation=40, ha="right")
save_and_show("chart9_venues_per_timezone.png")


# =====================================================================
# CHART 10: Top 10 countries by average points (bar) -> query #21
# =====================================================================
df10 = run_query("""
    SELECT co.country, ROUND(AVG(r.points), 1) AS avg_points
    FROM competitor_rankings r JOIN competitors co ON r.competitor_id = co.competitor_id
    GROUP BY co.country
    ORDER BY avg_points DESC LIMIT 10
""")
plt.figure(figsize=(8, 5))
plt.bar(df10["country"], df10["avg_points"], color="crimson")
plt.title("Top 10 Countries by Average Points")
plt.xlabel("Country")
plt.ylabel("Average Points")
plt.xticks(rotation=40, ha="right")
save_and_show("chart10_avg_points_by_country.png")


# =====================================================================
# CHART 11: Doubles competitions per category (bar) -> query #23
# =====================================================================
df11 = run_query("""
    SELECT cat.category_name, COUNT(*) AS doubles_count
    FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
    WHERE c.type = 'doubles'
    GROUP BY cat.category_name
""")
plt.figure(figsize=(6, 4))
plt.bar(df11["category_name"], df11["doubles_count"], color="cornflowerblue")
plt.title("Doubles Competitions per Category")
plt.xlabel("Category")
plt.ylabel("Doubles Competition Count")
save_and_show("chart11_doubles_per_category.png")


# =====================================================================
# CHART 12: Top-level vs sub-competitions (pie) -> query #7
# =====================================================================
df12 = run_query("""
    SELECT
        CASE WHEN parent_id IS NULL THEN 'Top-Level' ELSE 'Sub-Competition' END AS level_type,
        COUNT(*) AS total
    FROM competitions
    GROUP BY level_type
""")
plt.figure(figsize=(5, 5))
plt.pie(df12["total"], labels=df12["level_type"], autopct="%1.1f%%",
        colors=["mediumturquoise", "salmon"])
plt.title("Top-Level vs Sub-Competitions")
save_and_show("chart12_toplevel_vs_sub.png")


# =====================================================================
# CHART 13: Points distribution across all competitors (histogram) -> query #15
# =====================================================================
df13 = run_query("SELECT points FROM competitor_rankings")
plt.figure(figsize=(7, 5))
plt.hist(df13["points"], bins=20, color="mediumslateblue", edgecolor="white")
plt.title("Distribution of Ranking Points (All Competitors)")
plt.xlabel("Points")
plt.ylabel("Number of Competitors")
save_and_show("chart13_points_distribution.png")


# =====================================================================
# CHART 14: Competitions per gender (pie) -> based on competitions.gender
# =====================================================================
df14 = run_query("""
    SELECT gender, COUNT(*) AS total
    FROM competitions
    GROUP BY gender
""")
plt.figure(figsize=(5, 5))
plt.pie(df14["total"], labels=df14["gender"], autopct="%1.1f%%",
        colors=["skyblue", "lightpink", "khaki"])
plt.title("Competitions by Gender")
save_and_show("chart14_gender_distribution.png")

conn.close()
print("✅ All 14 charts generated and saved as PNG files.")