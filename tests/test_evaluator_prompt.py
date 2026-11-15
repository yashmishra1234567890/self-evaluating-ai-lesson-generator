
from prompts.evaluator_prompt import (
    get_evaluator_system_prompt,
    build_evaluator_user_prompt
)


def test_system_prompt():

    prompt = get_evaluator_system_prompt()

    assert "E1. TECHNICAL ACCURACY" in prompt
    assert "E10. COMPLETENESS" in prompt
    assert "exactly 10" in prompt.lower()
    assert "hallucinations" in prompt.lower()


def test_basic_evaluation_prompt():

    prompt = build_evaluator_user_prompt(
        topic="Introduction to RAG",
        lesson_content="RAG retrieves information before generation."
    )

    assert "Introduction to RAG" in prompt
    assert "RAG retrieves information" in prompt


def test_empty_topic():

    try:
        build_evaluator_user_prompt(
            topic="",
            lesson_content="Sample lesson"
        )

        assert False, "Empty topic was accepted."

    except ValueError:
        pass


def test_empty_lesson():

    try:
        build_evaluator_user_prompt(
            topic="Introduction to RAG",
            lesson_content=""
        )

        assert False, "Empty lesson was accepted."

    except ValueError:
        pass


if __name__ == "__main__":

    test_system_prompt()
    test_basic_evaluation_prompt()
    test_empty_topic()
    test_empty_lesson()

    print("All evaluator prompt tests passed!")
