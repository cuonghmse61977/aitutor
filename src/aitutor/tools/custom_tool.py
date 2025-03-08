import json
from crewai.tools import tool
from crewai import LLM

llm = LLM(
		model="gemini/gemini-2.0-flash",
		temperature=0.3,
		api_key="AIzaSyBMLXoaoDU8gMe0qLNWGA91tOxx4GNfvew"
	)

def load_data(file_path):
    """Loads JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
@tool("Load examaples to generate explanation")
def load_examples(answer: str) -> str:
    """Load examaples to generate explanation"""
    training_data = load_data("src/aitutor/training_set.json")
    examples_to_use = training_data[:50]

    examples = "\n".join([f"Question: ${item['item_description']}\n{item['question_content']}\nAnswer: {item['explanation']}" for item in examples_to_use])
    
    return examples