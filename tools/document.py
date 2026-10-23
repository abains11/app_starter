from pathlib import Path
from markitdown import MarkItDown, StreamInfo  # pyright: ignore[reportMissingImports]
from io import BytesIO
from pydantic import Field

SUPPORTED_EXTENSIONS = {"pdf", "docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Absolute or relative path to a .pdf or .docx file on the server's filesystem"
    ),
) -> str:
    """Read a PDF or DOCX file from disk and convert its contents to markdown.

    Opens the file at the given path, detects its type from the file
    extension (case-insensitive), and converts the document to
    markdown-formatted text. Headings, lists, and tables are preserved where
    the source format allows. Relative paths are resolved against the
    server's current working directory.

    When to use:
    - When you have the path to a PDF or DOCX file and need its text content
    - When you want to read or summarize a document as markdown

    When not to use:
    - For other file types (e.g. .txt, .xlsx, .pptx); they are rejected
    - When you already have the document's raw bytes rather than a path

    Raises:
    - FileNotFoundError if the path does not exist or is not a file
    - ValueError if the file extension is not .pdf or .docx

    Examples:
    >>> document_path_to_markdown("reports/summary.docx")
    '# Summary\n\nQuarterly results ...'
    >>> document_path_to_markdown("/data/paper.pdf")
    'Abstract\n\nThis paper ...'
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"No file found at path: {file_path}")

    extension = path.suffix.lower().lstrip(".")
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'. Supported types: .pdf, .docx"
        )

    return binary_document_to_markdown(path.read_bytes(), extension)
