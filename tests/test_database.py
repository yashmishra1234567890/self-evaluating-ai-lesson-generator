
import json
import pytest

from database.schema import create_tables
from database.operations import (
    create_run,
    save_evaluation_log,
    save_final_lesson,
    get_run_history,
    get_evaluation_logs,
    update_failure_count,
    get_historical_guidance
)


@pytest.fixture
def database(monkeypatch, tmp_path):

    db_path = tmp_path / "test_database.db"

    monkeypatch.setenv(
        "DATABASE_PATH",
        str(db_path)
    )

    create_tables()

    return db_path


def test_create_run(database):

    run_id = create_run("Introduction to RAG")

    history = get_run_history(run_id)

    assert history is not None
    assert history["topic"] == "Introduction to RAG"
    assert history["status"] == "in_progress"


def test_save_evaluation_log(database):

    run_id = create_run("Introduction to RAG")

    save_evaluation_log(
        run_id,
        1,
        "Test lesson",
        ["E1", "E2"],
        ["E4"],
        {"feedback": "Explain jargon"},
        False
    )

    logs = get_evaluation_logs(run_id)

    assert len(logs) == 1
    assert logs[0]["is_passing"] == 0
    assert json.loads(
        logs[0]["failed_checkpoint_ids"]
    ) == ["E4"]


def test_learning_memory(database):

    update_failure_count("E4", "Explain jargon simply.")
    update_failure_count("E4", "Use simple examples.")

    guidance = get_historical_guidance()

    assert len(guidance) == 1
    assert guidance[0]["total_failure_count"] == 2


def test_save_final_lesson(database):

    run_id = create_run("Introduction to RAG")

    save_final_lesson(
        run_id,
        "RAG retrieves relevant information before generation."
    )

    history = get_run_history(run_id)

    assert history["status"] == "shipped"
    assert history["final_lesson_content"] is not None
