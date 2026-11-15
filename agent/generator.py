
from openrouter import OpenRouter

from config import get_settings

from prompts.generator_prompt import (
    get_generator_system_prompt,
    build_generator_user_prompt
)


def generate_lesson(
    topic: str,
    target_audience: str,
    historical_guidance: list = None,
    rejection_log: list = None,
    previous_draft: str = None
) -> str:
    """
    Generate a beginner-friendly lesson using OpenRouter.
    """

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if not target_audience or not target_audience.strip():
        raise ValueError("Target audience cannot be empty.")

    settings = get_settings()

    system_prompt = get_generator_system_prompt()

    user_prompt = build_generator_user_prompt(
        topic=topic,
        target_audience=target_audience,
        historical_guidance=historical_guidance,
        rejection_log=rejection_log,
        previous_draft=previous_draft
    )

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
            ]
        )

    lesson = response.choices[0].message.content

    if not lesson or not lesson.strip():
        raise ValueError("Generator returned an empty lesson.")

    return lesson.strip()
