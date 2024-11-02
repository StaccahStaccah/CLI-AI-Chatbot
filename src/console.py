# Third-party libraries
from rich.console import Console

# Initialize rich console
console = Console()


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