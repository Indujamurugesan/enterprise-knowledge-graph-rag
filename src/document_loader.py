import pymupdf

PDF_PATH = "data/company_document.pdf"


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


if __name__ == "__main__":
    text = extract_text_from_pdf(PDF_PATH)

    print("PDF text extracted successfully!\n")
    print(text)