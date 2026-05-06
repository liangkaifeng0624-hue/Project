from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file) -> str:
    try:
        reader = PdfReader(uploaded_file)
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts).strip()

    except Exception as e:
        return f"ERROR: Could not read PDF file. Details: {str(e)}"