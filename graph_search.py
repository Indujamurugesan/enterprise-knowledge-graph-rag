import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load .env
load_dotenv()

# Neo4j settings
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


# Connect to Neo4j
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# Search term
search_term = "Project Alpha"


# Cypher query
cypher = """
MATCH (a:Entity)-[r:RELATED]->(b:Entity)
WHERE toLower(a.name) CONTAINS toLower($search_term)
   OR toLower(b.name) CONTAINS toLower($search_term)

RETURN
    a.name AS source,
    r.type AS relationship,
    b.name AS target
LIMIT 20
"""


try:

    with driver.session() as session:

        result = session.run(
            cypher,
            search_term=search_term
        )

        print("🔍 Graph Search:")
        print(f"Query: {search_term}")
        print()

        found = False

        for record in result:

            found = True

            print(
                f"{record['source']} "
                f"--[{record['relationship']}]--> "
                f"{record['target']}"
            )

        if not found:
            print("No relationships found.")


finally:

    driver.close()