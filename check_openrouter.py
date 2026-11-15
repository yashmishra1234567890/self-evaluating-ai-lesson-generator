
from openrouter import OpenRouter
from config import get_settings

settings = get_settings()

print("Testing OpenRouter model...")
print("Model:", settings.openrouter_model)

with OpenRouter(
    api_key=settings.openrouter_api_key
) as client:

    response = client.chat.send(
        model=settings.openrouter_model,
        messages=[
            {
                "role": "user",
                "content": "Explain RAG in two simple sentences."
            }
        ],
        temperature=0,
        max_tokens=300,
        stream=False
    )

    print("\nRAW RESPONSE:")
    print(repr(response))

    print("\nRESPONSE DATA:")
    if hasattr(response, "model_dump"):
        print(response.model_dump())
    else:
        print(response)

    if response.choices:
        message = response.choices[0].message

        print("\nMESSAGE:")
        print(repr(message))

        print("\nCONTENT:")
        print(repr(message.content))

        print("\nFINISH REASON:")
        print(response.choices[0].finish_reason)
