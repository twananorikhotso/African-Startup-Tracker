from unittest.mock import patch

from ingestion.model import StartupInfo
from ingestion.pipeline import run_pipeline


@patch("ingestion.pipeline.save_startups")
@patch("ingestion.pipeline.transform_startups")
@patch("ingestion.pipeline.extract_startup_links")
@patch("ingestion.pipeline.extract_startup_html")
def test_run_pipeline_coordinates_etl(
        mock_extract,
        mock_links,
        mock_transform,
        mock_save,
):
    funding_html = "<html>funding page</html>"
    profile_html = "<html>startup profile</html>"

    profile_url = (
        "https://au-startups.com/startups/sycamore"
    )

    startups = [
        StartupInfo(
            company="Sycamore",
            country="Nigeria",
            sector="Fintech",
            funding=5_000_000,
            source_url=profile_url,
        )
    ]

    mock_extract.side_effect = [
        funding_html,
        profile_html,
    ]

    mock_links.return_value = [profile_url]
    mock_transform.return_value = startups
    mock_save.return_value = True

    result = run_pipeline(
        "https://au-startups.com/funding",
        "test-connection",
    )

    assert result is True

    assert mock_extract.call_count == 2

    mock_links.assert_called_once_with(
        funding_html,
        "https://au-startups.com/funding",
        limit=10,
    )

    mock_transform.assert_called_once_with(
        profile_html,
        profile_url,
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
@patch("ingestion.pipeline.extract_startup_links")
@patch("ingestion.pipeline.extract_startup_html")
def test_run_pipeline_stops_when_no_valid_data_found(
        mock_extract,
        mock_links,
        mock_transform,
        mock_save,
):
    funding_html = "<html>funding page</html>"
    profile_html = "<html>startup profile</html>"

    profile_url = (
        "https://au-startups.com/startups/sycamore"
    )

    mock_extract.side_effect = [
        funding_html,
        profile_html,
    ]

    mock_links.return_value = [profile_url]
    mock_transform.return_value = []

    result = run_pipeline(
        "https://au-startups.com/funding",
        "test-connection",
    )

    assert result is False
    mock_save.assert_not_called()