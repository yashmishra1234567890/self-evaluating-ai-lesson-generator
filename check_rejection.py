
from workflow.graph import build_workflow
from database.operations import create_run


def main():

    topic = "Introduction to RAG"

    target_audience = (
        "A 12th-grade Indian learner with limited English "
        "vocabulary and no prior AI knowledge."
    )

    run_id = create_run(topic)

    initial_state = {
        "run_id": run_id,
        "topic": topic,
        "target_audience": target_audience,
        "current_draft": "",
        "retry_count": 0,
        "historical_guidance": [],
        "evaluation_results": [],
        "rejection_log": [],
        "is_passing": False,
        "final_output": "",
        "status": "running",

        # Force every attempt to fail
        "simulate_all_attempts_failure": True
    }

    print("\nStarting controlled rejection test...")
    print("Run ID:", run_id)

    workflow = build_workflow()
    result = workflow.invoke(initial_state)

    total_generations = len(
        result.get("evaluation_results", [])
    )

    print("\n========== REJECTION TEST RESULT ==========")
    print("Final status:", result["status"])
    print("Total generations:", total_generations)
    print("Retry count:", result.get("retry_count"))
    print("Rejection log:", result.get("rejection_log"))
    print("Run ID:", run_id)

    if (
        result["status"] == "rejected"
        and total_generations == 3
        and result.get("retry_count") == 2
    ):
        print("\nSUCCESS: Maximum retry limit verified.")

    else:
        print("\nTEST FAILED: Unexpected workflow result.")


if __name__ == "__main__":
    main()
