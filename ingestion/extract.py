import logging
import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def extract_startup_html(url: str) -> str | None:
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
            "Successfully extracted startup data from %s with status %d",
            url,
            response.status_code,
        )

        return response.text

    except requests.RequestException as error:
        logger.error("Failed to extract startup data: %s", error)
        return None

def extract_startup_links(
        html: str,
        base_url: str,
        limit: int = 10,
) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    startup_urls = []
    seen_urls = set()

    for link in soup.select('a[href^="/startups/"]'):
        href = link.get("href")

        if not href:
            continue

        startup_url = urljoin(base_url, href)

        if startup_url in seen_urls:
            continue

        seen_urls.add(startup_url)
        startup_urls.append(startup_url)

        if len(startup_urls) >= limit:
            break

    logger.info(
        "Discovered %d startup profile URLs",
        len(startup_urls),
    )

    return startup_urls