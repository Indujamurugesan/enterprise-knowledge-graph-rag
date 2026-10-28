
import os
from pypdf import PdfReader

def extract_pdf_text(file_path):
    text = ""
    reader = PdfReader(file_path)

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def extract_txt_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)
    elif extension == ".txt":
        return extract_txt_text(file_path)
    else:
        raise ValueError("Only PDF and TXT files are supported.")

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def process_document(file_path):
    print("\nProcessing document...")
    print("File:", os.path.basename(file_path))

    text = extract_text(file_path)
    print(f"Extracted {len(text)} characters")

    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    return chunks

if __name__ == "__main__":
    print("Document processor ready!")
