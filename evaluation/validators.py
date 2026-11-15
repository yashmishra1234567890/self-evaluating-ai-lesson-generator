
from evaluation.schemas import (
    EvaluationResult,
    calculate_is_passing
)


def validate_evaluation(
    evaluation: EvaluationResult
) -> bool:
    """
    Verify that the evaluation contains
    all valid checkpoints.
    """

    if not isinstance(evaluation, EvaluationResult):
        raise TypeError(
            "Expected an EvaluationResult object."
        )

    return len(evaluation.checks) == 10


def get_failed_checkpoints(
    evaluation: EvaluationResult
) -> list:
    """
    Return IDs of all failed checkpoints.
    """

    return [
        check.checkpoint_id
        for check in evaluation.checks
        if not check.passed
    ]


def get_passed_checkpoints(
    evaluation: EvaluationResult
) -> list:
    """
    Return IDs of all passed checkpoints.
    """

    return [
        check.checkpoint_id
        for check in evaluation.checks
        if check.passed
    ]


def get_evaluation_summary(
    evaluation: EvaluationResult
) -> dict:
    """
    Generate a summary of the evaluation.
    """

    passed = get_passed_checkpoints(evaluation)
    failed = get_failed_checkpoints(evaluation)

    return {
        "total_checkpoints": len(evaluation.checks),
        "passed_count": len(passed),
        "failed_count": len(failed),
        "passed_checkpoint_ids": passed,
        "failed_checkpoint_ids": failed,
        "is_passing": calculate_is_passing(evaluation)
    }


def is_lesson_approved(
    evaluation: EvaluationResult
) -> bool:
    """
    Decide whether the lesson can be shipped.

    Every checkpoint must pass.
    """

    validate_evaluation(evaluation)

    return calculate_is_passing(evaluation)
