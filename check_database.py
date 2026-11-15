
from database.operations import (
    get_run_history,
    get_evaluation_logs
)

run_id = "1d673aba-4a5e-4850-bce3-089a473a519c"

print("\n--- RUN HISTORY ---")

history = get_run_history(run_id)
print(history)

print("\n--- EVALUATION LOGS ---")

logs = get_evaluation_logs(run_id)

for log in logs:
    print(log)

print("\nTotal evaluation attempts:", len(logs))
