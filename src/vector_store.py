import chromadb

from sentence_transformers import SentenceTransformer
from document_loader import extract_text_from_pdf
from text_splitter import split_text


PDF_PATH = "data/company_document.pdf"

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")

# Extract text
text = extract_text_from_pdf(PDF_PATH)

# Split text into chunks
chunks = split_text(text)

# Create embeddings
embeddings = model.encode(chunks).tolist()

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="company_documents"
)

# Store chunks and embeddings
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)

print(f"Stored {len(chunks)} chunks in ChromaDB!")