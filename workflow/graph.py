
"""
LangGraph Workflow

Handles lesson generation, evaluation,
retry, shipping, rejection, and system errors.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy

from workflow.state import LessonState

from workflow.nodes import (
    load_memory_node,
    generate_lesson_node,
    evaluate_lesson_node,
    increment_retry_node
)

from database.operations import (
    save_final_lesson,
    update_run_status
)


def ship_lesson_node(state: LessonState) -> dict:
    """
    Save the approved lesson and mark the run as shipped.
    """

    save_final_lesson(
        run_id=state["run_id"],
        lesson=state["current_draft"]
    )

    return {
        "final_output": state["current_draft"],
        "status": "shipped"
    }


def reject_lesson_node(state: LessonState) -> dict:
    """
    Mark the run as rejected after all attempts fail.
    """

    update_run_status(
        run_id=state["run_id"],
        status="rejected"
    )

    return {
        "status": "rejected",
        "final_output": ""
    }


def system_error_node(state: LessonState) -> dict:
    """
    Mark the run as a system error.

    System errors are not treated as lesson rejections.
    """

    error_message = state.get(
        "system_error",
        "Unknown system error."
    )

    error_stage = state.get(
        "system_error_stage",
        "unknown"
    )

    print("\n========== SYSTEM ERROR ==========")
    print("Stage:", error_stage)
    print("Error:", error_message)

    update_run_status(
        run_id=state["run_id"],
        status="system_error"
    )

    return {
        "status": "system_error",
        "final_output": ""
    }


def route_after_generation(state: LessonState) -> str:
    """
    Route to evaluation or system-error handling.
    """

    if state.get("system_error"):
        return "system_error"

    return "evaluate"


def route_after_evaluation(state: LessonState) -> str:
    """
    Decide whether to ship, retry, reject, or stop on system error.
    """

    if state.get("system_error"):
        return "system_error"

    if state["is_passing"]:
        return "ship"

    if state.get("retry_count", 0) < 2:
        return "retry"

    return "reject"


def build_workflow():
    """
    Build and compile the complete LangGraph workflow.
    """

    graph = StateGraph(LessonState)

    # Register nodes
    graph.add_node("load_memory", load_memory_node)

    # Disable automatic retries.
    # Our workflow handles lesson retries manually.
    graph.add_node(
        "generate",
        generate_lesson_node,
        retry_policy=RetryPolicy(max_attempts=1)
    )

    graph.add_node(
        "evaluate",
        evaluate_lesson_node,
        retry_policy=RetryPolicy(max_attempts=1)
    )

    graph.add_node("increment_retry", increment_retry_node)
    graph.add_node("ship", ship_lesson_node)
    graph.add_node("reject", reject_lesson_node)
    graph.add_node("system_error", system_error_node)

    # Initial flow
    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "generate")

    # Check generation result
    graph.add_conditional_edges(
        "generate",
        route_after_generation,
        {
            "evaluate": "evaluate",
            "system_error": "system_error"
        }
    )

    # Check evaluation result
    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "ship": "ship",
            "retry": "increment_retry",
            "reject": "reject",
            "system_error": "system_error"
        }
    )

    # Retry loop
    graph.add_edge("increment_retry", "generate")

    # Terminal nodes
    graph.add_edge("ship", END)
    graph.add_edge("reject", END)
    graph.add_edge("system_error", END)

    return graph.compile()
