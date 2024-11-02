# Built-in libraries
import sys
import json

# Gemini SDK
import google.generativeai as genai

# Third-party libraries
from rich.markdown import Markdown
from rich.panel import Panel

# Local libraries
from src.console import console
from src.history import save_chat_to_history


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


def start_chat(model, history):
    """Start a new chat session.

    Args:
        model (GenerativeModel): The generative model to use for the chat.

    Returns:
        ChatSession: The started chat session.
    """
    try:
        chat = model.start_chat(history=history)
        return chat
    except Exception as e:
        console.print(f"Error starting chat session: {e}", style="bold red")
        sys.exit(1) 
        

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
        save_chat_to_history("response", "model", response.text)
        
        console.print(Panel(Markdown(response.text)), soft_wrap=True)
    except Exception as e:
        console.print(f"Error during chat interaction: {e}", style="bold red")
        sys.exit(1)
