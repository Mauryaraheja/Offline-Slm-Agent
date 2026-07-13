"""
Six zero-network tools the agent can call.
"""

import ast
import operator
from datetime import datetime
from pathlib import Path

from src.config import SANDBOX_DIR

# Create sandbox folder if it doesn't exist
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

# Allowed operators for the calculator
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


## _ in front of function name means private helper function , user can't call it directly 
def _eval_node(node: ast.AST) -> float:
    """
    Recursively evaluate one AST node, allowing only numbers
    and arithmetic operations.
    """

    # Number (e.g., 5, 3.14)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    # Binary operations (+, -, *, /, %, **)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](
            _eval_node(node.left),
            _eval_node(node.right),
        )

    # Unary operations (+5, -5)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](
            _eval_node(node.operand)
        )

    raise ValueError(
        f"Unsupported expression element: {ast.dump(node)}"
    )


# why not use path(filename) because then ai could use /././. to escape folder 
def _safe_path(filename: str) -> Path:
    """
    Return a safe path inside the sandbox directory.
    """

    path = (SANDBOX_DIR / filename).resolve()

    if SANDBOX_DIR.resolve() not in path.parents and path != SANDBOX_DIR.resolve():
        raise ValueError("Access outside sandbox is not allowed.")

    return path

def calculator(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    
def write_note(filename: str, content: str) -> str:
    """
    Write content to a file inside the sandbox.
    """
    path = _safe_path(filename)
    path.write_text(content, encoding="utf-8")
    return f"Saved note to '{filename}'."

def read_note(filename: str) -> str:
    """
    Read a file from the sandbox.
    """
    path = _safe_path(filename)

    if not path.exists():
        return "File does not exist."

    return path.read_text(encoding="utf-8")
