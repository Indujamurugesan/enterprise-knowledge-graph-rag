import os
import re

from dotenv import load_dotenv
from neo4j import GraphDatabase


# ==========================================
# Load .env file
# ==========================================

load_dotenv()


# ==========================================
# Neo4j Configuration
# ==========================================

NEO4J_URI = os.getenv(
    "NEO4J_URI"
)

NEO4J_USERNAME = os.getenv(
    "NEO4J_USERNAME"
)

NEO4J_PASSWORD = os.getenv(
    "NEO4J_PASSWORD"
)


# ==========================================
# Check Neo4j configuration
# ==========================================

if not NEO4J_URI:
    raise ValueError(
        "❌ NEO4J_URI is missing in .env"
    )

if not NEO4J_USERNAME:
    raise ValueError(
        "❌ NEO4J_USERNAME is missing in .env"
    )

if not NEO4J_PASSWORD:
    raise ValueError(
        "❌ NEO4J_PASSWORD is missing in .env"
    )


# ==========================================
# Extract Entities
# ==========================================

def extract_entities(text):

    entities = []

    # --------------------------------------
    # Person names
    # --------------------------------------

    person_pattern = (
        r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"
    )

    person_matches = re.findall(
        person_pattern,
        text
    )

    for name in person_matches:

        if name not in entities:
            entities.append(name)


    # --------------------------------------
    # Projects
    # --------------------------------------

    project_matches = re.findall(
        r"\bProject [A-Z][a-zA-Z0-9]*\b",
        text
    )

    for project in project_matches:

        if project not in entities:
            entities.append(project)


    # --------------------------------------
    # Technologies
    # --------------------------------------

    technologies = [
        "Python",
        "Neo4j",
        "ChromaDB",
        "OpenAI",
        "Streamlit",
        "Ollama"
    ]

    for technology in technologies:

        if technology.lower() in text.lower():

            if technology not in entities:
                entities.append(technology)


    return entities


# ==========================================
# Extract Relationships
# ==========================================

def extract_relationships(text):

    relationships = []


    # --------------------------------------
    # PERSON WORKS_ON PROJECT
    # --------------------------------------

    works_on_pattern = (
        r"([A-Z][a-z]+ [A-Z][a-z]+)"
        r"\s+works on\s+"
        r"(Project [A-Z][a-zA-Z0-9]*)"
    )

    works_on_matches = re.findall(
        works_on_pattern,
        text,
        re.IGNORECASE
    )

    for person, project in works_on_matches:

        relationships.append({
            "source": person,
            "type": "WORKS_ON",
            "target": project
        })


    # --------------------------------------
    # PROJECT USES TECHNOLOGY
    # --------------------------------------

    uses_pattern = (
        r"(Project [A-Z][a-zA-Z0-9]*)"
        r"\s+uses\s+"
        r"(Python|Neo4j|ChromaDB|OpenAI|Streamlit|Ollama)"
    )

    uses_matches = re.findall(
        uses_pattern,
        text,
        re.IGNORECASE
    )

    for project, technology in uses_matches:

        relationships.append({
            "source": project,
            "type": "USES",
            "target": technology
        })


    return relationships


# ==========================================
# Store Entities & Relationships in Neo4j
# ==========================================

def store_in_neo4j(
    entities,
    relationships
):

    print()
    print("🕸️ Connecting to Neo4j...")


    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(
            NEO4J_USERNAME,
            NEO4J_PASSWORD
        )
    )


    try:

        # Test connection
        driver.verify_connectivity()

        print(
            "✅ Neo4j connection successful"
        )


        with driver.session() as session:

            # ----------------------------------
            # Create Entity nodes
            # ----------------------------------

            for entity in entities:

                session.run(
                    """
                    MERGE (e:Entity {
                        name: $name
                    })
                    """,
                    name=entity
                )


            # ----------------------------------
            # Create Relationships
            # ----------------------------------

            for relationship in relationships:

                session.run(
                    """
                    MATCH (a:Entity {
                        name: $source
                    })

                    MATCH (b:Entity {
                        name: $target
                    })

                    MERGE (a)-[r:RELATED {
                        type: $type
                    }]->(b)
                    """,
                    source=relationship["source"],
                    target=relationship["target"],
                    type=relationship["type"]
                )


        print(
            "✅ Stored entities and relationships in Neo4j"
        )


    finally:

        driver.close()

        print(
            "🔒 Neo4j connection closed"
        )


# ==========================================
# Extract + Store
# ==========================================

def extract_and_store(text):

    print()
    print("=" * 50)
    print("🧠 ENTITY & RELATIONSHIP EXTRACTION")
    print("=" * 50)


    # Extract entities
    entities = extract_entities(
        text
    )


    # Extract relationships
    relationships = extract_relationships(
        text
    )


    print()
    print(
        f"🧠 Found {len(entities)} entities"
    )

    print(
        f"🔗 Found {len(relationships)} relationships"
    )


    # Display entities
    print()
    print("ENTITIES:")

    for entity in entities:

        print(
            f"  • {entity}"
        )


    # Display relationships
    print()
    print("RELATIONSHIPS:")

    for relationship in relationships:

        print(
            f"  • "
            f"{relationship['source']} "
            f"--[{relationship['type']}]--> "
            f"{relationship['target']}"
        )


    # Store in Neo4j
    store_in_neo4j(
        entities,
        relationships
    )


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    test_text = """
    Ananya Sharma works on Project Alpha.

    Rahul Kumar works on Project Beta.

    Rahul Kumar works on Project Alpha.

    Project Alpha uses Python.

    Project Alpha uses Neo4j.

    Project Alpha uses ChromaDB.
    """


    extract_and_store(
        test_text
    )