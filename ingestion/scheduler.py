import logging
import os
import time

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

    startup_url = os.getenv("STARTUP_SOURCE_URL")
    database_url = os.getenv("DATABASE_URL")
    interval = int(
        os.getenv(
            "INGESTION_INTERVAL_SECONDS",
            str(DEFAULT_INTERVAL_SECONDS),
        )
    )

    if not startup_url:
        raise RuntimeError("STARTUP_SOURCE_URL environment variable is required")

    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    run_scheduled_ingestion(
        startup_url,
        database_url,
        interval,
    )