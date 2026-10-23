# Document Tools

A Python package implementing a variety of document-related tools for converting and processing document formats. These tools are exposed through an MCP server interface for seamless integration with AI assistants.

## Setup

Requires Python 3.10–3.13 (`onnxruntime`, a `markitdown` dependency, has no wheels for newer versions). The `.python-version` file selects 3.13.

```bash
# Create a virtual env and install the locked dependencies
uv sync

# Activate it (on Windows: .venv\Scripts\activate)
source .venv/bin/activate
```

## Running

```bash
# Start the MCP server
uv run main.py
```

## Testing

```bash
# Run all tests
uv run pytest
```

## Development

### Tool Definitions

Tools are defined as Python functions and registered with the MCP server:

```python
mcp.tool()(my_function)
```

Tool descriptions should:

- Begin with a one-line summary
- Provide detailed explanation of functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

Use `Field` from pydantic for parameter descriptions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```
