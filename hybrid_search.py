
import os
import chromadb
from dotenv import load_dotenv
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="company_documents"
)

# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Vector Search
def vector_search(question):
    if collection.count() == 0:
        print("ChromaDB has no documents.")
        return []

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(3, collection.count())
    )

    return results.get("documents", [[]])[0]


# Graph Search
def graph_search(question):
    if not URI or not USERNAME or not PASSWORD:
        print("Neo4j settings missing. Check your .env file.")
        return []

    keywords = [
        word.strip("?!.,:;")
        for word in question.split()
        if len(word.strip("?!.,:;")) > 3
    ]

    if not keywords:
        return []

    cypher = """
    MATCH (a:Entity)-[r:RELATED]->(b:Entity)
    WHERE any(keyword IN $keywords
        WHERE toLower(a.name) CONTAINS toLower(keyword)
           OR toLower(b.name) CONTAINS toLower(keyword))
    RETURN a.name AS source,
           r.type AS relationship,
           b.name AS target
    LIMIT 20
    """

    relationships = []
    driver = None

    try:
        driver = GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD)
        )

        driver.verify_connectivity()

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

    except Exception as error:
        print("Neo4j error:", error)

    finally:
        if driver is not None:
            driver.close()

    return relationships


# Hybrid Search
def hybrid_search(question):
    print("Searching vector database...")

    try:
        vector_results = vector_search(question)
        print(f"Found {len(vector_results)} document chunks")
    except Exception as error:
        print("Vector search error:", error)
        vector_results = []

    print("\nSearching knowledge graph...")

    graph_results = graph_search(question)
    print(f"Found {len(graph_results)} relationships")

    context_parts = []

    if vector_results:
        context_parts.append("DOCUMENT CONTEXT:")
        context_parts.extend(vector_results)

    if graph_results:
        context_parts.append("\nGRAPH CONTEXT:")
        context_parts.extend(graph_results)

    if not context_parts:
        return "No relevant information found in the databases."

    return "\n".join(context_parts)


# Test the search
if __name__ == "__main__":
    question = "Who is the project manager of Project Alpha?"

    context = hybrid_search(question)

    print("\n" + "=" * 50)
    print("HYBRID SEARCH RESULT")
    print("=" * 50)
    print(context)
