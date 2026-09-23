# African Startup Ecosystem Tracker

African Startup Ecosystem Tracker is a data engineering project that collects real African startup funding data and turns it into useful ecosystem insights.

The project uses a Python ETL pipeline to extract, clean, validate, and load startup data into PostgreSQL. A Spring Boot REST API exposes the processed data to a web dashboard for exploration and funding analysis.

## Features

* Real African startup data ingestion
* Data cleaning and validation
* Duplicate prevention
* PostgreSQL data storage
* Spring Boot REST API
* Searchable startup explorer
* Country and sector analytics
* Funding analytics
* Scheduled data ingestion
* Automated testing

## Architecture

```text
External Startup Data
        ↓
     Extract
        ↓
    Transform
        ↓
    PostgreSQL
        ↓
 Spring Boot API
        ↓
 Web Dashboard
```

The production pipeline currently collects public startup funding information from AU-Startups.

Before storage, records are normalized and validated, including company names, countries, sectors, and funding amounts. Duplicate protection allows the pipeline to run repeatedly without creating duplicate company records.

## Tech Stack

|                  | Technology                             |
| ---------------- | -------------------------------------- |
| Data Engineering | Python, Requests, BeautifulSoup        |
| Database         | PostgreSQL                             |
| Backend          | Java, Spring Boot                      |
| Frontend         | HTML, CSS, JavaScript, Chart.js        |
| Testing          | pytest, JUnit                          |
| DevOps           | Docker, Docker Compose, GitHub Actions |

## Setup

### Requirements

* Python
* Java
* Maven
* PostgreSQL
* Git

Install the Python dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The project uses the following environment variables:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
STARTUP_SOURCE_URL
```

Database credentials and `.env` files should not be committed to the repository.

## Run the Project

The project can be started using Docker Compose:

```bash
docker compose up --build
```

To run the Spring Boot backend directly:

```bash
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=postgres
```

The API is available at:

```text
http://localhost:8080/startups
```

## API

### GET `/startups`

Returns the startup records currently stored in the database.

```bash
curl http://localhost:8080/startups
```

### POST `/startups`

Creates a new startup record.

```json
{
  "company": "Example Startup",
  "country": "South Africa",
  "sector": "FinTech",
  "funding": 5000000
}
```

## Run the Tests

Python:

```bash
python -m pytest ingestion/tests -v
```

Spring Boot:

```bash
cd backend
mvn test
```

## Scope and Limitations

The current production pipeline uses AU-Startups as its external data source, so dataset coverage depends on the information available from that source.

The project currently runs locally and is intended as a data engineering and startup analytics platform rather than a complete database of every startup operating in Africa.

## Future Improvements

* Add more reliable African startup data sources
* Expand startup and funding coverage
* Add historical funding trends
* Improve dashboard analytics and filtering
* Deploy the platform publicly

## Author

Built by **Twanano Rikhotso**
Software Engineering Student — WeThinkCode

WTC-KWUT5NS9
