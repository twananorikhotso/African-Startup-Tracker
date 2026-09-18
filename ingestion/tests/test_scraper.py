from unittest.mock import patch

from ingestion.scraper import (
    StartupInfo,
    clean_funding,
    fetch_startups,
    normalize_company,
    normalize_country,
    normalize_sector,
    save_startups,
)

def test_normalize_company_cleans_whitespace():
    assert normalize_company("  Flutterwave  ") == "Flutterwave"
    assert normalize_company("  M-KOPA   Solar  ") == "M-KOPA Solar"
    assert normalize_company(None) == ""


def test_normalize_country_cleans_values():
    assert normalize_country("  south   africa  ") == "South Africa"
    assert normalize_country("NIGERIA") == "Nigeria"
    assert normalize_country("") == "Unknown"
    assert normalize_country(None) == "Unknown"


def test_normalize_sector_cleans_values():
    assert normalize_sector("  financial   technology  ") == "Financial Technology"
    assert normalize_sector("FINTECH") == "Fintech"
    assert normalize_sector("") == "Unknown"
    assert normalize_sector(None) == "Unknown"


def test_clean_funding_converts_common_amounts():
    assert clean_funding("$500K") == 500_000
    assert clean_funding("$2M") == 2_000_000
    assert clean_funding("$1.5B") == 1_500_000_000
    assert clean_funding("$250000") == 250_000


def test_clean_funding_handles_missing_and_unknown_values():
    assert clean_funding(None) == 0
    assert clean_funding("") == 0
    assert clean_funding("N/A") == 0
    assert clean_funding("Unknown") == 0
    assert clean_funding("Undisclosed") == 0


def test_valid_startup_passes_validation():
    startup = StartupInfo(
        company="Paystack",
        country="Nigeria",
        sector="FinTech",
        funding=200_000_000,
        source_url="https://example.com",
    )

    assert startup.is_valid() is True


def test_startup_with_missing_company_is_invalid():
    startup = StartupInfo(
        company="",
        country="Nigeria",
        sector="FinTech",
        funding=1_000_000,
        source_url="https://example.com",
    )

    assert startup.is_valid() is False


def test_startup_with_unknown_country_is_invalid():
    startup = StartupInfo(
        company="Example Startup",
        country="Unknown",
        sector="FinTech",
        funding=1_000_000,
        source_url="https://example.com",
    )

    assert startup.is_valid() is False


def test_startup_with_unknown_sector_is_invalid():
    startup = StartupInfo(
        company="Example Startup",
        country="Nigeria",
        sector="Unknown",
        funding=1_000_000,
        source_url="https://example.com",
    )

    assert startup.is_valid() is False


def test_startup_with_negative_funding_is_invalid():
    startup = StartupInfo(
        company="Example Startup",
        country="Nigeria",
        sector="FinTech",
        funding=-1,
        source_url="https://example.com",
    )

    assert startup.is_valid() is False


@patch("ingestion.scraper.extract_startup_html")
def test_fetch_startups_skips_invalid_startup_data(mock_extract):
    html = """
    <div class="startup-card">
        <div class="company-name">Missing Details Startup</div>
    </div>
    """

    mock_extract.return_value = html

    startups = fetch_startups(
        "https://example.com/startups"
    )

    assert startups == []