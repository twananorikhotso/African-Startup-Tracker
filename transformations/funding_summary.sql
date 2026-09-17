-- African Startup Tracker
-- Phase 3: Data Transformations
-- Overall funding summary

-- Total funding across all startups
SELECT
    SUM(funding_amount) AS total_funding
FROM startups;


-- Average funding per startup
SELECT
    AVG(funding_amount) AS average_funding
FROM startups;
