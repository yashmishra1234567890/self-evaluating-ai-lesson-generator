
"""
Workflow Nodes

Contains memory, generation, evaluation,
retry, and system-error handling nodes.
"""

from agent.generator import generate_lesson
from agent.evaluator import evaluate_lesson

from database.operations import (
    get_historical_guidance,
    save_evaluation_log,
    update_failure_count
)


def load_memory_node(state: dict) -> dict:
    """
    Load historical failure guidance from SQLite.
    """

    historical_guidance = get_historical_guidance(limit=3)

    return {
        "historical_guidance": historical_guidance
    }


def generate_lesson_node(state: dict) -> dict:
    """
    Generate a lesson using the Generator Agent.

    API or generation errors are returned as system errors.
    """

    print("\nGenerating lesson...")

    try:
        lesson = generate_lesson(
            topic=state["topic"],
            target_audience=state["target_audience"],
            historical_guidance=state.get("historical_guidance", []),
            rejection_log=state.get("rejection_log", []),
            previous_draft=state.get("current_draft")
        )

        if not lesson or not lesson.strip():
            raise ValueError("Generator returned empty lesson content.")

        print("Lesson generated successfully.")

        return {
            "current_draft": lesson,
            "system_error": "",
            "system_error_stage": "",
            "status": "running"
        }

    except Exception as error:
        print("\nGENERATION SYSTEM ERROR:", str(error))

        return {
            "system_error": str(error),
            "system_error_stage": "generation",
            "status": "system_error"
        }


def evaluate_lesson_node(state: dict) -> dict:
    """
    Evaluate the generated lesson and save its results.

    Supports controlled failure simulation for testing.
    Evaluator/API errors are treated as system errors,
    not as lesson rubric failures.
    """

    print("\nEvaluating lesson...")

    try:
        result = evaluate_lesson(
            topic=state["topic"],
            lesson_content=state["current_draft"]
        )

    except Exception as error:
        print("\nEVALUATION SYSTEM ERROR:", str(error))

        return {
            "system_error": str(error),
            "system_error_stage": "evaluation",
            "status": "system_error"
        }

    # Extract evaluation result
    evaluation = result["evaluation"]

    is_passing = result["is_passing"]

    passed_ids = list(result["passed_checkpoint_ids"])
    failed_ids = list(result["failed_checkpoint_ids"])

    summary = result["summary"]

    attempt_number = state.get("retry_count", 0) + 1

    evaluation_data = evaluation.model_dump()

    # -------------------------------------------------
    # CONTROLLED FAILURE SIMULATION
    # -------------------------------------------------

    simulate_first = (
        state.get("simulate_first_failure", False)
        and state.get("retry_count", 0) == 0
    )

    simulate_all = state.get(
        "simulate_all_attempts_failure",
        False
    )

    simulated_failure = simulate_first or simulate_all

    if simulated_failure:
        print(
            f"\n[TEST MODE] Simulating failure on attempt "
            f"{attempt_number}: E3"
        )

        for check in evaluation_data.get("checks", []):
            if check.get("checkpoint_id") == "E3":
                check["passed"] = False

                check["reason"] = (
                    "Controlled test: E3 deliberately failed."
                )

                check["feedback"] = (
                    "TEST FAILURE: Improve the simplicity of the language."
                )

        is_passing = False

        if "E3" in passed_ids:
            passed_ids.remove("E3")

        if "E3" not in failed_ids:
            failed_ids.append("E3")

        summary = (
            f"Controlled test failure on attempt {attempt_number}: "
            "E3 was deliberately failed to verify the workflow."
        )

    # -------------------------------------------------
    # SAVE EVALUATION LOG
    # -------------------------------------------------

    save_evaluation_log(
        run_id=state["run_id"],
        attempt_number=attempt_number,
        draft_content=state["current_draft"],
        passed_checkpoint_ids=passed_ids,
        failed_checkpoint_ids=failed_ids,
        evaluator_feedback=evaluation_data,
        is_passing=is_passing
    )

    # -------------------------------------------------
    # UPDATE HISTORICAL MEMORY
    # Do not store synthetic test failures.
    # -------------------------------------------------

    if not simulated_failure:
        checks = evaluation_data.get("checks", [])

        for check in checks:
            checkpoint_id = check.get("checkpoint_id")

            if checkpoint_id in failed_ids:
                guidance = (
                    check.get("feedback")
                    or summary
                )

                update_failure_count(
                    checkpoint_id=checkpoint_id,
                    guidance=guidance
                )

    # -------------------------------------------------
    # MAINTAIN REJECTION HISTORY
    # -------------------------------------------------

    rejection_log = list(
        state.get("rejection_log", [])
    )

    if not is_passing:
        rejection_log.append({
            "attempt": attempt_number,
            "failed_checkpoint_ids": failed_ids,
            "feedback": summary
        })

    # -------------------------------------------------
    # PRINT EVALUATION RESULT
    # -------------------------------------------------

    print("\nEvaluation completed.")
    print("Attempt:", attempt_number)
    print("Passed checkpoints:", passed_ids)
    print("Failed checkpoints:", failed_ids)
    print("Passing:", is_passing)

    return {
        "is_passing": is_passing,

        "evaluation_results": (
            list(state.get("evaluation_results", []))
            + [evaluation_data]
        ),

        "rejection_log": rejection_log,

        "system_error": "",
        "system_error_stage": "",
        "status": "running"
    }


def increment_retry_node(state: dict) -> dict:
    """
    Increment retry count after a failed evaluation.
    """

    new_retry_count = state.get("retry_count", 0) + 1

    print(
        f"\nRetrying lesson generation. "
        f"Retry count: {new_retry_count}"
    )

    return {
        "retry_count": new_retry_count
    }
