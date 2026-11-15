
from workflow.state import LessonState

state: LessonState = {
    "run_id": "test-001",
    "topic": "Introduction to RAG",
    "target_audience": "12th-grade Indian learner",
    "current_draft": "",
    "retry_count": 0,
    "historical_guidance": "",
    "evaluation_results": [],
    "rejection_log": [],
    "is_passing": False,
    "final_output": "",
    "status": "running"
}

print("State created successfully!")
print("Topic:", state["topic"])
print("Retry count:", state["retry_count"])
print("Status:", state["status"])
