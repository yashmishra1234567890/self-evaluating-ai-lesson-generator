
from typing import Any, TypedDict


class LessonState(TypedDict, total=False):

    # Unique ID for each workflow execution
    run_id: str

    # Input details
    topic: str
    target_audience: str

    # Generator data
    current_draft: str

    # Retry management
    retry_count: int

    # Guidance retrieved from database
    historical_guidance: list[dict[str, Any]]

    # Evaluation data for every attempt
    evaluation_results: list[dict[str, Any]]

    # Failed checkpoints and feedback
    rejection_log: list[dict[str, Any]]

    # Evaluator decision
    is_passing: bool

    # Final lesson
    final_output: str

    # Workflow status
    status: str

    # System error information
    system_error: str
    system_error_stage: str

    # Controlled test flags
    simulate_first_failure: bool
    simulate_all_attempts_failure: bool
