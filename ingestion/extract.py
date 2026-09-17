import logging

import requests


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