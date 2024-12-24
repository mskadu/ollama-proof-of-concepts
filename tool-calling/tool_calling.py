"""PoC for implementing tool-calling with Ollama3.2"""
import ollama
import requests

LLM_NAME = "llama3.2"  # The generative LLM


def get_current_weather(city):
    """Get the current weather for a city using a free API"""
    url = f"http://wttr.in/{city}?format=3"
    try:
        weather_response = requests.get(url, timeout=5)
        if weather_response.status_code == 200:
            city_weather = weather_response.text.split(':')[1].strip()
            return f"The current weather in {city} is {city_weather}."
        else:
            return f"Could not retrieve weather data for {city}."

    except requests.exceptions.RequestException as e:
        return f"An error occurred while retrieving weather data: {e}"


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

PROMPT_TEXT = "What is the weather in Jakarta?"
# PROMPT_TEXT = "How hot is it in California today?"
# PROMPT_TEXT = "Will I need an umbrella today?"  # note how there is no city?

# note this is irrelevant to our tool/ function
# So you should see a "City not found in tool call arguments" message
# PROMPT_TEXT = "Who is Mahatma Gandhi?"

response = ollama.chat(
    model=LLM_NAME,
    messages=[{"role": "user", "content": PROMPT_TEXT}],
    tools=[weather_tool],
)

# Check for tool calls in the response
if "tool_calls" in response["message"]:
    tool_call = response["message"]["tool_calls"][0]

    # Check for city in function arguments
    if "city" in tool_call.function.arguments:
        arg_city = tool_call.function.arguments["city"]

        weather_info = get_current_weather(arg_city)
        print(weather_info)
    else:
        print("City not found in tool call arguments")
else:
    print("No tool calls made.")
