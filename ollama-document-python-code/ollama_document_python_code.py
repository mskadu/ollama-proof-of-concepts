from ollama_env_setup import query_ollama


def document_code(code_snippet: str, model: str = "codellama") -> str:
    """
    Generate comprehensive documentation for the given code snippet.

    Args:
        code_snippet: The code to document
        model: The Ollama model to use (preferably a code-specialized model)

    Returns:
        Documented code with added comments and docstrings
    """
    prompt = f"""
    Add comprehensive documentation to the following Python code.
    Include:
    - Detailed docstrings in Google format
    - In-line comments for complex logic
    - Type hints
    - Brief explanation of the purpose of each function/class
    
    Here's the code:
    
    ```python
    {code_snippet}
    ```
    
    Return only the documented code without any additional explanations.
    """

    system_prompt = "You are an expert Python developer skilled in writing clear, comprehensive documentation."
    documented_code = query_ollama(prompt, model, system_prompt)

    return documented_code


# Example usage
def example_documentation():
    undocumented_code = """
    def process_data(data, columns, filter_condition=None):
        df = pd.DataFrame(data)
        if filter_condition:
            df = df[df.apply(filter_condition, axis=1)]
        result = df[columns].to_dict('records')
        return result
    
    class DataProcessor:
        def __init__(self, source):
            self.source = source
            self.data = None
        
        def load(self):
            if self.source.endswith('.csv'):
                self.data = pd.read_csv(self.source)
            elif self.source.endswith('.json'):
                self.data = pd.read_json(self.source)
            return self
        
        def transform(self, operations):
            for op in operations:
                self.data = op(self.data)
            return self
    """

    documented = document_code(undocumented_code,"llama3.2")
    print(documented)


if __name__ == "__main__":
    example_documentation()
