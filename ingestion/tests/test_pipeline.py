from unittest.mock import patch

from ingestion.model import StartupInfo
from ingestion.pipeline import run_pipeline


@patch("ingestion.pipeline.save_startups")
@patch("ingestion.pipeline.transform_startups")
@patch("ingestion.pipeline.extract_startup_html")
def test_run_pipeline_coordinates_etl(
        mock_extract,
        mock_transform,
        mock_save,
):
    html = "<html>startup data</html>"

    startups = [
        StartupInfo(
            company="Paystack",
            country="Nigeria",
            sector="FinTech",
            funding=200_000_000,
            source_url="https://example.com/startups",
        )
    ]

    mock_extract.return_value = html
    mock_transform.return_value = startups
    mock_save.return_value = True

    result = run_pipeline(
        "https://example.com/startups",
        "test-connection",
    )

    assert result is True

    mock_extract.assert_called_once_with(
        "https://example.com/startups"
    )

    mock_transform.assert_called_once_with(
        html,
        "https://example.com/startups",
    )

    mock_save.assert_called_once_with(
        startups,
        "test-connection",
    )


@patch("ingestion.pipeline.extract_startup_html")
def test_run_pipeline_stops_when_extraction_fails(
        mock_extract,
):
    mock_extract.return_value = None

    result = run_pipeline(
        "https://example.com/startups",
        "test-connection",
    )

    assert result is False


@patch("ingestion.pipeline.save_startups")
@patch("ingestion.pipeline.transform_startups")
@patch("ingestion.pipeline.extract_startup_html")
def test_run_pipeline_stops_when_no_valid_data_found(
        mock_extract,
        mock_transform,
        mock_save,
):
    mock_extract.return_value = "<html></html>"
    mock_transform.return_value = []

    result = run_pipeline(
        "https://example.com/startups",
        "test-connection",
    )

    assert result is False
    mock_save.assert_not_called()