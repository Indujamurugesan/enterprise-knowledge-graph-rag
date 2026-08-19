import chromadb

from sentence_transformers import SentenceTransformer


print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


# Connect to existing ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="company_documents"
)


# User question
question = input("\nAsk a question: ")


# Convert question into embedding
question_embedding = model.encode([question]).tolist()


# Search ChromaDB
results = collection.query(
    query_embeddings=question_embedding,
    n_results=2
)


print("\nRelevant information:\n")

for document in results["documents"][0]:
    print(document)
    print("--------------------")