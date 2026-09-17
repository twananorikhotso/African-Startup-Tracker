-- African Startup Tracker
-- Phase 3: Data Transformations
-- Country-level analytics

-- Total funding by country
SELECT
    origin_country,
    SUM(funding_amount) AS total_funding
FROM startups
GROUP BY origin_country
ORDER BY total_funding DESC;


-- Startup count by country
SELECT
    origin_country,
    COUNT(*) AS startup_count
FROM startups
GROUP BY origin_country
ORDER BY startup_count DESC, origin_country;