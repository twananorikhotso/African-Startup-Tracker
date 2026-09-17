import re
import logging
from typing import List

from bs4 import BeautifulSoup

from ingestion.model import StartupInfo

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

def transform_startups(
        html: str,
        source_url: str,
) -> List[StartupInfo]:
    soup = BeautifulSoup(html, "html.parser")

    startup_links = soup.select('a[href^="/startups/"]')
    logger.info("Found %d startup links", len(startup_links))

    startups = []

    for card in soup.select(
            ".startup-card, .deal-card, .company-card"
    ):
        company = card.select_one(".company-name, .name")
        country = card.select_one(".country, .location")
        sector = card.select_one(".sector, .category")
        funding = card.select_one(".funding, .amount")

        if not company:
            logger.warning(
                "Skipping startup card with missing company name"
            )
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
            source_url=source_url,
        )

        if not startup.is_valid():
            logger.warning(
                "Skipping invalid startup: %s",
                startup,
            )
            continue

        startups.append(startup)

    return startups