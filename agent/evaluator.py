
"""
Evaluator Agent

Evaluates generated lessons using OpenRouter
and validates the response using Pydantic.
"""

from openrouter import OpenRouter
from pydantic import ValidationError

from config import get_settings

from prompts.evaluator_prompt import (
    get_evaluator_system_prompt,
    build_evaluator_user_prompt
)

from evaluation.schemas import (
    EvaluationResult,
    calculate_is_passing
)

from evaluation.validators import (
    get_failed_checkpoints,
    get_passed_checkpoints,
    get_evaluation_summary
)


def evaluate_lesson(
    topic: str,
    lesson_content: str
) -> dict:
    """
    Evaluate a generated lesson.

    Returns validated evaluation results.
    Python independently calculates the final verdict.
    """

    # 1. Validate inputs
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if not lesson_content or not lesson_content.strip():
        raise ValueError("Lesson content cannot be empty.")

    # 2. Load settings
    settings = get_settings()

    # 3. Build prompts
    system_prompt = get_evaluator_system_prompt()

    user_prompt = build_evaluator_user_prompt(
        topic=topic,
        lesson_content=lesson_content
    )

    # 4. Call OpenRouter
    with OpenRouter(
        api_key=settings.openrouter_api_key
    ) as client:

        response = client.chat.send(
            model=settings.openrouter_model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0,
            max_tokens=8000,

            reasoning={
                "effort": "low",
                "exclude": True
            },

            stream=False
        )

    # 5. Validate response structure
    if not response.choices:
        raise ValueError(
            "Evaluator returned no response choices."
        )

    choice = response.choices[0]
    message = choice.message

    raw_response = message.content

    # 6. Safely read optional response metadata
    finish_reason = getattr(
        choice,
        "finish_reason",
        None
    )

    usage = getattr(
        response,
        "usage",
        None
    )

    print("\n--- EVALUATOR DEBUG ---")
    print("Model:", settings.openrouter_model)
    print("Finish reason:", finish_reason)
    print("Content length:", len(raw_response or ""))
    print("Usage:", usage)

    if raw_response:
        print(
            "Raw response ending:",
            repr(raw_response[-300:])
        )

    print("--- END EVALUATOR DEBUG ---\n")

    # 7. Handle empty response
    if not raw_response or not raw_response.strip():

        raise ValueError(
            "Evaluator returned empty content. "
            f"Finish reason: {finish_reason}. "
            f"Usage: {usage}"
        )

    # 8. Validate JSON using Pydantic
    try:

        evaluation = EvaluationResult.model_validate_json(
            raw_response
        )

    except ValidationError as error:

        if finish_reason == "length":

            raise ValueError(
                "Evaluator response was truncated because "
                "the generation token limit was reached. "
                f"Usage: {usage}"
            ) from error

        raise ValueError(
            "Evaluator returned invalid structured JSON. "
            f"Finish reason: {finish_reason}. "
            f"Response ending: {raw_response[-300:]}"
        ) from error

    # 9. Calculate verdict independently using Python
    is_passing = calculate_is_passing(evaluation)

    # 10. Extract checkpoint results
    passed = get_passed_checkpoints(evaluation)

    failed = get_failed_checkpoints(evaluation)

    summary = get_evaluation_summary(evaluation)

    # 11. Return structured result
    return {
        "evaluation": evaluation,
        "is_passing": is_passing,
        "passed_checkpoint_ids": passed,
        "failed_checkpoint_ids": failed,
        "summary": summary
    }
