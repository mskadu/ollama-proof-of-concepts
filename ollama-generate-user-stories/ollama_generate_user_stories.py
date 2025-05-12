import ollama
import textwrap

def text_to_user_story(input_text):
    """
    Converts free-form text into agile user stories using llama3.2 model
    Returns formatted user story with acceptance criteria
    """
    system_prompt = textwrap.dedent("""
    You are an experienced product owner. Convert the following description into 
    proper agile user stories following INVEST criteria. Format the response as:
    
    Title: [Clear user story title]
    
    As a [role], I want [feature] so that [benefit]
    
    Acceptance Criteria:
    - [Criterion 1]
    - [Criterion 2]
    - [Criterion 3]
    
    Add a 'Why:' section explaining the business value.
    """)
    
    try:
        response = ollama.generate(
            model='llama3.2',  # Verify model name with `ollama list`
            system=system_prompt,
            prompt=input_text,
            options={
                'temperature': 0.7,
                'num_predict': 500
            },
            stream=False
        )
        
        return response['response']
        
    except Exception as e:
        return f"Error generating user story: {str(e)}"

# Example usage
if __name__ == "__main__":
    sample_input = """
    We need a way for users to reset their passwords if they forget them. 
    Should include email verification and option to use security questions. 
    Make sure it's secure against brute force attacks.
    """
    
    print("Input Text:")
    print(sample_input)
    
    print("\nGenerated User Story:")
    result = text_to_user_story(sample_input)
    print(result)
