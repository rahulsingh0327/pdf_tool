from server import mcp
import os
from typing import Any, Dict, Optional
import PyPDF2


def pdf_extract_text(file_path: str, max_pages: Optional[int] = None) -> str:
    """
    Extract textual content from a PDF file.

    Args:
        file_path: Path to local PDF file.
        max_pages: Optionally limit the number of pages to read.

    Returns:
        Concatenated string of extracted text.

    Raises:
        RuntimeError if PyPDF2 not installed or file cannot be read.
    """
    text_parts = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num = len(reader.pages)
        limit = num if max_pages is None else min(num, max_pages)
        for i in range(limit):
            page = reader.pages[i]
            try:
                text_parts.append(page.extract_text() or "")
            except Exception:
                continue
    return "\n".join(text_parts)


def pdf_page_count(file_path: str) -> int:
    """
    Return the number of pages in a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Integer page count.
    """
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)


@mcp.tool()
def pdf_tool(action: str, path: str, max_pages: int = 5) -> Dict[str, Any]:
    """
    PDF utility tool supporting 'text' and 'meta' actions.

    Args:
        action: "text" to extract text, "meta" to return page count.
        path: Local path to the PDF file.
        max_pages: Max pages to extract for 'text'.

    Returns:
        Dictionary with extracted text or metadata.

    Notes:
        Requires PyPDF2.
    """
    action = action.lower()
    if action == "text":
        return {"text": pdf_extract_text(path, max_pages)}
    if action == "meta":
        return {"page_count": pdf_page_count(path)}
    raise ValueError("Unsupported PDF action. Use 'text' or 'meta'.")
