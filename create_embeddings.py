from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------
# Load document
# --------------------------------

file_path = Path("data/sample_company.txt")

text = file_path.read_text(
    encoding="utf-8"
)


# --------------------------------
# Split document
# --------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

print(f"📄 Created {len(chunks)} chunks")


# --------------------------------
# Load embedding model
# --------------------------------

print("🔄 Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("✅ Embedding model loaded!")


# --------------------------------
# Create ChromaDB
# --------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="company_documents"
)


# --------------------------------
# Create embeddings
# --------------------------------

embeddings = model.encode(
    chunks
).tolist()


# --------------------------------
# Store in ChromaDB
# --------------------------------

ids = [
    f"chunk_{i}"
    for i in range(len(chunks))
]

collection.upsert(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=[
        {
            "source": "sample_company.txt",
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]
)


print()
print(
    f"🎉 Stored {len(chunks)} chunks in ChromaDB!"
)