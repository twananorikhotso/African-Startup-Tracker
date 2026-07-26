# African Startup Ecosystem Tracker

A full-stack data pipeline that scrapes, stores, and visualizes funding and activity data for startups across Africa — built to make sense of an ecosystem that's growing fast but is scattered across dozens of blogs, press releases, and databases with no single source of truth.

## Why this project

I'm a Software Engineering student at WeThinkCode, and this project doubles as my portfolio piece for the Data Engineering elective. I wanted to build something that goes beyond a toy CRUD app — a real scrape → clean → store → API → dashboard pipeline, the kind of thing a data engineering team would actually run and maintain.

## What it does

- **Scrapes** startup and funding data from public sources (news sites, press releases, ecosystem trackers)
- **Cleans** and normalizes the data (deduplication, standardizing country/sector/funding-stage fields)
- **Stores** it in PostgreSQL with a schema designed for querying by country, sector, funding stage, and time period
- **Serves** it through a REST API built with Java Spring Boot
- **Visualizes** it on a JavaScript dashboard — funding trends by country, sector breakdowns, growth over time

## Tech stack

| Layer         | Tech                          |
|---------------|-------------------------------|
| Scraping      | Python                        |
| Database      | PostgreSQL                    |
| API           | Java, Spring Boot             |
| Dashboard     | JavaScript                    |

## Architecture

```
[ Python scrapers ] --> [ Clean/normalize ] --> [ PostgreSQL ]
                                                       |
                                                       v
                                          [ Spring Boot REST API ]
                                                       |
                                                       v
                                          [ JS Dashboard (frontend) ]
```

## Getting started

> Setup steps below are placeholders — update with your actual commands once the project structure is finalized.

### Prerequisites
- Python 3.x
- Java 17+ and Maven
- PostgreSQL
- Node.js (for the dashboard)

### Scraper
```bash
cd scraper
pip install -r requirements.txt
python scrape.py
```

### API
```bash
cd api
mvn spring-boot:run
```

### Dashboard
```bash
cd dashboard
npm install
npm start
```

## Project status

🚧 In active development. Current focus: [scraping / API / dashboard — update to reflect where you're at]

## Roadmap

- [ ] Expand scraper coverage to more sources/countries
- [ ] Add historical trend analysis
- [ ] Deploy dashboard publicly
- [ ] Add automated scraping schedule (cron/Airflow)

## Author

Built by Twanano Rikhotso — Software Engineering student at WeThinkCode.
