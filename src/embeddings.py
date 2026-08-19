from sentence_transformers import SentenceTransformer
from text_splitter import split_text
from document_loader import extract_text_from_pdf


PDF_PATH = "data/company_document.pdf"

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")

text = extract_text_from_pdf(PDF_PATH)

chunks = split_text(text)

embeddings = model.encode(chunks)

print(f"Number of chunks: {len(chunks)}")
print(f"Embedding shape: {embeddings.shape}")