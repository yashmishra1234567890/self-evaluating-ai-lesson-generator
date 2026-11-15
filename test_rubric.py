
from evaluation.rubric import (
    get_all_checkpoints,
    get_checkpoint_by_id,
    get_checkpoint_ids,
    validate_rubric
)


def test_rubric():

    # Test 1: Validate rubric
    assert validate_rubric() is True

    # Test 2: Check total checkpoints
    checkpoints = get_all_checkpoints()

    assert len(checkpoints) == 10

    # Test 3: Check IDs
    checkpoint_ids = get_checkpoint_ids()

    assert checkpoint_ids == [
        "E1", "E2", "E3", "E4", "E5",
        "E6", "E7", "E8", "E9", "E10"
    ]

    # Test 4: Find checkpoint
    checkpoint = get_checkpoint_by_id("E4")

    assert checkpoint is not None

    assert checkpoint["checkpoint_name"] == (
        "Jargon Explanation"
    )

    # Test 5: Invalid checkpoint
    assert get_checkpoint_by_id("E99") is None

    print("All rubric tests passed!")


if __name__ == "__main__":

    test_rubric()
