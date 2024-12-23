"""PoC for implementing tool-calling with Ollama3.2"""
import ollama

LLM_NAME = "llama3.2"  # The generative LLM


def get_current_weather(city):
    """dummy function to get current weather"""
    # returning a mock response
    return f"The current weather in {city} is sunny with a temperature of 31°C."


# The tool/ function to be used by our LLM
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city",
                },
            },
            "required": ["city"],
        },
    },
}

# Our question to the LLM - the prompt
##
# NOTE: Uncomment just one of the prompts below to see how
# the output changes
##

# PROMPT_TEXT = "What is the weather in Jakarta?"
PROMPT_TEXT = "How hot is it in California today?"
# PROMPT_TEXT = "Will I need an umbrella today?" # note how there is no city?

# note this is irrelevant to our tool/ function
# PROMPT_TEXT = "Who is Mahatma Gandhi?"

response = ollama.chat(
    model=LLM_NAME,
    messages=[{"role": "user", "content": PROMPT_TEXT}],
    tools=[weather_tool],
)
# Peek at the response to see what we've got.
# print(response)

# Check for tool calls in the response
if "tool_calls" in response["message"]:
    tool_call = response["message"]["tool_calls"][0]
    # print("tool_call: ", tool_call)

    # Check for city in function arguments
    if "city" in tool_call.function.arguments:
        arg_city = tool_call.function.arguments["city"]

        weather_info = get_current_weather(arg_city)
        print(weather_info)
    else:
        print("City not found in tool call arguments")
else:
    print("No tool calls made.")
