
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

        # Enable controlled retry test
        "simulate_first_failure": True
    }

    print("\nStarting controlled retry test...")
    print("Run ID:", run_id)

    workflow = build_workflow()

    result = workflow.invoke(initial_state)

    print("\n========== RETRY TEST RESULT ==========")

    print("Final status:", result["status"])

    print(
        "Total generations:",
        len(result.get("evaluation_results", []))
    )

    print(
        "Retry count:",
        result.get("retry_count")
    )

    print(
        "Rejection log:",
        result.get("rejection_log")
    )

    print("Run ID:", run_id)

    if result["status"] == "shipped":
        print("\nSUCCESS: Lesson shipped after retry.")

    else:
        print("\nWorkflow finished without shipping the lesson.")


if __name__ == "__main__":
    main()
