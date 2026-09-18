from unittest.mock import MagicMock, patch

from ingestion.load import (
    build_connection_string,
    save_startups,
)
from ingestion.model import StartupInfo


@patch("ingestion.load.execute_values")
@patch("ingestion.load.psycopg2.connect")
def test_save_startups_uses_duplicate_safe_insert(
        mock_connect,
        mock_execute_values,
):
    connection = MagicMock()
    cursor = MagicMock()

    connection.cursor.return_value.__enter__.return_value = cursor
    cursor.rowcount = 1
    mock_connect.return_value = connection

    startups = [
        StartupInfo(
            company="Paystack",
            country="Nigeria",
            sector="FinTech",
            funding=200_000_000,
            source_url="https://example.com",
        ),
        StartupInfo(
            company="Paystack",
            country="Nigeria",
            sector="FinTech",
            funding=200_000_000,
            source_url="https://example.com",
        ),
    ]

    result = save_startups(startups, "test-connection")

    assert result is True

    mock_execute_values.assert_called_once()

    sql = mock_execute_values.call_args.args[1]

    assert "ON CONFLICT" in sql
    assert "DO NOTHING" in sql

    connection.commit.assert_called_once()
    connection.close.assert_called_once()


def test_build_connection_string():
    result = build_connection_string(
        host="localhost",
        database="startup_db",
        user="postgres",
        password="secret",
    )

    assert result == (
        "host=localhost "
        "dbname=startup_db "
        "user=postgres "
        "password=secret"
    )