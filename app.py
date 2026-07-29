import os
import sqlite3
import subprocess
import sys
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# MUST BE THE VERY FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Tennis Rankings Explorer", page_icon="🎾", layout="wide"
)


# Check if the database exists AND contains actual data
def init_database():
    db_needs_init = False

    if not os.path.exists("tennis.db"):
        db_needs_init = True
    else:
        # Check if tables exist inside the database file
        try:
            conn = sqlite3.connect("tennis.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='competitors';"
            )
            if not cursor.fetchone():
                db_needs_init = True
            conn.close()
        except Exception:
            db_needs_init = True

    if db_needs_init:
        st.info("⚡ Initializing database on Streamlit Cloud... Please wait.")
        # Remove empty or corrupted db file if present
        if os.path.exists("tennis.db"):
            os.remove("tennis.db")

        # Run schema and data loader using sys.executable
        subprocess.run([sys.executable, "schema.py"], check=True)
        subprocess.run([sys.executable, "load_data.py"], check=True)
        st.rerun()


init_database()

conn = sqlite3.connect("tennis.db", check_same_thread=False)

# ---------------------------------------------------------------------
# Color Scheme of Dashboard
# ---------------------------------------------------------------------
DEEP_GREEN = "#008C2B"
GREEN = "#01AA35"
LIME = "#C8DC00"
WHITE = "#FFFFFF"
CREAM = "#EFEBD8"
INK = "#123319"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600..900&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {INK}; }}

.hero-title {{
    font-family: 'Fraunces', serif; font-weight: 900; font-size: 2.6rem;
    color: {INK}; margin-bottom: 0.1rem; line-height: 1.1;
}}
.hero-subtitle {{
    font-family: 'Inter', sans-serif; font-size: 1rem; color: #3F5A45;
    margin-bottom: 1.4rem; max-width: 720px;
}}
.section-title {{
    font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.6rem;
    color: {INK}; margin-bottom: 0.1rem;
}}
.section-subtitle {{
    font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #5B7360;
    margin-bottom: 0.8rem;
}}
.card-title {{
    font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.1rem;
    color: {INK}; margin-bottom: 0.1rem;
}}
.eyebrow {{
    font-family: 'Space Grotesk', monospace; font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase; color: {GREEN};
}}
.scoreboard {{
    background: {DEEP_GREEN}; border-radius: 14px; padding: 1.6rem 2rem;
    margin-bottom: 1.4rem; display: flex; justify-content: space-between;
    border-top: 3px solid {LIME}; border-bottom: 3px solid {LIME};
}}
.scoreboard .stat {{ text-align: center; }}
.scoreboard .stat .num {{
    font-family: 'Space Grotesk', monospace; font-size: 2.3rem;
    font-weight: 700; color: {LIME}; line-height: 1;
}}
.scoreboard .stat .label {{ font-size: 0.75rem; color: {CREAM}; margin-top: 0.3rem; }}

.detail-card {{
    background: {WHITE}; border: 1px solid #D9D2B8; border-radius: 10px;
    padding: 0.9rem; text-align: center;
}}
.detail-card .val {{
    font-family: 'Space Grotesk', monospace; font-size: 1.6rem;
    font-weight: 700; color: {DEEP_GREEN};
}}
.detail-card .lbl {{ font-size: 0.75rem; color: #5B7360; }}

section[data-testid="stSidebar"] {{ background: {DEEP_GREEN}; }}
section[data-testid="stSidebar"] * {{ color: {CREAM} !important; }}
section[data-testid="stSidebar"] .stRadio label {{
    font-family: 'Space Grotesk', monospace; font-size: 0.95rem;
}}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)
def run_query(sql):
    return pd.read_sql_query(sql, sqlite3.connect("tennis.db"))


def eyebrow(text):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)


def section_header(title, subtitle):
    st.markdown(
        f'<div class="section-title">{title}</div>', unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True
    )


def download_button(df, label, filename):
    st.download_button(
        label, df.to_csv(index=False), file_name=filename, mime="text/csv"
    )


# =====================================================================
# SIDEBAR NAV
# =====================================================================
with st.sidebar:
    st.markdown("## 🎾 Tennis Explorer")
    st.caption("Data source: SportRadar Tennis API")
    st.divider()
    page = st.radio(
        "Navigate",
        ["Home", "Rankings", "Competitions", "Venues", "Graphs"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("~ Aayushi Tewari")

# =====================================================================
# HOME
# =====================================================================
if page == "Home":
    st.markdown(
        '<div class="hero-title">Tennis Rankings and Game Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle">Interactive insights on player rankings, competition structures, and venue data powered by Sportradar API.',
        unsafe_allow_html=True,
    )

    total_competitors = run_query("SELECT COUNT(*) AS n FROM competitors")["n"][
        0
    ]
    total_countries = run_query(
        "SELECT COUNT(DISTINCT country) AS n FROM competitors"
    )["n"][0]
    max_points = int(
        run_query("SELECT MAX(points) AS n FROM competitor_rankings")["n"][0]
    )

    st.markdown(
        f"""
    <div class="scoreboard">
        <div class="stat"><div class="num">{total_competitors}</div><div class="label">TOTAL COMPETITORS</div></div>
        <div class="stat"><div class="num">{total_countries}</div><div class="label">COUNTRIES REPRESENTED</div></div>
        <div class="stat"><div class="num">{max_points:,}</div><div class="label">HIGHEST POINTS</div></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # --- Country-Wise Analysis -----------------------------------------
    with st.container(border=True):
        eyebrow("BY COUNTRY")
        section_header(
            "Country-Wise Analysis",
            "Total competitors and their average ranking points, by country.",
        )
        country_df = run_query("""
            SELECT co.country, COUNT(DISTINCT co.competitor_id) AS competitor_count,
                   ROUND(AVG(r.points), 1) AS avg_points
            FROM competitors co JOIN competitor_rankings r ON co.competitor_id = r.competitor_id
            GROUP BY co.country ORDER BY competitor_count DESC
        """)
        search_country = st.text_input("Search country", key="country_search")
        if search_country:
            country_df = country_df[
                country_df["country"].str.contains(
                    search_country, case=False, na=False
                )
            ]
        st.dataframe(country_df, width="stretch", hide_index=True, height=280)
        download_button(country_df, "Download as CSV", "country_analysis.csv")

    # --- Leaderboards ----------------------------------------------------
    with st.container(border=True):
        eyebrow("LEADERBOARDS")
        section_header(
            "Top Performers",
            "The best-ranked competitors, and the highest point totals on tour.",
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                '<div class="card-title">Top-Ranked Competitors</div>',
                unsafe_allow_html=True,
            )
            top_ranked = run_query("""
                SELECT co.name, co.country, r.rank, r.points
                FROM competitor_rankings r JOIN competitors co ON r.competitor_id = co.competitor_id
                ORDER BY r.rank ASC LIMIT 10
            """)
            st.dataframe(top_ranked, width="stretch", hide_index=True)
        with col_b:
            st.markdown(
                '<div class="card-title">Highest Points</div>',
                unsafe_allow_html=True,
            )
            top_points = run_query("""
                SELECT co.name, co.country, r.rank, r.points
                FROM competitor_rankings r JOIN competitors co ON r.competitor_id = co.competitor_id
                ORDER BY r.points DESC LIMIT 10
            """)
            st.dataframe(top_points, width="stretch", hide_index=True)

# =====================================================================
# RANKINGS
# =====================================================================
elif page == "Rankings":
    st.markdown(
        '<div class="hero-title">Rankings</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-subtitle">Search, filter, and drill into individual competitor profiles.</div>',
        unsafe_allow_html=True,
    )

    all_competitors = run_query("""
        SELECT co.name, co.country, r.rank, r.points, r.movement, r.competitions_played
        FROM competitor_rankings r JOIN competitors co ON r.competitor_id = co.competitor_id
        ORDER BY r.rank
    """)

    max_rank_val = int(all_competitors["rank"].max())
    max_points_val = int(all_competitors["points"].max())

    if "rankings_search" not in st.session_state:
        st.session_state.rankings_search = ""
    if "rankings_country" not in st.session_state:
        st.session_state.rankings_country = "All"
    if "rankings_range" not in st.session_state:
        st.session_state.rankings_range = (1, max_rank_val)
    if "rankings_min_points" not in st.session_state:
        st.session_state.rankings_min_points = 0

    def reset_rankings_filters():
        st.session_state.rankings_search = ""
        st.session_state.rankings_country = "All"
        st.session_state.rankings_range = (1, max_rank_val)
        st.session_state.rankings_min_points = 0

    with st.container(border=True):
        hdr_col1, hdr_col2 = st.columns([4, 1])
        with hdr_col1:
            eyebrow("SEARCH & FILTER")
            section_header(
                "Competitors",
                "Filter by name, country, rank, or a minimum points threshold.",
            )
        with hdr_col2:
            st.write("")
            st.button(
                "🔄 Reset Filters",
                on_click=reset_rankings_filters,
                use_container_width=True,
            )

        c1, c2 = st.columns(2)
        search_name = c1.text_input("Search by name", key="rankings_search")
        countries = ["All"] + sorted(
            all_competitors["country"].dropna().unique().tolist()
        )
        country_filter = c2.selectbox(
            "Country", countries, key="rankings_country"
        )

        c3, c4 = st.columns(2)
        rank_range = c3.slider(
            "Rank range", 1, max_rank_val, key="rankings_range"
        )
        min_points = c4.number_input(
            "Minimum points threshold",
            min_value=0,
            max_value=max_points_val,
            step=100,
            key="rankings_min_points",
        )

        filtered = all_competitors.copy()
        if search_name:
            filtered = filtered[
                filtered["name"].str.contains(
                    search_name, case=False, na=False
                )
            ]
        if country_filter != "All":
            filtered = filtered[filtered["country"] == country_filter]
        filtered = filtered[
            (filtered["rank"] >= rank_range[0])
            & (filtered["rank"] <= rank_range[1])
        ]
        filtered = filtered[filtered["points"] >= min_points]

        st.dataframe(filtered, width="stretch", hide_index=True, height=320)
        download_button(
            filtered, "Download filtered results", "filtered_competitors.csv"
        )

    with st.container(border=True):
        eyebrow("PROFILE")
        section_header(
            "Competitor Details Viewer",
            "Select a competitor to see their full profile.",
        )
        selected = st.selectbox(
            "Select a competitor", all_competitors["name"].unique()
        )
        d = all_competitors[all_competitors["name"] == selected].iloc[0]

        cc1, cc2, cc3, cc4 = st.columns(4)
        for col, label, val in zip(
            [cc1, cc2, cc3, cc4],
            ["RANK", "MOVEMENT", "COMPETITIONS PLAYED", "COUNTRY"],
            [d["rank"], d["movement"], d["competitions_played"], d["country"]],
        ):
            col.markdown(
                f'<div class="detail-card"><div class="val">{val}</div>'
                f'<div class="lbl">{label}</div></div>',
                unsafe_allow_html=True,
            )

# =====================================================================
# COMPETITIONS
# =====================================================================
elif page == "Competitions":
    st.markdown(
        '<div class="hero-title">Competitions</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-subtitle">Browse every tracked competition across all tours and categories.</div>',
        unsafe_allow_html=True,
    )

    comps = run_query("""
        SELECT c.competition_name, c.type, c.gender, c.level, cat.category_name
        FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
    """)

    with st.container(border=True):
        eyebrow("SEARCH & FILTER")
        section_header(
            "All Competitions",
            "Search by name, or narrow down by type and category.",
        )

        c1, c2, c3 = st.columns(3)
        search_comp = c1.text_input("Search competition name")
        type_filter = c2.multiselect(
            "Type", options=sorted(comps["type"].unique())
        )
        category_filter = c3.multiselect(
            "Category", options=sorted(comps["category_name"].unique())
        )

        display_comps = comps.copy()
        if search_comp:
            display_comps = display_comps[
                display_comps["competition_name"].str.contains(
                    search_comp, case=False, na=False
                )
            ]
        if type_filter:
            display_comps = display_comps[
                display_comps["type"].isin(type_filter)
            ]
        if category_filter:
            display_comps = display_comps[
                display_comps["category_name"].isin(category_filter)
            ]

        st.dataframe(
            display_comps, width="stretch", hide_index=True, height=320
        )
        download_button(
            display_comps,
            "Download filtered results",
            "filtered_competitions.csv",
        )

# =====================================================================
# VENUES
# =====================================================================
elif page == "Venues":
    st.markdown(
        '<div class="hero-title">Venues & Complexes</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle">Every tournament venue, grouped by complex and country.</div>',
        unsafe_allow_html=True,
    )

    venues = run_query("""
        SELECT v.venue_name, v.city_name, v.country_name, cx.complex_name
        FROM venues v JOIN complexes cx ON v.complex_id = cx.complex_id
    """)

    with st.container(border=True):
        eyebrow("SEARCH & FILTER")
        section_header(
            "All Venues", "Search by venue name, or filter by country."
        )

        c1, c2 = st.columns(2)
        search_venue = c1.text_input("Search venue name")
        countries = ["All"] + sorted(
            venues["country_name"].dropna().unique().tolist()
        )
        country_filter = c2.selectbox("Country", countries)

        display_venues = venues.copy()
        if search_venue:
            display_venues = display_venues[
                display_venues["venue_name"].str.contains(
                    search_venue, case=False, na=False
                )
            ]
        if country_filter != "All":
            display_venues = display_venues[
                display_venues["country_name"] == country_filter
            ]

        st.dataframe(
            display_venues, width="stretch", hide_index=True, height=320
        )
        download_button(
            display_venues, "Download filtered results", "filtered_venues.csv"
        )

# =====================================================================
# GRAPHS
# =====================================================================
elif page == "Graphs":
    st.markdown(
        '<div class="hero-title">Insight Graphs</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-subtitle">All exploratory charts from the analysis notebook.</div>',
        unsafe_allow_html=True,
    )

    charts = [
        (
            "Competitions per Category",
            """
            SELECT cat.category_name, COUNT(*) AS competition_count
            FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
            GROUP BY cat.category_name
        """,
            "bar",
            "category_name",
            "competition_count",
            "seagreen",
        ),
        (
            "Top 10 Countries by Competitor Count",
            """
            SELECT country, COUNT(*) AS competitor_count FROM competitors
            GROUP BY country ORDER BY competitor_count DESC LIMIT 10
        """,
            "barh",
            "country",
            "competitor_count",
            "steelblue",
        ),
        (
            "Top 10 Competitors by Points",
            """
            SELECT co.name, r.points FROM competitor_rankings r
            JOIN competitors co ON r.competitor_id = co.competitor_id
            ORDER BY r.points DESC LIMIT 10
        """,
            "barh",
            "name",
            "points",
            "darkorange",
        ),
        (
            "Competitions per Level",
            """
            SELECT level, COUNT(*) AS competition_count FROM competitions
            WHERE level IS NOT NULL GROUP BY level ORDER BY competition_count DESC
        """,
            "bar",
            "level",
            "competition_count",
            "mediumpurple",
        ),
        (
            "Top 10 Complexes by Venue Count",
            """
            SELECT cx.complex_name, COUNT(*) AS venue_count
            FROM venues v JOIN complexes cx ON v.complex_id = cx.complex_id
            GROUP BY cx.complex_name ORDER BY venue_count DESC LIMIT 10
        """,
            "bar",
            "complex_name",
            "venue_count",
            "teal",
        ),
        (
            "Top 10 Countries by Venue Count",
            """
            SELECT country_name, COUNT(*) AS venue_count FROM venues
            GROUP BY country_name ORDER BY venue_count DESC LIMIT 10
        """,
            "barh",
            "country_name",
            "venue_count",
            "indianred",
        ),
        (
            "Top 10 Timezones by Venue Count",
            """
            SELECT timezone, COUNT(*) AS venue_count FROM venues
            GROUP BY timezone ORDER BY venue_count DESC LIMIT 10
        """,
            "bar",
            "timezone",
            "venue_count",
            "goldenrod",
        ),
        (
            "Top 10 Countries by Average Points",
            """
            SELECT co.country, ROUND(AVG(r.points), 1) AS avg_points
            FROM competitor_rankings r JOIN competitors co ON r.competitor_id = co.competitor_id
            GROUP BY co.country ORDER BY avg_points DESC LIMIT 10
        """,
            "bar",
            "country",
            "avg_points",
            "crimson",
        ),
        (
            "Doubles Competitions per Category",
            """
            SELECT cat.category_name, COUNT(*) AS doubles_count
            FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
            WHERE c.type = 'doubles' GROUP BY cat.category_name
        """,
            "bar",
            "category_name",
            "doubles_count",
            "cornflowerblue",
        ),
    ]

    cols = st.columns(2)
    for i, (title, sql, kind, x, y, color) in enumerate(charts):
        df = run_query(sql)
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(
                    f'<div class="card-title">{title}</div>',
                    unsafe_allow_html=True,
                )
                fig, ax = plt.subplots(figsize=(6, 4))
                if kind == "bar":
                    ax.bar(df[x], df[y], color=color)
                    plt.xticks(rotation=35, ha="right")
                else:
                    ax.barh(df[x], df[y], color=color)
                    ax.invert_yaxis()
                st.pyplot(fig)
                plt.close(fig)

    pie_col1, pie_col2 = st.columns(2)

    with pie_col1:
        with st.container(border=True):
            st.markdown(
                '<div class="card-title">Rank Movement Summary</div>',
                unsafe_allow_html=True,
            )
            df = run_query("""
                SELECT CASE WHEN movement > 0 THEN 'Moved Up'
                            WHEN movement < 0 THEN 'Moved Down'
                            ELSE 'No Change' END AS movement_status, COUNT(*) AS competitor_count
                FROM competitor_rankings GROUP BY movement_status
            """)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                df["competitor_count"],
                labels=df["movement_status"],
                autopct="%1.1f%%",
                colors=["mediumseagreen", "tomato", "lightgray"],
            )
            st.pyplot(fig)
            plt.close(fig)

    with pie_col2:
        with st.container(border=True):
            st.markdown(
                '<div class="card-title">Top-Level vs Sub-Competitions</div>',
                unsafe_allow_html=True,
            )
            df = run_query("""
                SELECT CASE WHEN parent_id IS NULL THEN 'Top-Level' ELSE 'Sub-Competition' END AS level_type,
                       COUNT(*) AS total FROM competitions GROUP BY level_type
            """)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                df["total"],
                labels=df["level_type"],
                autopct="%1.1f%%",
                colors=["mediumturquoise", "salmon"],
            )
            st.pyplot(fig)
            plt.close(fig)

    pie_col3, pie_col4 = st.columns(2)

    with pie_col3:
        with st.container(border=True):
            st.markdown(
                '<div class="card-title">Competitions by Gender</div>',
                unsafe_allow_html=True,
            )
            df = run_query(
                "SELECT gender, COUNT(*) AS total FROM competitions GROUP BY gender"
            )
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                df["total"],
                labels=df["gender"],
                autopct="%1.1f%%",
                colors=["skyblue", "lightpink", "khaki"],
            )
            st.pyplot(fig)
            plt.close(fig)

    with pie_col4:
        with st.container(border=True):
            st.markdown(
                '<div class="card-title">Distribution of Ranking Points</div>',
                unsafe_allow_html=True,
            )
            df = run_query("SELECT points FROM competitor_rankings")
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.hist(
                df["points"],
                bins=20,
                color="mediumslateblue",
                edgecolor="white",
            )
            st.pyplot(fig)
            plt.close(fig)

    with st.container(border=True):
        st.markdown(
            '<div class="card-title">Competition Types by Category</div>',
            unsafe_allow_html=True,
        )
        df = run_query("""
            SELECT cat.category_name, c.type, COUNT(*) AS total
            FROM competitions c JOIN categories cat ON c.category_id = cat.category_id
            GROUP BY cat.category_name, c.type
        """)
        pivot = (
            df.pivot(index="category_name", columns="type", values="total")
            .fillna(0)
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        pivot.plot(kind="bar", ax=ax)
        st.pyplot(fig)
        plt.close(fig)
