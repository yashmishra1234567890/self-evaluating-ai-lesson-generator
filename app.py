
"""
LessonForge - Streamlit Frontend
Self-Evaluating GenAI Lesson Content Generator
"""

import streamlit as st

from workflow.graph import build_workflow

from database.operations import (
    create_run,
    get_run_history,
    get_evaluation_logs
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="LessonForge | GenAI Content System",
    page_icon="🎓",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 750;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .status-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 12px;
    }

    .small-label {
        color: #888888;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if "run_id" not in st.session_state:
    st.session_state.run_id = None


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.title("🎓 LessonForge")

    st.caption("Self-Evaluating GenAI Content System")

    st.divider()

    st.subheader("About")

    st.write(
        """
        LessonForge generates beginner-friendly
        educational lessons and evaluates them
        using a 10-point quality rubric.
        """
    )

    st.divider()

    st.subheader("Workflow")

    st.markdown(
        """
        1. Generate lesson
        2. Evaluate quality
        3. Regenerate if required
        4. Ship or reject
        """
    )

    st.divider()

    st.caption("Powered by LangGraph, OpenRouter and SQLite")


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">Create Your Learning Lesson</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate, evaluate and improve educational content automatically.'
    '</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------

st.subheader("Lesson Configuration")

col1, col2 = st.columns(2)

with col1:

    topic = st.text_input(
        "Lesson Topic",
        value="Introduction to RAG",
        help="Enter the topic for which you want to generate a lesson."
    )

with col2:

    max_retries = st.selectbox(
        "Maximum Retries",
        options=[0, 1, 2],
        index=2,
        help="Maximum number of regeneration attempts after evaluation failure."
    )


target_audience = st.text_area(
    "Target Audience",
    value=(
        "A 12th-grade Indian student with limited English "
        "vocabulary, from a non-English-medium background, "
        "with no prior knowledge of Artificial Intelligence."
    ),
    height=110
)


st.divider()


# -------------------------------------------------
# GENERATION FUNCTION
# -------------------------------------------------

def run_lesson_workflow(topic, target_audience, max_retries):

    run_id = create_run(topic)

    initial_state = {
        "run_id": run_id,
        "topic": topic,
        "target_audience": target_audience,
        "current_draft": "",
        "retry_count": 0,
        "historical_guidance": [],
        "evaluation_results": [],
        "rejection_log": [],
        "is_passing": False,
        "final_output": "",
        "status": "running"
    }

    workflow = build_workflow()

    result = workflow.invoke(
        initial_state,
        config={
            "recursion_limit": 50
        }
    )

    return run_id, result


# -------------------------------------------------
# GENERATE BUTTON
# -------------------------------------------------

generate_button = st.button(
    "🚀 Generate & Evaluate Lesson",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not topic.strip():

        st.error("Please enter a lesson topic.")

    elif not target_audience.strip():

        st.error("Please enter the target audience.")

    else:

        try:

            with st.spinner(
                "Generating and evaluating your lesson..."
            ):

                run_id, result = run_lesson_workflow(
                    topic,
                    target_audience,
                    max_retries
                )

                st.session_state.run_id = run_id
                st.session_state.workflow_result = result

        except Exception as error:

            st.error(
                f"Workflow execution failed: {str(error)}"
            )

            st.stop()


# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------

result = st.session_state.workflow_result
run_id = st.session_state.run_id


if result:

    st.divider()

    st.header("Workflow Results")

    col1, col2, col3 = st.columns(3)

    status = result.get("status", "unknown")

    with col1:
        st.metric(
            "Workflow Status",
            status.upper()
        )

    with col2:
        st.metric(
            "Total Generations",
            len(result.get("evaluation_results", []))
        )

    with col3:
        st.metric(
            "Retries Used",
            result.get("retry_count", 0)
        )

    st.caption(f"Run ID: {run_id}")

    # ---------------------------------------------
    # SHIPPED RESULT
    # ---------------------------------------------

    if status == "shipped":

        st.success(
            "Lesson successfully evaluated and approved!"
        )

        st.subheader("Final Lesson")

        final_output = result.get("final_output", "")

        st.markdown(final_output)

        st.download_button(
            label="📥 Download Final Lesson",
            data=final_output,
            file_name="introduction_to_rag.md",
            mime="text/markdown",
            use_container_width=True
        )

    # ---------------------------------------------
    # REJECTED RESULT
    # ---------------------------------------------

    elif status == "rejected":

        st.error(
            "Lesson rejected after maximum generation attempts."
        )

        st.subheader("Rejection History")

        rejection_log = result.get("rejection_log", [])

        for entry in rejection_log:

            with st.expander(
                f"Attempt {entry.get('attempt', '?')} - Failed"
            ):

                st.write(
                    "Failed checkpoints:",
                    entry.get("failed_checkpoint_ids", [])
                )

                st.write(
                    "Feedback:",
                    entry.get("feedback", "")
                )

    # ---------------------------------------------
    # SYSTEM ERROR
    # ---------------------------------------------

    elif status == "system_error":

        st.error("A system error interrupted the workflow.")

        st.write(
            "Error stage:",
            result.get("system_error_stage", "Unknown")
        )

        st.code(
            result.get("system_error", "Unknown system error.")
        )

    # ---------------------------------------------
    # EVALUATION DASHBOARD
    # ---------------------------------------------

    evaluation_results = result.get(
        "evaluation_results",
        []
    )

    if evaluation_results:

        st.divider()

        st.header("Evaluation Dashboard")

        latest_evaluation = evaluation_results[-1]

        checks = latest_evaluation.get("checks", [])

        passed_count = sum(
            1 for check in checks if check.get("passed") is True
        )

        failed_count = len(checks) - passed_count

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Passed Checkpoints", passed_count)

        with col2:
            st.metric("Failed Checkpoints", failed_count)

        if checks:

            for check in checks:

                checkpoint_id = check.get(
                    "checkpoint_id",
                    "Unknown"
                )

                checkpoint_name = check.get(
                    "checkpoint_name",
                    checkpoint_id
                )

                passed = check.get("passed", False)

                with st.expander(
                    f"{'✅' if passed else '❌'} "
                    f"{checkpoint_id}: {checkpoint_name}"
                ):

                    st.write(
                        "**Result:**",
                        "PASS" if passed else "FAIL"
                    )

                    st.write(
                        "**Reason:**",
                        check.get("reason", "No reason provided.")
                    )

                    st.write(
                        "**Feedback:**",
                        check.get("feedback", "No feedback provided.")
                    )

    # ---------------------------------------------
    # ATTEMPT HISTORY
    # ---------------------------------------------

    if evaluation_results:

        st.divider()

        st.header("Generation History")

        for index, evaluation in enumerate(
            evaluation_results
        ):

            checks = evaluation.get("checks", [])

            passed = sum(
                1 for check in checks
                if check.get("passed") is True
            )

            with st.expander(
                f"Attempt {index + 1} — "
                f"{passed}/10 checkpoints passed"
            ):

                for check in checks:

                    icon = (
                        "✅"
                        if check.get("passed")
                        else "❌"
                    )

                    st.write(
                        f"{icon} {check.get('checkpoint_id')}: "
                        f"{check.get('feedback', '')}"
                    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "LessonForge | Built with Streamlit, LangGraph, "
    "OpenRouter and SQLite"
)
