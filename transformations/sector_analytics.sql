-- African Startup Tracker
-- Phase 3: Data Transformations
-- Sector-level analytics

-- Total funding by sector
SELECT
    target_sector,
    SUM(funding_amount) AS total_funding
FROM startups
GROUP BY target_sector
ORDER BY total_funding DESC;


-- Startup count by sector
SELECT
    target_sector,
    COUNT(*) AS startup_count
FROM startups
GROUP BY target_sector
ORDER BY startup_count DESC, target_sector;