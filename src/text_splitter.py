from document_loader import extract_text_from_pdf


PDF_PATH = "data/company_document.pdf"


def split_text(text, chunk_size=300, chunk_overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


text = extract_text_from_pdf(PDF_PATH)

chunks = split_text(text)

print(f"Total chunks created: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)