import logging
from typing import List

from ingestion.extract import (
    extract_startup_html,
    extract_startup_links,
)
from ingestion.load import save_startups
from ingestion.model import StartupInfo
from ingestion.transform import transform_startups


logger = logging.getLogger(__name__)


def run_pipeline(
        url: str,
        connection_string: str,
) -> bool:
    logger.info("Starting ETL pipeline for %s", url)

    # Extract funding page
    html = extract_startup_html(url)

    if html is None:
        logger.warning("ETL pipeline stopped during extraction")
        return False

    # Discover startup profile URLs
    startup_urls = extract_startup_links(
        html,
        url,
        limit=10,
    )

    if not startup_urls:
        logger.warning(
            "ETL pipeline stopped because no startup profiles were found"
        )
        return False

    startups: List[StartupInfo] = []

    # Extract and transform each startup profile
    for startup_url in startup_urls:
        profile_html = extract_startup_html(startup_url)

        if profile_html is None:
            logger.warning(
                "Skipping startup profile that could not be extracted: %s",
                startup_url,
            )
            continue

        transformed = transform_startups(
            profile_html,
            startup_url,
        )

        startups.extend(transformed)

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