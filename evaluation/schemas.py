
from typing import List, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    model_validator
)


CHECKPOINT_IDS = [
    "E1", "E2", "E3", "E4", "E5",
    "E6", "E7", "E8", "E9", "E10"
]


class CheckResult(BaseModel):
    """
    Represents the evaluation result
    of one rubric checkpoint.
    """

    model_config = ConfigDict(extra="forbid")

    checkpoint_id: Literal[
        "E1", "E2", "E3", "E4", "E5",
        "E6", "E7", "E8", "E9", "E10"
    ]

    passed: StrictBool

    reason: str = Field(
        min_length=1,
        description=(
            "Exact evidence quote for a failure, "
            "or explanation of what is missing. "
            "For a pass, explain the supporting evidence."
        )
    )

    feedback: str = Field(
        min_length=1,
        description=(
            "Actionable instructions for improving "
            "the lesson if this checkpoint fails."
        )
    )


class EvaluationResult(BaseModel):
    """
    Represents the complete lesson evaluation.
    """

    model_config = ConfigDict(extra="forbid")

    checks: List[CheckResult] = Field(
        min_length=10,
        max_length=10
    )

    overall_feedback: str = Field(
        min_length=1
    )

    @model_validator(mode="after")
    def validate_checkpoints(self):

        received_ids = [
            check.checkpoint_id
            for check in self.checks
        ]

        if len(received_ids) != len(set(received_ids)):
            raise ValueError(
                "Duplicate checkpoint IDs are not allowed."
            )

        if set(received_ids) != set(CHECKPOINT_IDS):
            raise ValueError(
                "All 10 evaluation checkpoints are required."
            )

        return self


def calculate_is_passing(
    evaluation: EvaluationResult
) -> bool:
    """
    Calculate the final verdict using Python.

    The LLM cannot decide the final verdict.
    """

    return all(
        check.passed
        for check in evaluation.checks
    )
