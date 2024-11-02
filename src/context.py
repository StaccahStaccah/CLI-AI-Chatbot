# Built-in libraries
import json


def get_contexts():
    """Load the chat contexts from the contexts.json file."""
    try:
        with open("contexts.json", "r") as file:
            contexts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        contexts = None
    
    return contexts

