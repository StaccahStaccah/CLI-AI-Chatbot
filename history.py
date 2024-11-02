# Local libraries
from console import console


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