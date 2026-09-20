import re
import logging
from typing import List

from bs4 import BeautifulSoup

from ingestion.model import StartupInfo

logger = logging.getLogger(__name__)
COUNTRY_CODES = {
    "NG": "Nigeria",
    "ZA": "South Africa",
    "KE": "Kenya",
    "EG": "Egypt",
    "GH": "Ghana",
    "MA": "Morocco",
    "CI": "Cote d'Ivoire",
    "TN": "Tunisia",
    "RW": "Rwanda",
    "SN": "Senegal",
    "ET": "Ethiopia",
    "TZ": "Tanzania",
    "UG": "Uganda",
}


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

def country_from_code(value: str | None) -> str:
    if not value:
        return "Unknown"

    code = value.strip().upper()

    return COUNTRY_CODES.get(code, "Unknown")


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

    value = value.replace(",", "")

    value = re.sub(
        r"\s+MILLION$",
        "M",
        value,
    )

    value = re.sub(
        r"\s+BILLION$",
        "B",
        value,
    )

    value = re.sub(
        r"\s+THOUSAND$",
        "K",
        value,
    )

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

    company_element = soup.select_one(
        'main h1[class*="text-white"]'
    )

    sector_element = soup.select_one(
        'a[href^="/sectors/"]'
    )

    country_code = None

    for script in soup.find_all(
            "script",
            type="application/ld+json",
    ):
        script_text = script.string

        if not script_text:
            continue

        match = re.search(
            r'"addressCountry"\s*:\s*"([^"]+)"',
            script_text,
        )

        if match:
            country_code = match.group(1)
            break

    funding_element = None

    for paragraph in soup.find_all("p"):
        text = paragraph.get_text(strip=True)

        if re.fullmatch(
                r"\$[\d,.]+[KMB]?",
                text,
                flags=re.IGNORECASE,
        ):
            funding_element = paragraph
            break

    if not company_element:
        logger.warning(
            "Skipping startup profile with missing company name"
        )
        return []

    if funding_element is None:
        logger.warning(
            "Skipping startup profile with missing or undisclosed funding"
        )
        return []

    startup = StartupInfo(
        company=normalize_company(
            company_element.get_text(strip=True)
        ),
        country=country_from_code(country_code),
        sector=normalize_sector(
            sector_element.get_text(strip=True)
            if sector_element else None
        ),
        funding=clean_funding(
            funding_element.get_text(strip=True)
            if funding_element else None
        ),
        source_url=source_url,
    )

    if not startup.is_valid():
        logger.warning(
            "Skipping invalid startup: %s",
            startup,
        )
        return []

    return [startup]
