import argparse
import logging
from typing import List

import psycopg2
from psycopg2.extras import execute_values

from ingestion.model import StartupInfo
from ingestion.extract import extract_startup_html
from ingestion.transform import (
    clean_funding,
    normalize_company,
    normalize_country,
    normalize_sector,
    transform_startups,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def fetch_startups(url: str) -> List[StartupInfo]:
    html = extract_startup_html(url)

    if html is None:
        return []

    return transform_startups(html, url)


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