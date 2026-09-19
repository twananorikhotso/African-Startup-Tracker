import logging
import os
import time

from ingestion.load import build_connection_string
from ingestion.pipeline import run_pipeline


logger = logging.getLogger(__name__)

DEFAULT_INTERVAL_SECONDS = 60


def run_scheduled_ingestion(
        url: str,
        connection_string: str,
        interval_seconds: int = DEFAULT_INTERVAL_SECONDS,
) -> None:
    logger.info(
        "Scheduled ingestion started with interval of %d seconds",
        interval_seconds,
    )

    while True:
        logger.info("Starting scheduled ETL execution")

        try:
            success = run_pipeline(url, connection_string)

            if success:
                logger.info("Scheduled ETL execution completed successfully")
            else:
                logger.warning("Scheduled ETL execution was unsuccessful")

        except Exception:
            logger.exception("Scheduled ETL execution failed unexpectedly")

        logger.info(
            "Waiting %d seconds before next scheduled execution",
            interval_seconds,
        )

        time.sleep(interval_seconds)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    startup_url = os.getenv(
        "STARTUP_SOURCE_URL",
        "https://example.com",
    )

    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "startup_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD")

    interval = int(
        os.getenv(
            "INGESTION_INTERVAL_SECONDS",
            str(DEFAULT_INTERVAL_SECONDS),
        )
    )

    if not db_password:
        raise RuntimeError(
            "DB_PASSWORD environment variable is required"
        )

    connection_string = build_connection_string(
        db_host,
        db_name,
        db_user,
        db_password,
    )

    run_scheduled_ingestion(
        startup_url,
        connection_string,
        interval,
    )