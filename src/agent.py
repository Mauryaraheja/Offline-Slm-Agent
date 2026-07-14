"""
The hand-built agent loop: think -> call tools -> observe -> repeat -> answer.

One function, run_agent(), owns the whole ReAct cycle against a local
Ollama model.
"""

from ollama import Client

from src.config import MAX_STEPS, MODEL, OLLAMA_HOST, SYSTEM_PROMPT
from src.tools import TOOL_FUNCTIONS, TOOL_MAP

# One client for the process. host=None falls back to http://localhost:11434
_client = Client(host=OLLAMA_HOST)
#this is outside the function because everytime we call it, python would do
#create client , talk , destroy , again repeat (unnecessary)

def _execute_tool_call(name: str, arguments: dict) -> str:
    """Run one tool by name; return its result or a readable error for the model."""
    
    fn = TOOL_MAP.get(name)
    #.get prevents program from crashing (in case of error)

    if fn is None:
        return (
            f"Error: no tool named '{name}'. "
            f"Available: {', '.join(TOOL_MAP)}."
        )

    try:
        return fn(**arguments)

    #this ** before aguments do dictionary unpacking thing
    except Exception as exc:
        return f"Error running {name}: {exc}"