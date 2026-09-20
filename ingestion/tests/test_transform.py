from ingestion.transform import (
    clean_funding,
    normalize_company,
    normalize_country,
    normalize_sector,
    transform_startups,
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
    assert normalize_sector(
        "  financial   technology  "
    ) == "Financial Technology"
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

def test_transform_startups_creates_clean_valid_records():
    html = """
    <main>
        <h1 class="text-white">
            Sycamore
        </h1>

        <a href="/sectors/fintech">
            Fintech
        </a>

        <p class="funding-total">
            $5.0M
        </p>

        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Sycamore",
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "NG"
            }
        }
        </script>
    </main>
    """

    source_url = (
        "https://au-startups.com/startups/sycamore"
    )

    startups = transform_startups(
        html,
        source_url,
    )

    assert len(startups) == 1

    startup = startups[0]

    assert startup.company == "Sycamore"
    assert startup.country == "Nigeria"
    assert startup.sector == "Fintech"
    assert startup.funding == 5_000_000
    assert startup.source_url == source_url