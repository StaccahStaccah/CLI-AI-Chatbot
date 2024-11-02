# Built-in libraries
import json

# Local libraries
from src.console import console

def get_history():
    """Load the chat history from the history.json file."""
    try:
        with open("history.json", "r") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    return history


def delete_history():
    """Delete the chat history from the history.json file."""
    try:
        with open("history.json", "w") as file:
            file.write("[]")
    except Exception as e:
        console.print(f"Error deleting history: {e}", style="bold red")


def save_chat_to_history(type, role, content):
    """Save the user's prompt to the history.json file."""
    import json
    
    history_file = "history.json"
    try:
        # Load existing history
        try:
            with open(history_file, "r") as file:
                history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        # Append new string to history
        history.append({"role": role, "parts": [content]})

        # Save updated history
        with open(history_file, "w") as file:
            json.dump(history, file, indent=4)

    except Exception as e:
        console.print(f"Error saving {type} to history: {e}", style="bold red")