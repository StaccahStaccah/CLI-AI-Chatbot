# Built-in libraries
import os
import sys
import subprocess
import json

# Gemini SDK
import google.generativeai as genai

# Third-party libraries
from dotenv import load_dotenv

# Local libraries
from src.console import console, print_ascii_art
from src.context import get_contexts
from src.gemini import init_gemini, start_chat, send_message
from src.history import save_chat_to_history, get_history, delete_history


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


def start_chatbot():
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
    
    # Check if history file exists
    history = get_history()
    if history != []:
        console.print("Do you want to continue the previous chat session? (y/n)", style="bold yellow")
        while True:
            response = console.input("[bold yellow]> [/]")
            if response.lower() == "n":
                delete_history()
                history = []
                break
            elif response.lower() == "y":
                console.print("Continuing previous chat session...", style="bold yellow")
                break
            else:
                console.print("Invalid response. Please enter 'y' or 'n'.", style="bold red")
    
    # If is a new chat session, ask user to select a context
    if history == []:
        contexts = get_contexts()
        if contexts:
            console.print("Who do you want to chat with?", style="bold yellow")
            for idx, context in enumerate(contexts):
                console.print(f"{idx+1}. {context['name']}")
            while True:
                try:
                    context_idx = int(console.input("[bold yellow]> [/]")) - 1
                    if 0 <= context_idx < len(contexts):
                        break
                    else:
                        console.print("Invalid context index. Please try again.", style="bold red")
                except ValueError:
                    console.print("Invalid input. Please enter a number.", style="bold red")
            selected_context = contexts[context_idx]
            history = [{"role": "user", "parts": [selected_context["context"]]}]
            save_chat_to_history("context", "user", selected_context["context"])
    
    # Start a new chat session
    chat = start_chat(model, history)
        
    console.print("Hi, how can I assist you today? Feel free to ask anything! (Type '!exit' to quit)", style="bold cyan")
    
    while True:
        # Accept user's next message, add to context, resubmit context to Gemini
        prompt = console.input("[bold yellow]> [/]")
        if prompt.lower() == "!exit":
            console.print("Goodbye!", style="bold cyan")
            break
        
        if prompt:
            # Save prompt to history file
            save_chat_to_history("prompt", "user", prompt)
            
            send_message(chat, prompt)
