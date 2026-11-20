import pymupdf
from docx import Document
from io import BytesIO
from pathlib import Path


def extract_pdf_text(file_bytes):
    """Extract text from a PDF document."""

    extracted_text = []

    with pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    ) as pdf:

        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")

            if page_text.strip():
                extracted_text.append(page_text)

    return "\n".join(extracted_text)


def extract_docx_text(file_bytes):
    """Extract text from a DOCX document."""

    document = Document(BytesIO(file_bytes))

    extracted_text = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_text.append(paragraph.text)

    # Extract table contents
    for table in document.tables:
        for row in table.rows:
            row_text = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if row_text:
                extracted_text.append(" | ".join(row_text))

    return "\n".join(extracted_text)


def extract_txt_text(file_bytes):
    """Extract text from a TXT document."""

    try:
        return file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        return file_bytes.decode("cp1252")


def extract_document_text(knowledge_document):
    """
    Extract text from an uploaded KnowledgeDocument.

    Supported formats:
    PDF, DOCX and TXT.
    """

    file_name = knowledge_document.file.name
    extension = Path(file_name).suffix.lower()

    knowledge_document.file.open("rb")

    try:
        file_bytes = knowledge_document.file.read()
    finally:
        knowledge_document.file.close()

    if extension == ".pdf":
        extracted_text = extract_pdf_text(file_bytes)

    elif extension == ".docx":
        extracted_text = extract_docx_text(file_bytes)

    elif extension == ".txt":
        extracted_text = extract_txt_text(file_bytes)

    else:
        raise ValueError(
            f"Unsupported document format: {extension}"
        )

    extracted_text = extracted_text.strip()

    if not extracted_text:
        raise ValueError(
            "No readable text was found in this document."
        )

    return extracted_text
