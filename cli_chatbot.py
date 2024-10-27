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


# Initialize rich console
console = Console()


def load_env_vars() -> tuple[str, str]:
    """Load environment variables from .env file"""
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
    """Initialize Gemini"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name, 
            generation_config = config)
        return model
    except Exception as e:
        console.print(f"Error initializing Gemini: {e}", style="bold red")
        sys.exit(1)


def load_configuration() -> dict:
    """Load configuration parameters from a JSON file"""
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
    """Start a new chat session"""
    try:
        chat = model.start_chat(history=[])
        return chat
    except Exception as e:
        console.print(f"Error starting chat session: {e}", style="bold red")
        sys.exit(1) 

        
def print_ascii_art():
    ascii_art = """
   ___                 __        _   ___ 
  / __|___ _ __  _ __  \_\_     /_\ |_ _|
 | (__/ _ \ '  \| '_ \/ _` |   / _ \ | | 
  \___\___/_|_|_| .__/\__,_|  /_/ \_\___|
                |_|                      
                        
    """    
    console.print(ascii_art, style="bold magenta", highlight=False)
    

def send_message(chat, prompt):
    try:
        # Send user entry to Gemini and read the response in stream
        with console.status("[bold cyan]Thinking...[/bold cyan]") as status:
            response = chat.send_message(prompt)
        status.stop()
        console.print(Markdown(response.text), soft_wrap=True)  # Add slight delay to simulate streaming effect
        
    except Exception as e:
        console.print(f"Error during chat interaction: {e}", style="bold red")
        sys.exit(1) 


def main():
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
            send_message(chat, prompt)
            

if __name__ == "__main__":
    main()
