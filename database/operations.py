
import json
import uuid

from database.connection import get_connection


def create_run(topic: str, run_id: str = None) -> str:
    """
    Create a new lesson generation run.

    Returns:
        str: Unique run ID.
    """

    if not run_id:
        run_id = str(uuid.uuid4())

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO runs (run_id, topic)
            VALUES (?, ?)
            """,
            (run_id, topic)
        )

        connection.commit()

        return run_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def update_run_status(run_id: str, status: str) -> None:
    """
    Update the status of an existing run.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE runs
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE run_id = ?
            """,
            (status, run_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Run ID not found")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def save_final_lesson(run_id: str, lesson: str) -> None:
    """
    Save the final passing lesson and mark run as shipped.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE runs
            SET final_lesson_content = ?,
                status = 'shipped',
                updated_at = CURRENT_TIMESTAMP
            WHERE run_id = ?
            """,
            (lesson, run_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Run ID not found")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def save_evaluation_log(
    run_id: str,
    attempt_number: int,
    draft_content: str,
    passed_checkpoint_ids: list,
    failed_checkpoint_ids: list,
    evaluator_feedback: dict,
    is_passing: bool
) -> None:
    """
    Save the complete evaluation result for one attempt.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO evaluation_logs (
                run_id,
                attempt_number,
                draft_content,
                passed_checkpoint_ids,
                failed_checkpoint_ids,
                evaluator_feedback_json,
                is_passing
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                attempt_number,
                draft_content,
                json.dumps(passed_checkpoint_ids),
                json.dumps(failed_checkpoint_ids),
                json.dumps(evaluator_feedback),
                int(is_passing)
            )
        )

        cursor.execute(
            """
            UPDATE runs
            SET total_attempts = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE run_id = ?
            """,
            (attempt_number, run_id)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_run_history(run_id: str):
    """
    Retrieve details of a specific run.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM runs
            WHERE run_id = ?
            """,
            (run_id,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        return dict(result)

    finally:
        connection.close()


def get_evaluation_logs(run_id: str):
    """
    Retrieve all evaluation attempts for a run.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM evaluation_logs
            WHERE run_id = ?
            ORDER BY attempt_number ASC
            """,
            (run_id,)
        )

        results = cursor.fetchall()

        return [dict(row) for row in results]

    finally:
        connection.close()


def update_failure_count(
    checkpoint_id: str,
    guidance: str
) -> None:
    """
    Insert a new failure pattern or increment its count.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO learning_memory (
                checkpoint_id,
                total_failure_count,
                historical_guidance,
                last_triggered_at
            )
            VALUES (?, 1, ?, CURRENT_TIMESTAMP)

            ON CONFLICT(checkpoint_id)
            DO UPDATE SET
                total_failure_count =
                    total_failure_count + 1,

                historical_guidance = excluded.historical_guidance,

                last_triggered_at = CURRENT_TIMESTAMP
            """,
            (checkpoint_id, guidance)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_historical_guidance(limit: int = 3):
    """
    Retrieve the most frequent historical failure patterns.
    """

    if limit < 1:
        raise ValueError("Limit must be at least 1")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                checkpoint_id,
                total_failure_count,
                historical_guidance
            FROM learning_memory
            ORDER BY
                total_failure_count DESC,
                last_triggered_at DESC
            LIMIT ?
            """,
            (limit,)
        )

        results = cursor.fetchall()

        return [dict(row) for row in results]

    finally:
        connection.close()

def get_rejection_log(run_id: str) -> list:
    """
    Retrieve rejected attempts for a specific workflow run.
    Reconstructs rejection history from persisted evaluation logs.
    """

    logs = get_evaluation_logs(run_id)

    rejection_log = []

    for log in logs:

        if log["is_passing"] == 0:

            evaluator_feedback = json.loads(
                log["evaluator_feedback_json"]
            )

            rejection_log.append({
                "attempt": log["attempt_number"],
                "failed_checkpoint_ids": json.loads(
                    log["failed_checkpoint_ids"]
                ),
                "feedback": evaluator_feedback.get(
                    "overall_feedback",
                    "Lesson failed evaluation."
                )
            })

    return rejection_log
