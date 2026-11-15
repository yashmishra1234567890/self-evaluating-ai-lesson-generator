
import workflow.nodes as workflow_nodes

from workflow.graph import build_workflow
from database.operations import (
    create_run,
    get_run_history
)


def simulate_generator_error(*args, **kwargs):
    raise RuntimeError(
        "Controlled test: OpenRouter API unavailable."
    )


def main():

    topic = "Introduction to RAG"

    run_id = create_run(topic)

    # Replace generator with a controlled failing function
    workflow_nodes.generate_lesson = simulate_generator_error

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

    print("\nStarting controlled system-error test...")
    print("Run ID:", run_id)

    workflow = build_workflow()

    result = workflow.invoke(initial_state)

    run_history = get_run_history(run_id)

    print("\n========== SYSTEM ERROR TEST RESULT ==========")
    print("Workflow status:", result["status"])
    print("Database status:", run_history["status"])
    print("System error:", result.get("system_error"))
    print("Error stage:", result.get("system_error_stage"))
    print("Retry count:", result.get("retry_count"))
    print("Rejection log:", result.get("rejection_log"))

    if (
        result["status"] == "system_error"
        and run_history["status"] == "system_error"
        and result.get("retry_count") == 0
        and not result.get("rejection_log")
    ):
        print("\nSUCCESS: System error handled correctly.")

    else:
        print("\nTEST FAILED: Unexpected workflow behaviour.")


if __name__ == "__main__":
    main()
