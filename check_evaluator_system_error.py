
"""
Controlled Evaluator System Error Test

Tests whether the workflow handles evaluator failures
without crashing or treating them as lesson rejections.
"""

import workflow.nodes as workflow_nodes

from workflow.graph import build_workflow

from database.operations import (
    create_run,
    get_run_history
)


def simulate_generator_success(*args, **kwargs):
    """
    Return dummy lesson content.
    No real OpenRouter API call.
    """

    return """
    # Introduction to RAG

    RAG stands for Retrieval-Augmented Generation.
    It helps AI systems answer questions using information
    retrieved from external documents.
    """


def simulate_evaluator_error(*args, **kwargs):
    """
    Simulate an evaluator API failure.
    """

    raise RuntimeError(
        "Controlled test: Evaluator API unavailable."
    )


def main():

    topic = "Introduction to RAG"

    run_id = create_run(topic)

    print("\nStarting controlled evaluator system-error test...")
    print("Run ID:", run_id)

    # Replace real agent functions with controlled test functions.
    workflow_nodes.generate_lesson = simulate_generator_success
    workflow_nodes.evaluate_lesson = simulate_evaluator_error

    initial_state = {
        "run_id": run_id,
        "topic": topic,
        "target_audience": (
            "A 12th-grade Indian learner with limited English "
            "vocabulary and no prior AI knowledge."
        ),
        "current_draft": "",
        "retry_count": 0,
        "historical_guidance": [],
        "evaluation_results": [],
        "rejection_log": [],
        "is_passing": False,
        "final_output": "",
        "status": "running"
    }

    workflow = build_workflow()

    result = workflow.invoke(initial_state)

    run_history = get_run_history(run_id)

    print("\n========== EVALUATOR SYSTEM ERROR TEST RESULT ==========")

    print("Workflow status:", result.get("status"))
    print("Database status:", run_history["status"])
    print("System error:", result.get("system_error"))
    print("Error stage:", result.get("system_error_stage"))
    print("Retry count:", result.get("retry_count"))
    print("Rejection log:", result.get("rejection_log"))

    if (
        result.get("status") == "system_error"
        and run_history["status"] == "system_error"
        and result.get("system_error_stage") == "evaluation"
        and result.get("retry_count") == 0
        and not result.get("rejection_log")
    ):

        print("\nSUCCESS: Evaluator system error handled correctly.")

    else:

        print("\nFAILED: Evaluator system error test did not pass.")


if __name__ == "__main__":
    main()
