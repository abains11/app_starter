import os
import shutil
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_docx_path(self):
        """Test converting a DOCX file by path."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_pdf_path(self):
        """Test converting a PDF file by path."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_matches_binary_conversion(self):
        """Path-based conversion should match the binary conversion."""
        with open(self.DOCX_FIXTURE, "rb") as f:
            expected = binary_document_to_markdown(f.read(), "docx")
        assert document_path_to_markdown(self.DOCX_FIXTURE) == expected

    def test_uppercase_extension(self, tmp_path):
        """File extensions are matched case-insensitively."""
        upper = tmp_path / "MCP_DOCS.PDF"
        shutil.copy(self.PDF_FIXTURE, upper)
        result = document_path_to_markdown(str(upper))
        assert len(result) > 0

    def test_missing_file(self, tmp_path):
        """A nonexistent path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(tmp_path / "missing.pdf"))

    def test_directory_path(self, tmp_path):
        """A directory path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(tmp_path))

    def test_unsupported_extension(self, tmp_path):
        """Unsupported file types raise ValueError."""
        txt = tmp_path / "notes.txt"
        txt.write_text("hello")
        with pytest.raises(ValueError):
            document_path_to_markdown(str(txt))
