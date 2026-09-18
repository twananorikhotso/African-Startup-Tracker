import logging
from typing import List

from ingestion.extract import extract_startup_html
from ingestion.load import save_startups
from ingestion.model import StartupInfo
from ingestion.transform import transform_startups


logger = logging.getLogger(__name__)


def run_pipeline(
        url: str,
        connection_string: str,
) -> bool:
    logger.info("Starting ETL pipeline for %s", url)

    # Extract
    html = extract_startup_html(url)

    if html is None:
        logger.warning("ETL pipeline stopped during extraction")
        return False

    # Transform
    startups: List[StartupInfo] = transform_startups(
        html,
        url,
    )

    if not startups:
        logger.warning(
            "ETL pipeline stopped because no valid startup data was found"
        )
        return False

    # Load
    if not save_startups(startups, connection_string):
        logger.error("ETL pipeline stopped during loading")
        return False

    logger.info(
        "ETL pipeline completed successfully with %d startup records",
        len(startups),
    )

    return True