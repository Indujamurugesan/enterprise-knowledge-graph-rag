from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Read document
file_path = Path("data/sample_company.txt")

text = file_path.read_text(
    encoding="utf-8"
)


# Create text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


# Split document
chunks = splitter.split_text(text)


print(f"✅ Document split into {len(chunks)} chunks")
print()


# Display chunks
for i, chunk in enumerate(chunks):

    print(f"--- CHUNK {i + 1} ---")
    print(chunk)
    print()