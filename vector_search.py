import chromadb

from sentence_transformers import SentenceTransformer


# -----------------------------
# Load embedding model
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------
# Connect to ChromaDB
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="company_documents"
)


# -----------------------------
# User question
# -----------------------------

query = "Who works on Project Alpha?"


# -----------------------------
# Convert question to vector
# -----------------------------

query_embedding = model.encode(
    query
).tolist()


# -----------------------------
# Search ChromaDB
# -----------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)


# -----------------------------
# Display results
# -----------------------------

print("🔍 Query:")
print(query)

print()
print("📚 Relevant chunks:")

for i, document in enumerate(
    results["documents"][0]
):

    print()
    print(f"--- Result {i + 1} ---")
    print(document)