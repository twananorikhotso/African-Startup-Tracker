from unittest.mock import MagicMock, patch
from ingestion.extract import (
    extract_startup_html,
    extract_startup_links,
)
import requests

from ingestion.extract import extract_startup_html


@patch("ingestion.extract.requests.get")
def test_extract_startup_html_returns_response_html(mock_get):
    response = MagicMock()
    response.text = "<html><body>Startup data</body></html>"
    response.status_code = 200
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    result = extract_startup_html("https://example.com/startups")

    assert result == "<html><body>Startup data</body></html>"

    mock_get.assert_called_once_with(
        "https://example.com/startups",
        headers=mock_get.call_args.kwargs["headers"],
        timeout=15,
    )


@patch("ingestion.extract.requests.get")
def test_extract_startup_html_handles_request_failure(mock_get):
    mock_get.side_effect = requests.RequestException("Connection failed")

    result = extract_startup_html("https://example.com/startups")

    assert result is None

def test_extract_startup_links_discovers_unique_profiles():
    html = """
    <html>
        <body>
            <a href="/startups/sycamore">Sycamore</a>
            <a href="/startups/flot">Flot</a>
            <a href="/startups/sycamore">Sycamore again</a>
            <a href="/funding">Funding</a>
        </body>
    </html>
    """

    links = extract_startup_links(
        html,
        "https://au-startups.com/funding",
        limit=10,
    )

    assert links == [
        "https://au-startups.com/startups/sycamore",
        "https://au-startups.com/startups/flot",
    ]