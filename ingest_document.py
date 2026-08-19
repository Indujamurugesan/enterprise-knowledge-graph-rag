import os
import chromadb

from document_processor import process_document


# ==========================================
# ChromaDB Setup
# ==========================================

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "company_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ==========================================
# Ingest Document
# ==========================================

def ingest_document(file_path):

    print()
    print("=" * 50)
    print("📄 DOCUMENT INGESTION")
    print("=" * 50)

    # --------------------------------------
    # Process document
    # --------------------------------------

    chunks = process_document(
        file_path
    )

    if not chunks:

        print("❌ No text found in document.")

        return 0


    # --------------------------------------
    # Prepare data
    # --------------------------------------

    file_name = os.path.basename(
        file_path
    )

    ids = []

    documents = []

    metadatas = []


    for index, chunk in enumerate(chunks):

        ids.append(
            f"{file_name}_{index}"
        )

        documents.append(
            chunk
        )

        metadatas.append({
            "source": file_name,
            "chunk": index
        })


    # --------------------------------------
    # Store in ChromaDB
    # --------------------------------------

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )


    print()
    print(
        f"✅ Stored {len(chunks)} chunks "
        "in ChromaDB"
    )

    print(
        f"📚 Source: {file_name}"
    )

    return len(chunks)


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    print(
        "🚀 Document ingestion module ready!"
    )