# African Startup Ecosystem Tracker

A full-stack data engineering project that extracts real African startup funding data, transforms and validates it, stores it in PostgreSQL, exposes it through a Spring Boot REST API, and visualizes it in a web dashboard.

The project was built as a portfolio project for the WeThinkCode Data Engineering elective, with a focus on building a complete and maintainable ETL pipeline rather than relying on hard-coded startup data.

## Project Overview

The African Startup Ecosystem Tracker follows an end-to-end data pipeline:

1. Extract startup data from a real external source
2. Clean, normalize, and validate the extracted data
3. Prevent duplicate startup records
4. Load validated records into PostgreSQL
5. Expose startup data through a Spring Boot REST API
6. Display startup and funding analytics in a JavaScript dashboard
7. Support scheduled ingestion and automated testing

## Data Source

The production ingestion pipeline currently uses public startup funding information from AU-Startups.

Funding page:

`https://au-startups.com/funding`

The pipeline discovers startup profile pages from the funding page and extracts information including:

- Company name
- Country
- Sector
- Total funding raised
- Source URL

Each stored startup record keeps its source URL so that the origin of the data can be traced.

## Architecture

```text
AU-Startups
    |
    v
Python Extraction
    |
    v
Cleaning / Transformation / Validation
    |
    v
PostgreSQL
    |
    v
Spring Boot REST API
    |
    v
JavaScript Dashboard
```

## Tech Stack

| Layer | Technology |
|---|---|
| Data extraction | Python, Requests, BeautifulSoup |
| Transformation | Python |
| Database | PostgreSQL |
| Backend API | Java, Spring Boot |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Testing | pytest, JUnit, Spring Boot Test |
| Containers | Docker, Docker Compose |
| CI configuration | GitHub Actions |

## Project Structure

```text
African-Startup-Tracker/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── ingestion/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── model.py
│   ├── pipeline.py
│   ├── scheduler.py
│   └── tests/
├── transformations/
│   ├── country_analytics.sql
│   ├── sector_analytics.sql
│   └── funding_summary.sql
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## ETL Pipeline

### Extract

The extraction layer downloads the AU-Startups funding page and discovers startup profile URLs.

Each selected startup profile is then fetched for transformation.

### Transform

The transformation layer:

- Normalizes company names
- Converts country codes to country names
- Normalizes sector names
- Converts funding values such as `$500K`, `$5M`, and `$1.5B` into integer values
- Handles additional funding formats such as `5 million`
- Rejects incomplete or invalid startup records

### Load

Validated startup records are loaded into PostgreSQL.

The database includes validation and duplicate protection. Startup names are compared using normalized values so that rerunning the pipeline does not create duplicate records for the same company.

## Database

The main PostgreSQL table is `startups`.

Important fields include:

- `id`
- `company_name`
- `origin_country`
- `target_sector`
- `funding_amount`
- `source_url`
- `fetched_at`

The database enforces required fields, non-negative funding values, and duplicate protection.

## REST API

The Spring Boot backend exposes startup data through:

```text
GET /startups
```

and supports validated startup creation through:

```text
POST /startups
```

Example:

```bash
curl http://localhost:8080/startups
```

## Dashboard

The frontend retrieves startup data from the Spring Boot API and displays:

- Total number of startups
- Total funding
- Average funding
- Searchable startup table
- Startup distribution by country
- Startup distribution by sector

Chart.js is used for the analytics visualizations.

## Scheduled Ingestion

The ingestion pipeline can run on a schedule using:

```text
ingestion/scheduler.py
```

The production source is configured through the `STARTUP_SOURCE_URL` environment variable.

Database credentials are also supplied through environment variables rather than being committed to the repository.

## Environment Variables

The project supports environment-based configuration such as:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
STARTUP_SOURCE_URL
```

Do not commit database passwords or `.env` files to the repository.

## Running the Tests

### Python

From the project root:

```bash
python -m pytest ingestion/tests -v
```

Current verified result:

```text
29 passed
```

### Spring Boot

```bash
cd backend
mvn test
```

Current verified result:

```text
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## Running the Backend with PostgreSQL

Set the required database environment variables, including `DB_PASSWORD`.

Then:

```bash
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=postgres
```

The API is available at:

```text
http://localhost:8080/startups
```

## Current Verification

The complete production data flow has been manually verified:

```text
Real External Source
        ↓
Extraction
        ↓
Transformation
        ↓
PostgreSQL
        ↓
Spring Boot API
        ↓
Frontend Dashboard
```

The verified dataset contains real startup records sourced through the production ETL pipeline rather than hard-coded production startup data.

Repeated ingestion has also been verified to avoid duplicate company records.

## Docker

The project includes Docker configuration for the backend and Docker Compose configuration for the application infrastructure.

```bash
docker compose up --build
```

## CI

A GitHub Actions workflow is included in:

```text
.github/workflows/ci.yml
```

The workflow is configured to automate project checks. Local Python and Spring Boot test suites have been independently verified successfully.

## Future Improvements

- Expand ingestion to additional reliable African startup data sources
- Increase startup coverage beyond the current ingestion batch
- Add historical funding snapshots and trend analysis
- Improve source monitoring and ingestion observability
- Deploy the application publicly
- Add richer analytics and filtering to the dashboard

## Author

Built by Twanano Rikhotso  
Software Engineering Student — WeThinkCode

WTC-KWUT5NS9
