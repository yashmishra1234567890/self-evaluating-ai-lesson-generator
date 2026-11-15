
from prompts.generator_prompt import (
    get_generator_system_prompt,
    build_generator_user_prompt
)


def test_system_prompt():

    prompt = get_generator_system_prompt()

    assert "beginner-friendly" in prompt
    assert "Technical Accuracy" in prompt or "TECHNICAL ACCURACY" in prompt
    assert "hallucinations" in prompt


def test_basic_user_prompt():

    prompt = build_generator_user_prompt(
        topic="Introduction to RAG",
        target_audience="12th-grade beginner"
    )

    assert "Introduction to RAG" in prompt
    assert "12th-grade beginner" in prompt


def test_historical_guidance():

    prompt = build_generator_user_prompt(
        topic="Introduction to RAG",
        target_audience="Beginner",
        historical_guidance=[
            {
                "checkpoint_id": "E4",
                "historical_guidance": (
                    "Explain technical jargon using simple examples."
                )
            }
        ]
    )

    assert "HISTORICAL LEARNING GUIDANCE" in prompt
    assert "simple examples" in prompt


def test_retry_feedback():

    prompt = build_generator_user_prompt(
        topic="Introduction to RAG",
        target_audience="Beginner",
        previous_draft="RAG uses embeddings.",
        rejection_log=[
            {
                "checkpoint_id": "E4",
                "reason": "Embedding was not explained.",
                "feedback": "Explain embedding in simple words."
            }
        ]
    )

    assert "PREVIOUS DRAFT" in prompt
    assert "RAG uses embeddings." in prompt
    assert "E4" in prompt
    assert "Explain embedding in simple words." in prompt


if __name__ == "__main__":

    test_system_prompt()
    test_basic_user_prompt()
    test_historical_guidance()
    test_retry_feedback()

    print("All generator prompt tests passed!")
