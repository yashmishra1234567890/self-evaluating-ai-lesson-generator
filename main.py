
from workflow.graph import build_workflow

from database.operations import create_run


def main():
    topic = "Introduction to RAG"

    target_audience = (
        "A 12th-grade Indian student with limited English "
        "vocabulary, from a non-English-medium background, "
        "with no prior knowledge of Artificial Intelligence."
    )

    # Create a new database run
    run_id = create_run(topic)

    print("\nStarting Lesson Generation System...")
    print("Run ID:", run_id)
    print("Topic:", topic)

    # Initial workflow state
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
        "status": "running"
    }

    # Build and execute workflow
    workflow = build_workflow()

    result = workflow.invoke(initial_state)

    print("\n" + "=" * 50)
    print("WORKFLOW COMPLETED")
    print("=" * 50)

    print("Run ID:", run_id)
    print("Final Status:", result["status"])

    print(
        "Total Generations:",
        len(result.get("evaluation_results", []))
    )

    if result["status"] == "shipped":

        print("\nLesson approved and shipped!")
        print("\nFINAL LESSON:\n")

        print(result["final_output"])

    else:

        print("\nLesson rejected after maximum attempts.")

        print("\nREJECTION LOG:")

        for entry in result.get("rejection_log", []):
            print(entry)


if __name__ == "__main__":
    main()
