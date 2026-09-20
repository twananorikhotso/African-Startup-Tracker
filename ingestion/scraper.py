import argparse
import logging
from typing import List
from ingestion.pipeline import run_pipeline

from ingestion.model import StartupInfo
from ingestion.extract import extract_startup_html
from ingestion.transform import (
    clean_funding,
    normalize_company,
    normalize_country,
    normalize_sector,
    transform_startups,
)
from ingestion.load import (
    build_connection_string,
    save_startups,
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape and ingest startup funding data."
    )
    parser.add_argument(
        "--url",
        help="Source website URL to scrape",
        required="True",
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

    args = parser.parse_args()

    connection_string = build_connection_string(
        args.host,
        args.database,
        args.user,
        args.password,
    )

    logger.info("Running startup ETL pipeline for %s", args.url)

    if not run_pipeline(args.url, connection_string):
        logger.warning("Startup ETL pipeline did not complete successfully")

if __name__ == "__main__":
    main()