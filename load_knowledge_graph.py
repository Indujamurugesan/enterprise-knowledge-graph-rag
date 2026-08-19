import json
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


# -----------------------------
# Create entity
# -----------------------------

def create_entity(tx, name, entity_type):

    query = """
    MERGE (e:Entity {
        name: $name,
        type: $entity_type
    })

    RETURN e.name AS name
    """

    result = tx.run(
        query,
        name=name,
        entity_type=entity_type
    )

    return result.single()["name"]


# -----------------------------
# Create relationship
# -----------------------------

def create_relationship(
    tx,
    source,
    relationship,
    target
):

    query = """
    MATCH (a:Entity {name: $source})
    MATCH (b:Entity {name: $target})

    MERGE (a)-[r:RELATED {
        type: $relationship
    }]->(b)

    RETURN a.name AS source,
           b.name AS target
    """

    result = tx.run(
        query,
        source=source,
        relationship=relationship,
        target=target
    )

    return result.single()


# -----------------------------
# Load JSON
# -----------------------------

with open(
    "data/extracted_knowledge.json",
    "r",
    encoding="utf-8"
) as file:

    knowledge = json.load(file)


try:

    with driver.session() as session:

        entity_count = 0
        relationship_count = 0


        # -------------------------
        # Entities
        # -------------------------

        for chunk in knowledge:

            for entity in chunk.get(
                "entities",
                []
            ):

                session.execute_write(
                    create_entity,
                    entity["name"],
                    entity["type"]
                )

                entity_count += 1


        # -------------------------
        # Relationships
        # -------------------------

        for chunk in knowledge:

            for relation in chunk.get(
                "relationships",
                []
            ):

                result = session.execute_write(
                    create_relationship,
                    relation["source"],
                    relation["relationship"],
                    relation["target"]
                )

                if result:
                    relationship_count += 1


finally:

    driver.close()


print()
print("🎉 Knowledge Graph loaded!")
print(
    f"Entities processed: {entity_count}"
)
print(
    f"Relationships processed: "
    f"{relationship_count}"
)