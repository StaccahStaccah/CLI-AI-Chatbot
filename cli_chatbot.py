# Built-in libraries
import os
import sys
import subprocess
import json

# Gemini SDK
import google.generativeai as genai

# Third-party libraries
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Initialize rich console
console = Console()


def load_env_vars() -> tuple[str, str]:
    """Load the API key and model name from environment variables.

    Raises:
        ValueError: If API_KEY or MODEL_NAME is not set.

    Returns:
        tuple[str, str]: The API key and model name.
    """
    try:
        load_dotenv()
        api_key = os.getenv("API_KEY")
        model_name = os.getenv("MODEL_NAME")
        if not api_key or not model_name:
            raise ValueError("API_KEY and MODEL_NAME must be set in .env file or environment variables")
        return api_key, model_name
    except Exception as e:
        console.print(f"Error loading environment variables: {e}", style="bold red")
        sys.exit(1)


def init_gemini(api_key: str, model_name: str, config):
    """Initialize Gemini model with given parameters.

    Args:
        api_key (str): The API key for Gemini.
        model_name (str): The name of the model to use.
        config (dict): Configuration parameters for the model.

    Returns:
        GenerativeModel: The initialized generative model.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name, 
            generation_config = config
        )
        return model
    except Exception as e:
        console.print(f"Error initializing Gemini: {e}", style="bold red")
        sys.exit(1)


def load_configuration() -> dict:
    """Load configuration parameters from a JSON file.

    Returns:
        dict: Configuration parameters for the model.
    """
    default_config = {"temperature": 1.0, "max_tokens": 200, "top_k": 40, "top_p": 0.9}
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        console.print("Configuration file not found. Using default values.", style="bold yellow")
        config = default_config
    
    # Merge default config with loaded config
    final_config = {**default_config, **config}
    
    return genai.GenerationConfig(
        max_output_tokens=final_config["max_tokens"],
        temperature=final_config["temperature"],
        top_k=final_config["top_k"],
        top_p=final_config["top_p"]
    )
    
    
def start_chat(model):
    """Start a new chat session.

    Args:
        model (GenerativeModel): The generative model to use for the chat.

    Returns:
        ChatSession: The started chat session.
    """
    try:
        # Load chat history
        try:
            chat_history = json.load(open("history.json", "r"))
        except (FileNotFoundError, json.JSONDecodeError):
            chat_history = [] 

        chat = model.start_chat(history=chat_history)
        return chat
    except Exception as e:
        console.print(f"Error starting chat session: {e}", style="bold red")
        sys.exit(1) 


def print_ascii_art():
    """Print ASCII art for the chatbot CLI."""
    ascii_art = """
   ___                 __        _   ___ 
  / __|___ _ __  _ __  \_\_     /_\ |_ _|
 | (__/ _ \ '  \| '_ \/ _` |   / _ \ | | 
  \___\___/_|_|_| .__/\__,_|  /_/ \_\___|
                |_|                      
                        
    """    
    console.print(ascii_art, style="bold magenta", highlight=False)


def send_message(chat, prompt):
    """Send user message to Gemini and print the response.

    Args:
        chat (ChatSession): The chat session.
        prompt (str): The user's message.
    """
    try:
        # Send user entry to Gemini and read the response in stream
        with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
            response = chat.send_message(prompt)
        
        # Save chat response to history
        save_response_to_history(response.text)
        
        console.print(Panel(Markdown(response.text)), soft_wrap=True)
    except Exception as e:
        console.print(f"Error during chat interaction: {e}", style="bold red")
        sys.exit(1)


def main():
    """Main function to run the chatbot CLI."""
    # Clear terminal and print ascii art
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
    print_ascii_art()

    # Load environment variables
    api_key, model_name = load_env_vars()

    # Get configuration parameters for the model
    config = load_configuration()
    
    # Initialize Gemini 
    model = init_gemini(api_key, model_name, config)
    
    # Start a new chat session
    chat = start_chat(model)
        
    console.print("Hi, how can I assist you today? Feel free to ask anything! (Type '!exit' to quit)", style="bold cyan")
    
    while True:
        # Accept user's next message, add to context, resubmit context to Gemini
        prompt = console.input("[bold yellow]> [/]")
        if prompt.lower() == "!exit":
            console.print("Goodbye!", style="bold cyan")
            break
        
        if prompt:
            # Save prompt to history file
            save_prompt_to_history(prompt)
            
            send_message(chat, prompt)


def save_response_to_history(response):
    """Save the response to the history.json file."""
    import json
    
    history_file = "history.json"
    try:
        # Load existing history
        try:
            with open(history_file, "r") as file:
                history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        # Append new response to history
        history.append({"role": "model", "parts": response})

        # Save updated history
        with open(history_file, "w") as file:
            json.dump(history, file, indent=4)

    except Exception as e:
        console.print(f"Error saving response to history: {e}", style="bold red")

def save_prompt_to_history(prompt):
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

        # Append new prompt to history
        history.append({"role": "user", "parts": prompt})

        # Save updated history
        with open(history_file, "w") as file:
            json.dump(history, file, indent=4)

    except Exception as e:
        console.print(f"Error saving prompt to history: {e}", style="bold red")


if __name__ == "__main__":
    main()
