import os

import chromadb
from dotenv import load_dotenv
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


# ==========================================
# 2. ChromaDB connection
# ==========================================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="company_documents"
)


# ==========================================
# 3. Embedding model
# ==========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# 4. Vector Search
# ==========================================

def vector_search(question):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    return documents


# ==========================================
# 5. Graph Search
# ==========================================

def graph_search(question):

    keywords = [
        word.strip("?!.,")
        for word in question.split()
        if len(word.strip("?!.,"))
        > 3
    ]

    cypher = """
    MATCH (a:Entity)-[r:RELATED]->(b:Entity)

    WHERE any(keyword IN $keywords
              WHERE toLower(a.name) CONTAINS toLower(keyword)
                 OR toLower(b.name) CONTAINS toLower(keyword))

    RETURN
        a.name AS source,
        r.type AS relationship,
        b.name AS target

    LIMIT 20
    """

    relationships = []

    # Create a NEW Neo4j driver for this search
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    try:

        with driver.session() as session:

            result = session.run(
                cypher,
                keywords=keywords
            )

            for record in result:

                relationships.append(
                    f"{record['source']} "
                    f"--[{record['relationship']}]--> "
                    f"{record['target']}"
                )

    finally:

        # Close ONLY this temporary driver
        driver.close()

    return relationships


# ==========================================
# 6. Hybrid Search
# ==========================================

def hybrid_search(question):

    print("🔍 Searching Vector Database...")

    vector_results = vector_search(
        question
    )

    print(
        f"✅ Found {len(vector_results)} "
        f"relevant chunks"
    )


    print()
    print("🕸️ Searching Knowledge Graph...")

    graph_results = graph_search(
        question
    )

    print(
        f"✅ Found {len(graph_results)} "
        f"relationships"
    )


    # ======================================
    # Combine results
    # ======================================

    context = ""

    context += "DOCUMENT CONTEXT:\n"

    for document in vector_results:

        context += "\n"
        context += document
        context += "\n"


    context += "\nGRAPH CONTEXT:\n"

    for relationship in graph_results:

        context += "\n"
        context += relationship


    return context


# ==========================================
# 7. Test Hybrid Search
# ==========================================

if __name__ == "__main__":

    question = "Who works on Project Alpha?"

    context = hybrid_search(
        question
    )

    print()
    print("=" * 60)
    print("🧠 COMBINED HYBRID CONTEXT")
    print("=" * 60)
    print()

    print(context)