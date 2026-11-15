
from database.operations import (
    get_run_history,
    get_evaluation_logs,
    get_rejection_log
)


def main():

    run_id = "36650800-a478-409a-9ef0-a2309580ac73"

    print("\nChecking rejection persistence...")

    # 1. Retrieve run history
    run = get_run_history(run_id)

    if run is None:
        print("ERROR: Run not found.")
        return

    print("\nRun status:", run["status"])
    print("Total attempts:", run["total_attempts"])

    # 2. Retrieve evaluation logs
    evaluation_logs = get_evaluation_logs(run_id)

    print("\nEvaluation logs found:", len(evaluation_logs))

    # 3. Reconstruct rejection history
    rejection_log = get_rejection_log(run_id)

    print("\nPersisted rejection log:")

    for item in rejection_log:
        print(item)

    # 4. Verify expected result
    if (
        run["status"] == "rejected"
        and len(evaluation_logs) == 3
        and len(rejection_log) == 3
    ):
        print("\nSUCCESS: Rejection history persisted in SQLite.")

    else:
        print("\nFAILED: Persistence verification unsuccessful.")


if __name__ == "__main__":
    main()
