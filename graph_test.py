import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def create_graph(tx):

    query = """
    MERGE (p:Person {name: "Ananya"})
    MERGE (project:Project {name: "Project Alpha"})

    MERGE (p)-[:WORKS_ON]->(project)

    RETURN p.name AS person,
           project.name AS project
    """

    result = tx.run(query)

    return result.single()


try:

    with driver.session() as session:

        result = session.execute_write(
            create_graph
        )

        print(
            f"✅ {result['person']} "
            f"WORKS_ON {result['project']}"
        )

finally:

    driver.close()