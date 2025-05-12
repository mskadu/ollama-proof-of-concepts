import ollama
import yaml

def generate_openapi_spec(user_stories):
    prompt = f"""
    Create OpenAPI 3.0 specification from these requirements:
    {user_stories}
    
    Include: endpoints, schemas, security requirements
    """
    
    response = ollama.generate(
        model='codellama',
        prompt=prompt,
        system="Output valid YAML without any Markdown formatting",
        options={'temperature': 0.3}
    )
    
    try:
        # Remove Markdown code blocks
        cleaned_yaml = response['response'].split('```yaml')[-1].split('```')[0].strip()
        return yaml.safe_load(cleaned_yaml)
    except yaml.YAMLError as e:
        print(f"Failed to parse:\n{cleaned_yaml}")
        raise

# Example usage with better error handling
if __name__ == "__main__":
    sample_requirements = """
    Create a blog API with:
    - CRUD operations for posts
    - Tagging system
    - JWT authentication
    - Pagination
    - Search endpoint
    """
    
    try:
        print("Writing OpenAPI spec...")
        spec = generate_openapi_spec(sample_requirements)
        
        with open('spec.yaml', 'w') as f:
            yaml.dump(spec, f, sort_keys=False)
            
        print("Successfully generated specification!")
        print(f"Version: {spec['info']['version']}")
        
    except Exception as e:
        print(f"Generation failed: {str(e)}")
