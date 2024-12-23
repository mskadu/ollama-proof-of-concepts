"""Basic script to use the "chat completion" API of Llama 3.12 model via Ollama. 
   See: https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion
"""

from ollama import ChatResponse, chat

LLM_NAME = "llama3.2"  # The LLM to use
CHAT_PROMPT = "Who is Linus Torvalds?"  # What I want to ask the LLM

try:
    SYSTEM_PROMPT = "You are a helpful assistant. Be as accurate and brief as possible."
    response: ChatResponse = chat(
        model=LLM_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": CHAT_PROMPT},
        ],
        # stream=False # No need - this is false by default
    )

    print(f"The LLM ({LLM_NAME}) responded with the following:")
    print(response["message"]["content"])

except Exception as e:
    print('There was an Error:', e)
