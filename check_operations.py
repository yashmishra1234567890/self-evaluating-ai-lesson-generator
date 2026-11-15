
import json

from database.schema import create_tables
from database.operations import (
    create_run,
    save_evaluation_log,
    update_failure_count,
    get_historical_guidance,
    get_run_history,
    get_evaluation_logs,
    save_final_lesson
)


def test_database_operations():

    create_tables()

    # 1. Create run
    run_id = create_run("Introduction to RAG")

    print("Created Run:", run_id)

    # 2. Save evaluation
    feedback = {
        "overall_feedback": "Technical jargon needs improvement"
    }

    save_evaluation_log(
        run_id=run_id,
        attempt_number=1,
        draft_content="RAG uses embeddings.",
        passed_checkpoint_ids=["E1", "E5"],
        failed_checkpoint_ids=["E4"],
        evaluator_feedback=feedback,
        is_passing=False
    )

    # 3. Update learning memory
    update_failure_count(
        "E4",
        "Explain technical terms using simple language."
    )

    # 4. Increment same checkpoint again
    update_failure_count(
        "E4",
        "Explain technical terms with simple examples."
    )

    # 5. Retrieve memory
    guidance = get_historical_guidance()

    print("Historical Guidance:", guidance)

    assert guidance[0]["total_failure_count"] == 2

    # 6. Retrieve evaluation history
    logs = get_evaluation_logs(run_id)

    assert len(logs) == 1

    print("Evaluation Logs:", logs)

    # 7. Save final lesson
    save_final_lesson(
        run_id,
        "RAG helps an AI find useful information before answering."
    )

    history = get_run_history(run_id)

    assert history["status"] == "shipped"

    print("Final Run Status:", history["status"])

    print("All database operations passed!")


if __name__ == "__main__":
    test_database_operations()
