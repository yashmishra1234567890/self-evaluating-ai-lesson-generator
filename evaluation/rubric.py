
"""
Evaluation Rubric

Defines 10 topic-independent checkpoints for
evaluating beginner-friendly educational lessons.
"""


RUBRIC = [

    {
        "checkpoint_id": "E1",
        "checkpoint_name": "Technical Accuracy",

        "description": (
            "Check whether the technical explanations "
            "related to the requested topic are factually correct."
        ),

        "pass_condition": (
            "All important technical explanations are correct. "
            "There are no misleading statements or technically "
            "incorrect claims about the requested topic."
        )
    },

    {
        "checkpoint_id": "E2",
        "checkpoint_name": "Grounding and Factual Support",

        "description": (
            "Check whether important factual claims are "
            "reliable, relevant, and appropriately supported."
        ),

        "pass_condition": (
            "Important factual claims are consistent with "
            "established knowledge and any reference material "
            "provided to the evaluator. Unsupported, fabricated, "
            "or contradictory claims must fail."
        )
    },

    {
        "checkpoint_id": "E3",
        "checkpoint_name": "Simple Language",

        "description": (
            "Check whether the lesson uses language "
            "understandable to a beginner from a "
            "non-English-medium background."
        ),

        "pass_condition": (
            "Sentences are short, vocabulary is simple, "
            "and explanations are easy to understand."
        )
    },

    {
        "checkpoint_id": "E4",
        "checkpoint_name": "Jargon Explanation",

        "description": (
            "Check whether technical terms are explained "
            "when they are introduced."
        ),

        "pass_condition": (
            "Every important technical term is followed "
            "by a simple explanation or relatable analogy."
        )
    },

    {
        "checkpoint_id": "E5",
        "checkpoint_name": "Clear Definition",

        "description": (
            "Check whether the requested topic is clearly "
            "defined and its main purpose is explained."
        ),

        "pass_condition": (
            "The lesson explicitly explains what the requested "
            "topic is and what it does."
        )
    },

    {
        "checkpoint_id": "E6",
        "checkpoint_name": "Problem Explanation",

        "description": (
            "Check whether the lesson explains why the topic "
            "is important and what problem it solves."
        ),

        "pass_condition": (
            "The lesson clearly describes the problem, need, "
            "or use case that makes the requested topic useful."
        )
    },

    {
        "checkpoint_id": "E7",
        "checkpoint_name": "Workflow Explanation",

        "description": (
            "Check whether the lesson explains the main working "
            "process, stages, or components of the requested topic."
        ),

        "pass_condition": (
            "The main process is explained in a logical order. "
            "Important stages or components and their relationships "
            "are clearly described."
        )
    },

    {
        "checkpoint_id": "E8",
        "checkpoint_name": "Practical Example",

        "description": (
            "Check whether the lesson teaches the requested topic "
            "using a relatable practical example."
        ),

        "pass_condition": (
            "At least one relevant example demonstrates how "
            "the requested topic works or is used in a real situation."
        )
    },

    {
        "checkpoint_id": "E9",
        "checkpoint_name": "Teaching Flow",

        "description": (
            "Check whether concepts are presented in a logical "
            "teaching sequence suitable for a beginner."
        ),

        "pass_condition": (
            "The lesson moves logically from introduction and "
            "basic understanding to importance, working process, "
            "and practical application."
        )
    },

    {
        "checkpoint_id": "E10",
        "checkpoint_name": "Completeness",

        "description": (
            "Check whether the lesson covers the essential "
            "information needed by a beginner to understand "
            "the requested topic."
        ),

        "pass_condition": (
            "The lesson covers the definition, purpose, important "
            "concepts, working process, practical example, "
            "advantages, and limitations where applicable."
        )
    }

]


def get_all_checkpoints():
    """
    Return all 10 evaluation checkpoints.
    """

    return RUBRIC.copy()


def get_checkpoint_by_id(checkpoint_id: str):
    """
    Find a checkpoint using its unique ID.
    """

    for checkpoint in RUBRIC:

        if checkpoint["checkpoint_id"] == checkpoint_id:
            return checkpoint

    return None


def get_checkpoint_ids():
    """
    Return all checkpoint IDs.
    """

    return [
        checkpoint["checkpoint_id"]
        for checkpoint in RUBRIC
    ]


def validate_rubric():
    """
    Validate checkpoint count, IDs and required fields.
    """

    if len(RUBRIC) != 10:
        raise ValueError(
            "Rubric must contain exactly 10 checkpoints."
        )

    checkpoint_ids = get_checkpoint_ids()

    if len(checkpoint_ids) != len(set(checkpoint_ids)):
        raise ValueError(
            "Duplicate checkpoint IDs found."
        )

    required_fields = [
        "checkpoint_id",
        "checkpoint_name",
        "description",
        "pass_condition"
    ]

    for checkpoint in RUBRIC:

        for field in required_fields:

            if not checkpoint.get(field):
                raise ValueError(
                    f"Missing {field} in checkpoint "
                    f"{checkpoint.get('checkpoint_id')}"
                )

    return True
