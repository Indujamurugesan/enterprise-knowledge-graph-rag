import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# -----------------------------
# Read document
# -----------------------------

file_path = Path("data/sample_company.txt")

text = file_path.read_text(
    encoding="utf-8"
)


# -----------------------------
# Split document
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)


# -----------------------------
# Store chunks in Neo4j
# -----------------------------

def create_chunk(tx, chunk_id, text):

    query = """
    MERGE (c:DocumentChunk {
        chunk_id: $chunk_id
    })

    SET c.text = $text,
        c.source = "sample_company.txt"

    RETURN c.chunk_id AS chunk_id
    """

    result = tx.run(
        query,
        chunk_id=chunk_id,
        text=text
    )

    return result.single()["chunk_id"]


try:

    with driver.session() as session:

        for index, chunk in enumerate(chunks):

            chunk_id = f"sample_company_{index}"

            session.execute_write(
                create_chunk,
                chunk_id,
                chunk
            )

            print(
                f"✅ Stored chunk {index + 1}/{len(chunks)}"
            )


finally:

    driver.close()


print()
print("🎉 All document chunks stored in Neo4j!")