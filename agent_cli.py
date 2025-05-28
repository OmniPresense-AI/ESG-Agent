from agents import Agent, FileSearchTool, Runner, OpenAIChatCompletionsModel, set_default_openai_api
from dotenv import load_dotenv
from openai import OpenAI
import os
import importlib.util
import glob
import json
from datetime import datetime
import sys
from typing import Any, Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

# Set default API type for chat completions
set_default_openai_api("chat_completions")

# Initialize OpenAI client and Rich console
openai_client = OpenAI()
console = Console()

class ConversationLogger:
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
    
    def log_message(self, role: str, content: str, tool_calls: List[Dict] = None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = {
            "timestamp": timestamp,
            "role": role,
            "content": content,
            "tool_calls": tool_calls or []
        }
        self.messages.append(message)
        self._print_message(message)
    
    def _print_message(self, message: Dict[str, Any]):
        if message["role"] == "user":
            console.print(Panel(
                message["content"],
                title=f"[bold blue]User Input[/bold blue] ({message['timestamp']})",
                border_style="blue"
            ))
        elif message["role"] == "assistant":
            console.print(Panel(
                message["content"],
                title=f"[bold green]Agent Response[/bold green] ({message['timestamp']})",
                border_style="green"
            ))
            if message["tool_calls"]:
                for tool_call in message["tool_calls"]:
                    self._print_tool_call(tool_call)
    
    def _print_tool_call(self, tool_call: Dict[str, Any]):
        table = Table(title=f"Tool Call: {tool_call['name']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Arguments", Syntax(
            json.dumps(tool_call["args"], indent=2),
            "json",
            theme="monokai"
        ))
        table.add_row("Result", Syntax(
            json.dumps(tool_call["result"], indent=2),
            "json",
            theme="monokai"
        ))
        
        console.print(table)

class LoggingRunner(Runner):
    def __init__(self):
        super().__init__()
        self.logger = ConversationLogger()
    
    def run_sync(self, agent, query):
        # Log user input
        self.logger.log_message("user", query)
        
        # Execute query
        result = super().run_sync(agent, query)
        
        # Log tool calls and response
        tool_calls = []
        if hasattr(result, 'tool_calls'):
            for tool_call in result.tool_calls:
                tool_calls.append({
                    "name": tool_call.name,
                    "args": tool_call.args,
                    "result": tool_call.result
                })
        
        self.logger.log_message("assistant", result.final_output, tool_calls)
        return result

def load_agent_module(file_path):
    """Load an agent module from a Python file."""
    try:
        spec = importlib.util.spec_from_file_location("agent_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.agent
    except Exception as e:
        console.print(f"[bold red]Error loading agent from {file_path}: {str(e)}[/bold red]")
        return None

def get_available_agents():
    """Get all available agent files in the Agents directory."""
    agent_files = glob.glob("Agents/*.py")
    agents = {}
    
    for file in agent_files:
        agent = load_agent_module(file)
        if agent:
            key = os.path.basename(file).replace(".py", "")
            agents[key] = agent
    
    return agents

def chat_with_agent(agent):
    """Start a chat session with a specific agent."""
    console.print(Panel(
        f"Starting chat with {agent.name}!",
        title="[bold green]Chat Session[/bold green]",
        border_style="green"
    ))
    console.print("[yellow]Type 'exit' or 'quit' to end the conversation.[/yellow]")
    console.print("[yellow]Type 'back' to return to agent selection.[/yellow]")
    console.print("[yellow]Type your questions below.[/yellow]\n")

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check if user wants to exit or go back
            if user_input.lower() in ['exit', 'quit']:
                console.print("[bold green]Goodbye![/bold green]")
                return False
            elif user_input.lower() == 'back':
                return True
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get response from agent
            console.print("\n[yellow]Agent is thinking...[/yellow]")
            result = LoggingRunner().run_sync(agent, user_input)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Returning to agent selection...[/yellow]")
            return True
        except Exception as e:
            console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")
            console.print("[yellow]Please try again.[/yellow]")

def main():
    while True:
        # Get available agents
        agents = get_available_agents()
        
        if not agents:
            console.print("[bold red]No agent files found in the current directory![/bold red]")
            console.print("[yellow]Please create agent files with names ending in '_agent.py'[/yellow]")
            return
        
        # Display available agents
        console.print("\n[bold]Available Agents:[/bold]")
        for i, (name, agent) in enumerate(agents.items(), 1):
            console.print(f"{i}. {agent.name}")
        console.print("0. Exit")
        
        try:
            # Get user selection
            choice = input("\nSelect an agent (number) or 'exit': ").strip()
            
            if choice.lower() in ['exit', '0']:
                console.print("[bold green]Goodbye![/bold green]")
                break
            
            # Convert choice to index
            try:
                index = int(choice) - 1
                if 0 <= index < len(agents):
                    selected_agent = list(agents.values())[index]
                    # Start chat session with selected agent
                    if not chat_with_agent(selected_agent):
                        break
                else:
                    console.print("[yellow]Invalid selection. Please try again.[/yellow]")
            except ValueError:
                console.print("[yellow]Please enter a valid number.[/yellow]")
                
        except KeyboardInterrupt:
            console.print("\n[bold green]Goodbye![/bold green]")
            break

if __name__ == "__main__":
    main() 