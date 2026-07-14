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
    #return immediately returns value to run_agent()
    except Exception as exc:
        return f"Error running {name}: {exc}"

def run_agent(user_input: str) -> str:
    """Run the local ReAct loop and return the assistant's final answer."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    #This is saved as list because it remembers the flow of conversation (memory management)
    # using _ instead of i means we don't care about the loop variable
    for _ in range(MAX_STEPS):

      response = _client.chat(
        model=MODEL,
        messages=messages, 
        tools=TOOL_FUNCTIONS,
      )  
    
    #right side messages is our variable , left side is what ollama expects
    #here in respose block , python sends everything to ollama
      msg = response.message

      messages.append(msg)
      #appending helps model to remember things that it said , not overwriting 
      #but it is necessary
      if not msg.tool_calls:
        return msg.content or ""

      for call in msg.tool_calls:
        result = _execute_tool_call(
            call.function.name,
            call.function.arguments,
        )

    #for loop is used because model could request multiple tools