import pandas as pd
import fitz  # PyMuPDF
from docx import Document


class DocumentProcessor:
    """
    Enterprise Document Processing Engine

    Supports:
    - Excel (.xlsx, .xls)
    - Word (.docx)
    - PDF (.pdf)
    - Text (.txt)

    Converts business documents into AI-friendly text.
    """

    def process(self, uploaded_file):

        if uploaded_file is None:
            return ""

        filename = uploaded_file.name.lower()

        if filename.endswith((".xlsx", ".xls")):
            return self._process_excel(uploaded_file)

        elif filename.endswith(".docx"):
            return self._process_docx(uploaded_file)

        elif filename.endswith(".pdf"):
            return self._process_pdf(uploaded_file)

        elif filename.endswith(".txt"):
            return self._process_txt(uploaded_file)

        return ""

    # ----------------------------------------------------
    # Excel
    # ----------------------------------------------------

    def _process_excel(self, uploaded_file):

        df = pd.read_excel(uploaded_file).fillna("")

        if df.empty:
            return ""

        text = []

        text.append("COMPETITIVE ANALYSIS DOCUMENT")
        text.append("")

        columns = list(df.columns)

        # ------------------------------------------------
        # Detect feature comparison matrix
        # ------------------------------------------------

        if len(columns) >= 3:

            first_column = columns[0]

            text.append("Document Type: Feature Comparison Matrix")
            text.append("")

            for _, row in df.iterrows():

                feature = str(row[first_column]).strip()

                if feature == "":
                    continue

                text.append(f"Feature: {feature}")

                for col in columns[1:]:

                    value = str(row[col]).strip()

                    if value:

                        text.append(
                            f"{col}: {value}"
                        )

                text.append("")

        else:

            text.append("Document Type: Spreadsheet")
            text.append("")

            text.append(df.to_string(index=False))

        return "\n".join(text)

    # ----------------------------------------------------
    # Word
    # ----------------------------------------------------

    def _process_docx(self, uploaded_file):

        doc = Document(uploaded_file)

        paragraphs = []

        paragraphs.append("COMPETITIVE ANALYSIS DOCUMENT")
        paragraphs.append("")
        paragraphs.append("Document Type: Word Report")
        paragraphs.append("")

        for p in doc.paragraphs:

            if p.text.strip():

                paragraphs.append(
                    p.text.strip()
                )

        return "\n".join(paragraphs)

    # ----------------------------------------------------
    # PDF
    # ----------------------------------------------------

    def _process_pdf(self, uploaded_file):

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        text = []

        text.append("COMPETITIVE ANALYSIS DOCUMENT")
        text.append("")
        text.append("Document Type: PDF Report")
        text.append("")

        for page in pdf:

            page_text = page.get_text()

            if page_text.strip():

                text.append(page_text)

        return "\n".join(text)

    # ----------------------------------------------------
    # TXT
    # ----------------------------------------------------

    def _process_txt(self, uploaded_file):

        text = uploaded_file.read().decode("utf-8")

        return (
            "COMPETITIVE ANALYSIS DOCUMENT\n\n"
            "Document Type: Text Document\n\n"
            + text
        )


# --------------------------------------------------------
# Convenience Function
# --------------------------------------------------------

def extract_competitor_text(uploaded_file):

    processor = DocumentProcessor()

    return processor.process(uploaded_file)