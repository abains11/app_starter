# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Uses `uv` for environment and dependency management.

```bash
uv sync                                # create venv + install locked deps (Python 3.13 via .python-version)
source .venv/Scripts/activate          # Windows/Git Bash; .venv/bin/activate on Unix
uv run main.py                         # start the MCP server (FastMCP, "docs")
uv run pytest                          # run all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf   # single test
```

No linter is configured.

**Python version:** `pyproject.toml` allows `>=3.10`, but Python 3.15 does not work: `markitdown` depends on `magika` -> `onnxruntime`, which has no cp315 wheels. Use 3.10–3.13; `.python-version` pins 3.13 for uv.

**pydantic is capped `<2.14`** in `pyproject.toml`: 2.14 removed `eval_type_backport`, which the pinned `mcp==1.8.0` imports. Prefer `uv sync` (uses `uv.lock`) over `uv pip install -e .`.

## Code style

- Always apply appropriate type annotations to function arguments (and return values).

## Architecture

A small MCP server exposing document-processing tools to AI assistants.

- `main.py` creates the `FastMCP("docs")` server (from `mcp.server.fastmcp`) and registers each tool with `mcp.tool()(fn)`. A new tool must be both implemented in `tools/` and registered here.
- `tools/` holds plain Python functions, grouped by module; they have no MCP dependency and can be unit-tested directly.
  - `tools/math.py`: `add`, the reference example of a fully documented tool.
  - `tools/document.py`: `binary_document_to_markdown(binary_data, file_type)` wraps `markitdown` (bytes + file extension such as `"docx"`/`"pdf"` -> markdown text); it is a helper, not a registered tool. `document_path_to_markdown(file_path)` is the registered tool: it validates the path and `.pdf`/`.docx` extension, reads the file, and delegates to the helper.
- `tests/test_document.py` tests the document tools against `tests/fixtures/mcp_docs.docx` and `mcp_docs.pdf`.

## Defining MCP tools

Tools are plain Python functions registered with the server:

```python
mcp.tool()(my_function)
```

The function's signature and docstring become the tool schema and description that the AI client sees, so they must be thorough.

**Parameters:** describe every parameter with pydantic `Field` as its default value:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """Comprehensive docstring here"""
```

**Docstrings** must:

- Begin with a one-line summary
- Provide a detailed explanation of the functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

Example (from `tools/math.py`):

```python
def add(
    a: float = Field(description="First number to add"),
    b: float = Field(description="Second number to add"),
) -> float:
    """Add two numbers together.

    Takes two numerical inputs and returns their sum. This tool handles
    integers and floating point numbers.

    When to use:
    - When you need to perform simple addition
    - When you need precise numerical calculation

    Examples:
    >>> add(2, 3)
    5.0
    >>> add(2.5, 3.5)
    6.0
    """
    return a + b
```
