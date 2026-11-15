
from evaluation.schemas import (
    CheckResult,
    EvaluationResult
)

from evaluation.validators import (
    validate_evaluation,
    get_failed_checkpoints,
    get_passed_checkpoints,
    get_evaluation_summary,
    is_lesson_approved
)


def create_evaluation():

    checks = []

    for number in range(1, 11):

        checkpoint_id = "E" + str(number)

        passed = True

        if checkpoint_id == "E4":
            passed = False

        checks.append(
            CheckResult(
                checkpoint_id=checkpoint_id,
                passed=passed,
                reason="Checkpoint evidence checked.",
                feedback="Explain technical terms simply."
            )
        )

    return EvaluationResult(
        checks=checks,
        overall_feedback="One checkpoint failed."
    )


def test_validators():

    evaluation = create_evaluation()

    # Test 1
    assert validate_evaluation(evaluation) is True

    # Test 2
    failed = get_failed_checkpoints(evaluation)

    assert failed == ["E4"]

    # Test 3
    passed = get_passed_checkpoints(evaluation)

    assert len(passed) == 9

    # Test 4
    summary = get_evaluation_summary(evaluation)

    assert summary["passed_count"] == 9
    assert summary["failed_count"] == 1
    assert summary["is_passing"] is False

    # Test 5
    assert is_lesson_approved(evaluation) is False

    print("All validator tests passed!")

    print("Evaluation Summary:", summary)


if __name__ == "__main__":

    test_validators()
