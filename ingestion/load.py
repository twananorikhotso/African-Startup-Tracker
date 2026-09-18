import logging
from typing import List

import psycopg2
from psycopg2.extras import execute_values

from ingestion.model import StartupInfo


logger = logging.getLogger(__name__)


def save_startups(
        startups: List[StartupInfo],
        connection_string: str,
) -> bool:
    try:
        conn = psycopg2.connect(connection_string)
        logger.info("Successfully connected to PostgreSQL")

    except psycopg2.Error as error:
        logger.error("Database connection failed: %s", error)
        return False

    try:
        with conn.cursor() as cursor:
            execute_values(
                cursor,
                """
                INSERT INTO startups (
                    company_name,
                    origin_country,
                    target_sector,
                    funding_amount,
                    source_url
                )
                VALUES %s
                    ON CONFLICT (LOWER(BTRIM(company_name)))
                DO NOTHING
                """,
                [
                    (
                        startup.company,
                        startup.country,
                        startup.sector,
                        startup.funding,
                        startup.source_url,
                    )
                    for startup in startups
                ],
            )

            inserted_count = cursor.rowcount
            conn.commit()

            logger.info(
                "Saved %d new startup records; skipped %d duplicates",
                inserted_count,
                len(startups) - inserted_count,
                )

            return True

    except psycopg2.Error as error:
        conn.rollback()
        logger.error("Failed to save startup data: %s", error)
        return False

    finally:
        conn.close()


def build_connection_string(
        host: str,
        database: str,
        user: str,
        password: str,
) -> str:
    return (
        f"host={host} "
        f"dbname={database} "
        f"user={user} "
        f"password={password}"
    )