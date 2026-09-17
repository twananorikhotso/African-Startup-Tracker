import argparse
import logging
import re
from ingestion.model import StartupInfo
from typing import List

import psycopg2
import requests
from bs4 import BeautifulSoup
from psycopg2.extras import execute_values


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def normalize_company(value: str | None) -> str:
    if not value:
        return ""

    return " ".join(value.split())


def normalize_country(value: str | None) -> str:
    if not value:
        return "Unknown"

    cleaned = " ".join(value.split()).strip()

    if not cleaned:
        return "Unknown"

    return cleaned.title()


def normalize_sector(value: str | None) -> str:
    if not value:
        return "Unknown"

    cleaned = " ".join(value.split()).strip()

    if not cleaned:
        return "Unknown"

    return cleaned.title()

def clean_funding(value: str | None) -> int:
    if not value:
        return 0

    value = value.strip().upper()

    if value in {"N/A", "UNDISCLOSED", "UNKNOWN"}:
        return 0

    try:
        multiplier = 1

        if value.endswith("K"):
            multiplier = 1_000
            value = value[:-1]
        elif value.endswith("M"):
            multiplier = 1_000_000
            value = value[:-1]
        elif value.endswith("B"):
            multiplier = 1_000_000_000
            value = value[:-1]

        numeric_value = re.sub(r"[^0-9.]", "", value)

        if not numeric_value:
            return 0

        return int(float(numeric_value) * multiplier)

    except (ValueError, TypeError):
        return 0


def fetch_startups(url: str) -> List[StartupInfo]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/152.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        logger.info(
            "Successfully fetched startup data from %s with status %d",
            url,
            response.status_code,
        )
    except requests.RequestException as error:
        logger.error("Failed to fetch startup data: %s", error)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    startup_links = soup.select('a[href^="/startups/"]')
    logger.info("Found %d startup links", len(startup_links))

    startups = []

    for card in soup.select(".startup-card, .deal-card, .company-card"):
        company = card.select_one(".company-name, .name")
        country = card.select_one(".country, .location")
        sector = card.select_one(".sector, .category")
        funding = card.select_one(".funding, .amount")

        if not company:
            logger.warning("Skipping startup card with missing company name")
            continue

        startup = StartupInfo(
            company=normalize_company(
                company.get_text(strip=True)
            ),
            country=normalize_country(
                country.get_text(strip=True) if country else None
            ),
            sector=normalize_sector(
                sector.get_text(strip=True) if sector else None
            ),
            funding=clean_funding(
                funding.get_text(strip=True) if funding else None
            ),
            source_url=url,
        )

        if not startup.is_valid():
            logger.warning("Skipping invalid startup: %s", startup)
            continue

        startups.append(startup)

    return startups


def save_startups(startups: List[StartupInfo], connection_string: str):
    try:
        conn = psycopg2.connect(connection_string)
        logger.info("Successfully connected to PostgreSQL")
    except psycopg2.Error as error:
        logger.error("Database connection failed: %s", error)
        return False

    try:
        with conn.cursor() as cursor:
            execute_values(
                cursor,
                """
                INSERT INTO startups (
                    company_name,
                    origin_country,
                    target_sector,
                    funding_amount,
                    source_url
                )
                VALUES %s
                ON CONFLICT (LOWER(BTRIM(company_name)))
                DO NOTHING
                """,
                [
                    (
                        s.company,
                        s.country,
                        s.sector,
                        s.funding,
                        s.source_url,
                    )
                    for s in startups
                ],
            )

            inserted_count = cursor.rowcount
            conn.commit()
            logger.info(
                "Saved %d new startup records; skipped %d duplicates",
                inserted_count,
                len(startups) - inserted_count,
                )
            return True

    except psycopg2.Error as error:
        conn.rollback()
        logger.error("Failed to save startup data: %s", error)
        return False

    finally:
        conn.close()


def seed_sample_startup(connection_string: str):
    sample = StartupInfo(
        company="Paystack",
        country="Nigeria",
        sector="FinTech",
        funding=200000000,
        source_url="https://example.com",
    )

    if save_startups([sample], connection_string):
        logger.info("Sample startup ingestion completed")


def build_connection_string(
        host: str,
        database: str,
        user: str,
        password: str,
) -> str:
    return f"host={host} dbname={database} user={user} password={password}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape and ingest startup funding data."
    )
    parser.add_argument(
        "--url",
        help="Source website URL to scrape",
        default="https://example.com",
    )
    parser.add_argument("--host", help="PostgreSQL host", default="localhost")
    parser.add_argument(
        "--database",
        help="PostgreSQL database",
        default="startup_db",
    )
    parser.add_argument("--user", help="PostgreSQL user", default="postgres")
    parser.add_argument(
        "--password",
        help="PostgreSQL password",
        default="postgres",
    )
    parser.add_argument(
        "--seed-sample",
        help="Seed sample startup data instead of scraping",
        action="store_true",
    )

    args = parser.parse_args()

    connection_string = build_connection_string(
        args.host,
        args.database,
        args.user,
        args.password,
    )

    if args.seed_sample:
        seed_sample_startup(connection_string)
        return

    logger.info("Scraping startups from %s", args.url)

    startups = fetch_startups(args.url)

    if not startups:
        logger.warning(
            "No startup entries were detected. "
            "Check the URL or update scraping selectors."
        )
        return

    if save_startups(startups, connection_string):
        logger.info("Imported %d startups into PostgreSQL", len(startups))


if __name__ == "__main__":
    main()