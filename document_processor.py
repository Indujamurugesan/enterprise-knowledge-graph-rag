import os
import fitz


# ==========================================
# Extract text from PDF
# ==========================================

def extract_pdf_text(file_path):

    text = ""

    document = fitz.open(file_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text


# ==========================================
# Extract text from TXT
# ==========================================

def extract_txt_text(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ==========================================
# Extract text from PDF or TXT
# ==========================================

def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return extract_pdf_text(
            file_path
        )

    elif extension == ".txt":

        return extract_txt_text(
            file_path
        )

    else:

        raise ValueError(
            "Only PDF and TXT files are supported."
        )


# ==========================================
# Split text into chunks
# ==========================================

def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


# ==========================================
# Process Document
# ==========================================

def process_document(file_path):

    print()
    print("📄 Processing document...")
    print(
        "File:",
        os.path.basename(file_path)
    )

    # Extract text
    text = extract_text(
        file_path
    )

    print(
        f"✅ Extracted {len(text)} characters"
    )

    # Create chunks
    chunks = chunk_text(
        text
    )

    print(
        f"✅ Created {len(chunks)} chunks"
    )

    return chunks


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    print(
        "📄 Document processor ready!"
    )