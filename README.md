# Self-Evaluating GenAI Lesson Generator

An AI-powered lesson generation system that creates beginner-friendly educational content, evaluates its own output against a structured quality rubric, and automatically retries generation when the lesson does not meet the required standards.

The system uses LangGraph to orchestrate the workflow, OpenRouter to access the language model, Pydantic for structured validation, and SQLite to persist evaluation history and learning memory.

**Repository:** [self-evaluating-ai-lesson-generator](https://github.com/yashmishra1234567890/self-evaluating-ai-lesson-generator)

---

## 1. Problem Statement

Generating educational content with an LLM does not guarantee that the content is accurate, understandable, complete, or appropriate for its intended audience.

This project addresses that problem by introducing an evaluation-driven generation workflow.

Instead of accepting the first generated lesson, the system:

1. Generates a lesson for the requested topic and audience.
2. Evaluates the lesson against 10 quality checkpoints.
3. Identifies failed checkpoints and provides feedback.
4. Regenerates the lesson using evaluation feedback.
5. Repeats evaluation until the lesson passes or the retry limit is reached.
6. Ships approved lessons or rejects unsuccessful ones.
7. Stores evaluation history and recurring failure patterns in SQLite.

## 2. Key Features

- **Topic-independent generation:** Generate lessons on different topics rather than relying on a fixed subject.
- **Structured evaluation:** Evaluate every lesson against 10 binary quality checkpoints.
- **Automatic retry mechanism:** Allow up to 2 retries after the initial generation.
- **Maximum generation limit:** A maximum of 3 generation attempts per run.
- **Feedback-driven improvement:** Pass evaluation feedback and historical guidance into subsequent generation attempts.
- **Persistent learning memory:** Store recurring checkpoint failures and historical guidance in SQLite.
- **Rejection logging:** Preserve evaluation results for unsuccessful attempts.
- **System-error handling:** Handle generation and evaluation failures separately.
- **Structured validation:** Validate evaluator responses using Pydantic schemas.
- **Interactive interface:** Run the workflow through a Streamlit application.

## 3. System Architecture

```text
                  User Input
                      |
                      v
               Load Learning Memory
                      |
                      v
                Lesson Generator
                      |
                      v
               Generated Lesson
                      |
                      v
               Lesson Evaluator
                      |
                      v
              Validate Evaluation
                      |
                      v
                Check Result
                      |
          +-----------+-----------+
          |           |           |
        PASS        FAIL       ERROR
          |           |           |
          v           v           v
        SHIP       Retry /      System
                   Reject       Error
                      |
                      v
             Update Learning Memory
                      |
                      v
               Generate Again
```

The workflow is implemented using LangGraph.

## 4. Evaluation Rubric

Each lesson is evaluated using 10 binary checkpoints.

A checkpoint receives either PASS or FAIL.

| ID | Evaluation Checkpoint | What It Evaluates |
|---|---|---|
| E1 | Technical Accuracy | Correctness of technical information |
| E2 | Grounding and Factual Support | Factual support and avoidance of unsupported claims |
| E3 | Simple Language | Appropriate language for beginners |
| E4 | Jargon Explanation | Explanation of technical terminology |
| E5 | Clear Definition | Clarity of key concepts and definitions |
| E6 | Problem Explanation | Explanation of the problem being addressed |
| E7 | Workflow Explanation | Logical explanation of processes and steps |
| E8 | Practical Example | Relevant examples that support learning |
| E9 | Teaching Flow | Logical progression of concepts |
| E10 | Completeness | Coverage of essential lesson content |

**Passing condition:** All 10 checkpoints must pass.

A lesson that fails even one checkpoint is sent through the retry or rejection path.

## 5. Retry and Rejection Logic

The system supports a maximum of 3 generation attempts.

| Attempt | Result | System Action |
|---|---|---|
| 1 | All checkpoints pass | Ship lesson |
| 1 | One or more checkpoints fail | Retry |
| 2 | All checkpoints pass | Ship lesson |
| 2 | One or more checkpoints fail | Final retry |
| 3 | All checkpoints pass | Ship lesson |
| 3 | One or more checkpoints fail | Reject lesson |

The system also handles generation and evaluation errors through a separate system-error path.

Rejected runs preserve their evaluation history for inspection.

## 6. Learning Memory

The project includes a persistent learning-memory mechanism backed by SQLite.

It stores recurring checkpoint failures and associated guidance.

During subsequent runs:

1. Historical failure patterns are retrieved.
2. Relevant guidance is passed to the generator.
3. The generator uses that guidance while creating the lesson.
4. New evaluation failures update the stored patterns.

This allows the system to use previous evaluation outcomes as guidance for future lesson generation.

## 7. Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM API | OpenRouter |
| Model | NVIDIA Nemotron |
| Workflow Orchestration | LangGraph |
| Data Validation | Pydantic |
| Frontend | Streamlit |
| Database | SQLite |
| Configuration | Python-dotenv, Pydantic Settings |
| Testing | Pytest |

## 8. Project Structure

```text
lessongenerator/
│
├── agent/
│   ├── evaluator.py
│   └── generator.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── operations.py
│   └── schema.py
│
├── evaluation/
│   ├── rubric.py
│   ├── schemas.py
│   └── validators.py
│
├── prompts/
│   ├── evaluator_prompt.py
│   └── generator_prompt.py
│
├── workflow/
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_connection.py
│   ├── test_database.py
│   ├── test_evaluator.py
│   ├── test_evaluator_prompt.py
│   ├── test_generator.py
│   ├── test_generator_prompt.py
│   └── test_workflow.py
│
├── outputs/
│   ├── agentic_ai_lesson.txt
│   ├── rag_lesson.txt
│   ├── final_lesson.md
│   ├── rejection_log.json
│   └── test_evidence/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── check_connection.py
├── check_database.py
├── check_evaluator_system_error.py
├── check_graph.py
├── check_openrouter.py
├── check_operations.py
├── check_rejection.py
├── check_rejection_persistence.py
├── check_retry.py
├── check_schema.py
├── check_state.py
├── check_system_error.py
├── test_evel_schemas.py
├── test_rubric.py
├── test_validators.py
└── README.md
```

## 9. Installation and Setup

### Prerequisites

- Python 3.10 or later
- An OpenRouter API key
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/yashmishra1234567890/self-evaluating-ai-lesson-generator.git

cd self-evaluating-ai-lesson-generator
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root using `.env.example` as the template.

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=nvidia/nemotron-3.5-super-vl:free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Replace the placeholder with your own OpenRouter API key.

Never commit your real API key to GitHub.

## 10. Running the Application

Start the Streamlit interface:

```bash
streamlit run app.py
```

The interface allows users to enter a lesson topic and target audience and execute the generation and evaluation workflow.

The project also includes a command-line entry point:

```bash
python main.py
```

## 11. Testing

The project uses Pytest for automated testing.

Run the test suite:

```bash
pytest -q
```

**Latest verified test result:**

```text
...........................                  [100%]
27 passed in 0.65s
```

Dependency compatibility was also checked:

```text
pip check

No broken requirements found.
```

### Workflow Validation

The project includes validation scripts for:

- Successful lesson generation
- Evaluation and retry behavior
- Maximum retry limit
- Rejection after repeated failures
- Generator system errors
- Evaluator system errors
- Database persistence
- Evaluation schema validation

Test evidence is available in `outputs/test_evidence/`.

## 12. Example Outputs

The repository includes generated lesson examples:

- `outputs/rag_lesson.txt` — Introduction to RAG
- `outputs/agentic_ai_lesson.txt` — Introduction to Agentic AI
- `outputs/final_lesson.md` — Final lesson output
- `outputs/rejection_log.json` — Rejection information

## 13. Future Improvements

- Add more detailed evaluation metrics.
- Introduce topic-specific evaluation criteria.
- Improve learning-memory retrieval.
- Add evaluation analytics and run-history visualization.
- Expand automated testing with additional edge cases.

---

Built as a project demonstrating self-evaluating GenAI workflows, structured quality evaluation, retry orchestration, and persistent learning memory.