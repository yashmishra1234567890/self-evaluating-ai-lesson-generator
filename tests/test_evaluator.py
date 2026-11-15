
import json

import pytest

import agent.evaluator as evaluator_module


class FakeOpenRouter:

    response_text = ""

    def __init__(self, api_key):
        self.api_key = api_key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @property
    def chat(self):
        return self

    def send(self, **kwargs):

        return type(
            "Response",
            (),
            {
                "choices": [
                    type(
                        "Choice",
                        (),
                        {
                            "message": type(
                                "Message",
                                (),
                                {
                                    "content": self.response_text
                                }
                            )()
                        }
                    )()
                ]
            }
        )()


def create_evaluator_response(failed_checkpoint=None):

    checks = []

    for number in range(1, 11):

        checkpoint_id = "E" + str(number)

        passed = checkpoint_id != failed_checkpoint

        checks.append({
            "checkpoint_id": checkpoint_id,
            "passed": passed,
            "reason": "Evidence checked.",
            "feedback": "Improve the explanation if needed."
        })

    return json.dumps({
        "checks": checks,
        "overall_feedback": "Evaluation completed."
    })


def setup_mock(monkeypatch, response_text):

    monkeypatch.setenv(
        "OPENROUTER_API_KEY",
        "test-api-key"
    )

    monkeypatch.setenv(
        "OPENROUTER_MODEL",
        "test-model"
    )

    FakeOpenRouter.response_text = response_text

    monkeypatch.setattr(
        evaluator_module,
        "OpenRouter",
        FakeOpenRouter
    )


def test_all_checkpoints_pass(monkeypatch):

    setup_mock(
        monkeypatch,
        create_evaluator_response()
    )

    result = evaluator_module.evaluate_lesson(
        "Introduction to RAG",
        "RAG retrieves relevant information before generation."
    )

    assert result["is_passing"] is True
    assert len(result["passed_checkpoint_ids"]) == 10
    assert len(result["failed_checkpoint_ids"]) == 0


def test_one_checkpoint_fails(monkeypatch):

    setup_mock(
        monkeypatch,
        create_evaluator_response("E4")
    )

    result = evaluator_module.evaluate_lesson(
        "Introduction to RAG",
        "RAG uses embeddings."
    )

    assert result["is_passing"] is False
    assert result["failed_checkpoint_ids"] == ["E4"]


def test_invalid_json(monkeypatch):

    setup_mock(
        monkeypatch,
        "This is not valid JSON."
    )

    with pytest.raises(ValueError):

        evaluator_module.evaluate_lesson(
            "Introduction to RAG",
            "Sample lesson"
        )


def test_empty_lesson():

    with pytest.raises(ValueError):

        evaluator_module.evaluate_lesson(
            "Introduction to RAG",
            ""
        )


if __name__ == "__main__":

    print("Evaluator tests completed.")
