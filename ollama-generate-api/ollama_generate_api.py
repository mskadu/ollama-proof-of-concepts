"""
This script demonstrates how to use the Ollama API to generate text using the requests library.
"""
import json
import requests

url = "http://localhost:11434/api/generate"
data = {
    "model": "llama3.2",
    "prompt": "tell me a joke and make it rhyme"
}

# Use streaming response to handle large responses
response = requests.post(url, json=data, stream=True)

#check the response status
if response.status_code == 200:
    print("Generated Text:", end=" ", flush=True)
    
    # Iterate over the streaming response
    for line in response.iter_lines():
        #decode the line and parse JSON
        decoded_line = line.decode("utf-8")
        result = json.loads(decoded_line)
        
        #get text from the response
        generated_text = result.get("response", "")
        print( generated_text, end="", flush=True)
        
else:
    print("Error:", response.status_code, response.text)