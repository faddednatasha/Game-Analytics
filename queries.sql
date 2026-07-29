-- =====================================================================
-- SECTION 1: Competitions & Categories (1-7)
-- =====================================================================

-- 1) List all competitions along with their category name
SELECT c.competition_id, c.competition_name, c.type, c.gender, cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id;

-- 2) Count the number of competitions in each category
SELECT cat.category_name, COUNT(*) AS competition_count
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name;

-- 3) Find all competitions of type 'doubles'
SELECT * FROM competitions WHERE type = 'doubles';

-- 4) Get competitions that belong to a specific category (e.g., ATP)
SELECT c.*
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ATP';

-- 5) Identify parent competitions and their sub-competitions
SELECT parent.competition_name AS parent_competition,
       child.competition_name  AS sub_competition
FROM competitions child
JOIN competitions parent ON child.parent_id = parent.competition_id;

-- 6) Analyze the distribution of competition types by category
SELECT cat.category_name, c.type, COUNT(*) AS total
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, c.type;

-- 7) List all competitions with no parent (top-level competitions)
SELECT * FROM competitions WHERE parent_id IS NULL;


-- =====================================================================
-- SECTION 2: Complexes & Venues (8-14)
-- =====================================================================

-- 8) List all venues along with their associated complex name
SELECT v.venue_name, v.city_name, v.country_name, cx.complex_name
FROM venues v
JOIN complexes cx ON v.complex_id = cx.complex_id;

-- 9) Count the number of venues in each complex
SELECT cx.complex_name, COUNT(*) AS venue_count
FROM venues v
JOIN complexes cx ON v.complex_id = cx.complex_id
GROUP BY cx.complex_name;

-- 10) Get details of venues in a specific country (e.g., Chile)
SELECT * FROM venues WHERE country_name = 'Chile';

-- 11) Identify all venues and their timezones
SELECT venue_name, timezone FROM venues;

-- 12) Find complexes that have more than one venue
SELECT cx.complex_name, COUNT(*) AS venue_count
FROM venues v
JOIN complexes cx ON v.complex_id = cx.complex_id
GROUP BY cx.complex_name
HAVING COUNT(*) > 1;

-- 13) List venues grouped by country
SELECT country_name, GROUP_CONCAT(venue_name, ', ') AS venues
FROM venues
GROUP BY country_name;

-- 14) Find all venues for a specific complex (e.g., Nacional)
SELECT v.*
FROM venues v
JOIN complexes cx ON v.complex_id = cx.complex_id
WHERE cx.complex_name = 'Nacional';


-- =====================================================================
-- SECTION 3: Competitors & Doubles Rankings (15-20)
-- =====================================================================

-- 15) Get all competitors with their rank and points
SELECT co.name, co.country, r.rank, r.points
FROM competitor_rankings r
JOIN competitors co ON r.competitor_id = co.competitor_id
ORDER BY r.rank;

-- 16) Find competitors ranked in the top 5
SELECT co.name, r.rank, r.points
FROM competitor_rankings r
JOIN competitors co ON r.competitor_id = co.competitor_id
WHERE r.rank <= 5
ORDER BY r.rank;

-- 17) List competitors with no rank movement (stable rank)
SELECT co.name, r.rank, r.movement
FROM competitor_rankings r
JOIN competitors co ON r.competitor_id = co.competitor_id
WHERE r.movement = 0;

-- 18) Get the total points of competitors from a specific country (e.g., Croatia)
SELECT co.country, SUM(r.points) AS total_points
FROM competitor_rankings r
JOIN competitors co ON r.competitor_id = co.competitor_id
WHERE co.country = 'Croatia'
GROUP BY co.country;

-- 19) Count the number of competitors per country
SELECT country, COUNT(*) AS competitor_count
FROM competitors
GROUP BY country
ORDER BY competitor_count DESC;

-- 20) Find competitors with the highest points in the current week
SELECT co.name, r.points
FROM competitor_rankings r
JOIN competitors co ON r.competitor_id = co.competitor_id
WHERE r.points = (SELECT MAX(points) FROM competitor_rankings);


-- =====================================================================
-- BONUS: Extra insight queries (21-25)
-- =====================================================================

-- 21) Average points per country (top 10)
SELECT co.country, ROUND(AVG(r.points), 1) AS avg_points, COUNT(*) AS num_competitors
FROM competitor_rankings r
JOIN competitors co ON r.competitor_id = co.competitor_id
GROUP BY co.country
ORDER BY avg_points DESC
LIMIT 10;

-- 22) Number of competitions per level (grand_slam, atp_250, atp_1000, etc.)
SELECT level, COUNT(*) AS competition_count
FROM competitions
WHERE level IS NOT NULL
GROUP BY level
ORDER BY competition_count DESC;

-- 23) Number of doubles competitions per category
SELECT cat.category_name, COUNT(*) AS doubles_count
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE c.type = 'doubles'
GROUP BY cat.category_name;

-- 24) Rank movement summary (how many competitors moved up / down / stayed)
SELECT
    CASE
        WHEN movement > 0 THEN 'Moved Up'
        WHEN movement < 0 THEN 'Moved Down'
        ELSE 'No Change'
    END AS movement_status,
    COUNT(*) AS competitor_count
FROM competitor_rankings
GROUP BY movement_status;

-- 25) Venue count per timezone
SELECT timezone, COUNT(*) AS venue_count
FROM venues
GROUP BY timezone
ORDER BY venue_count DESC;