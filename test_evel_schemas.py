
from pydantic import ValidationError

from evaluation.schemas import (
    CheckResult,
    EvaluationResult,
    calculate_is_passing
)


def create_checks(passed=True):

    checks = []

    for checkpoint_number in range(1, 11):

        checkpoint_id = "E" + str(checkpoint_number)

        checks.append(
            CheckResult(
                checkpoint_id=checkpoint_id,
                passed=passed,
                reason="Checkpoint evidence verified.",
                feedback="No correction required."
            )
        )

    return checks


def test_all_checkpoints_pass():

    evaluation = EvaluationResult(
        checks=create_checks(True),
        overall_feedback="Lesson meets all requirements."
    )

    assert calculate_is_passing(evaluation) is True


def test_one_checkpoint_fails():

    checks = create_checks(True)

    checks[3] = CheckResult(
        checkpoint_id="E4",
        passed=False,
        reason="Technical term was not explained.",
        feedback="Explain technical terms simply."
    )

    evaluation = EvaluationResult(
        checks=checks,
        overall_feedback="One checkpoint failed."
    )

    assert calculate_is_passing(evaluation) is False


def test_duplicate_checkpoint_rejected():

    checks = create_checks(True)

    checks[1] = checks[0]

    try:
        EvaluationResult(
            checks=checks,
            overall_feedback="Test"
        )
        assert False, "Duplicate checkpoint was accepted."

    except ValidationError:
        pass


def test_missing_checkpoint_rejected():

    checks = create_checks(True)

    checks.pop()

    try:
        EvaluationResult(
            checks=checks,
            overall_feedback="Test"
        )
        assert False, "Missing checkpoint was accepted."

    except ValidationError:
        pass


if __name__ == "__main__":

    test_all_checkpoints_pass()
    test_one_checkpoint_fails()
    test_duplicate_checkpoint_rejected()
    test_missing_checkpoint_rejected()

    print("All Pydantic schema tests passed!")
