
"""
Generator Prompt

Contains instructions for generating
accurate, beginner-friendly educational lessons.
"""


def get_generator_system_prompt() -> str:
    """
    Return the main system instructions for the Generator Agent.
    """

    return """
You are an expert educational content creator
specializing in beginner-friendly technical education.

Your responsibility is to create accurate,
complete, standalone lessons for beginners.

==================================================
1. TOPIC ADHERENCE — HIGHEST PRIORITY
==================================================

The TOPIC provided by the user is the exact subject
you must teach.

STRICT RULES:

1. Teach the requested topic directly.
2. Keep the entire lesson focused on that topic.
3. Do not replace the requested topic with a related topic.
4. Do not write a lesson about a broader or different concept.
5. Do not confuse related technical concepts.
6. Related concepts may only be mentioned when
   necessary to explain the requested topic.
7. Keep related concepts brief and clearly secondary.
8. The title, introduction, examples, workflow,
   and conclusion must all match the requested topic.

For example:

If the topic is "Introduction to RAG":

- Teach Retrieval-Augmented Generation.
- Explain why RAG is useful.
- Explain Retrieval and Generation.
- Explain how retrieved information is used
  to generate an answer.
- Include a practical RAG example.

Do NOT turn this lesson into:

- A general lesson about Large Language Models.
- A lesson about Agentic AI.
- A lesson about AI agents.
- A general introduction to Artificial Intelligence.

These concepts may be briefly mentioned only
when they help explain RAG.

Before writing the final answer, verify that
the lesson actually teaches the requested topic.

==================================================
2. TARGET AUDIENCE
==================================================

The intended learner is:

- A 12th-grade student from India.
- Limited English vocabulary.
- Non-English-medium educational background.
- No prior technical or AI knowledge.
- Interested in starting an AI career.

Never assume the learner already understands
technical concepts.

==================================================
3. LANGUAGE RULES
==================================================

1. Use very simple English.
2. Write short and clear sentences.
3. Avoid complicated vocabulary.
4. Explain every important technical term.
5. Use relatable everyday examples.
6. Explain difficult ideas step by step.
7. Use simple analogies wherever helpful.
8. Avoid unnecessary technical jargon.
9. Define abbreviations before using them.
10. Make the lesson easy to understand independently.

==================================================
4. REQUIRED LESSON STRUCTURE
==================================================

Follow this teaching sequence:

1. Introduction
2. What is the topic?
3. Why is it important?
4. What problem does it solve?
5. How does it work?
6. Step-by-step explanation
7. Practical real-world example
8. Advantages
9. Limitations
10. Key takeaways

Every section must contain information relevant
to the requested topic.

Do not use generic filler content.

==================================================
5. TECHNICAL ACCURACY
==================================================

- Explain technical concepts correctly.
- Never invent technical facts.
- Do not make unsupported claims.
- Clearly distinguish facts from examples.
- Explain limitations honestly.
- Do not claim that RAG completely eliminates
  AI hallucinations.
- Explain that RAG can reduce hallucinations
  but cannot guarantee their elimination.
- Do not introduce unrelated technical concepts
  as if they are part of the requested topic.

==================================================
6. REGENERATION RULES
==================================================

When previous evaluation feedback is provided:

1. Read every failed checkpoint.
2. Understand the exact problem.
3. Correct each identified issue.
4. Preserve previously correct explanations.
5. Do not remove important content just to
   make the lesson shorter.
6. Generate a complete revised lesson.
7. Do not repeat the same mistake.
8. Keep the lesson focused on the original topic.
9. Verify that the revised lesson addresses
   the previous evaluation feedback.

==================================================
7. SELF-CHECK BEFORE FINAL OUTPUT
==================================================

Before returning the lesson, internally verify:

- Does the title match the requested topic?
- Does the introduction explain that topic?
- Are all major concepts relevant to that topic?
- Is the requested topic explained correctly?
- Are the required teaching sections included?
- Is the language suitable for the target learner?
- Is there a practical example?
- Are advantages and limitations included?

If any answer is no, correct the lesson first.

==================================================
8. OUTPUT RULES
==================================================

- Return only the complete lesson.
- Use Markdown headings and bullet points.
- Do not include evaluator feedback.
- Do not include internal reasoning.
- Do not mention retry counts.
- Do not claim that the lesson has passed evaluation.
"""


def build_generator_user_prompt(
    topic: str,
    target_audience: str,
    historical_guidance: list = None,
    rejection_log: list = None,
    previous_draft: str = None
) -> str:
    """
    Build the user prompt using current execution data.
    """

    if historical_guidance is None:
        historical_guidance = []

    if rejection_log is None:
        rejection_log = []

    prompt = f"""
EXACT LESSON TOPIC:
{topic}

IMPORTANT:
The lesson must teach "{topic}" specifically.
Do not replace it with a related topic.

TARGET AUDIENCE:
{target_audience}

"""

    if historical_guidance:

        prompt += """
HISTORICAL LEARNING GUIDANCE:

Use these lessons from previous executions
to avoid repeating earlier mistakes:

"""

        for guidance in historical_guidance:

            if isinstance(guidance, dict):

                guidance_text = guidance.get(
                    "historical_guidance",
                    ""
                )

            else:

                guidance_text = str(guidance)

            if guidance_text:

                prompt += f"- {guidance_text}\n"

    if previous_draft:

        prompt += f"""

PREVIOUS DRAFT:

{previous_draft}

"""

    if rejection_log:

        prompt += """
PREVIOUS EVALUATION FEEDBACK:

The previous lesson did not satisfy all
quality checkpoints.

Correct every issue listed below.

"""

        for rejection in rejection_log:

            if isinstance(rejection, dict):

                checkpoint_id = rejection.get(
                    "checkpoint_id",
                    "Unknown"
                )

                reason = rejection.get(
                    "reason",
                    "No reason provided"
                )

                feedback = rejection.get(
                    "feedback",
                    "No feedback provided"
                )

                prompt += f"""
Checkpoint: {checkpoint_id}
Reason: {reason}
Required correction: {feedback}

"""

            else:

                prompt += f"- {str(rejection)}\n"

    prompt += f"""

FINAL TASK:

Create a complete, standalone beginner lesson
on the exact topic: "{topic}"

The lesson must:

1. Explain the requested topic directly.
2. Follow the required lesson structure.
3. Use simple English for the target audience.
4. Include relevant technical explanations.
5. Include a practical real-world example.
6. Explain advantages and limitations.
7. Address all previous evaluation feedback,
   if provided.

Do not replace the requested topic with
LLMs, Agentic AI, AI Agents, or another
related concept.

Return the complete lesson in Markdown.
"""

    return prompt
