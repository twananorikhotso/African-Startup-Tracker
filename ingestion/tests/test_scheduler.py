from unittest.mock import patch

from ingestion.scheduler import run_scheduled_ingestion


@patch("ingestion.scheduler.time.sleep")
@patch("ingestion.scheduler.run_pipeline")
def test_scheduler_invokes_pipeline(
        mock_run_pipeline,
        mock_sleep,
):
    mock_run_pipeline.return_value = True

    mock_sleep.side_effect = KeyboardInterrupt

    try:
        run_scheduled_ingestion(
            "https://example.com/startups",
            "test-connection",
            interval_seconds=60,
        )
    except KeyboardInterrupt:
        pass

    mock_run_pipeline.assert_called_once_with(
        "https://example.com/startups",
        "test-connection",
    )

    mock_sleep.assert_called_once_with(60)


@patch("ingestion.scheduler.time.sleep")
@patch("ingestion.scheduler.run_pipeline")
def test_scheduler_continues_when_pipeline_fails(
        mock_run_pipeline,
        mock_sleep,
):
    mock_run_pipeline.return_value = False

    mock_sleep.side_effect = KeyboardInterrupt

    try:
        run_scheduled_ingestion(
            "https://example.com/startups",
            "test-connection",
            interval_seconds=30,
        )
    except KeyboardInterrupt:
        pass

    mock_run_pipeline.assert_called_once()

    mock_sleep.assert_called_once_with(30)