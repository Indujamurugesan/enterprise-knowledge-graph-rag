import json
from pathlib import Path

import ollama

from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_knowledge(text):

    prompt = f"""
You are a Knowledge Graph extraction system.

Extract entities and relationships from the company text.

Allowed entity types:

Person
Project
Department
Product
Process
Technology
Organization
Document

Allowed relationships:

WORKS_ON
MANAGES
BELONGS_TO
DEVELOPS
USES
PART_OF
CREATED_BY
REPORTS_TO
DEPENDS_ON

Return ONLY valid JSON.

Format:

{{
    "entities": [
        {{
            "name": "Entity Name",
            "type": "Person"
        }}
    ],
    "relationships": [
        {{
            "source": "Entity A",
            "relationship": "WORKS_ON",
            "target": "Entity B"
        }}
    ]
}}

COMPANY TEXT:

{text}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"]

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)


# --------------------------------
# Read company document
# --------------------------------

file_path = Path("data/sample_company.txt")

text = file_path.read_text(
    encoding="utf-8"
)


# --------------------------------
# Split document
# --------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)


# --------------------------------
# Extract knowledge from chunks
# --------------------------------

all_results = []


for index, chunk in enumerate(chunks):

    print(
        f"🔍 Processing chunk "
        f"{index + 1}/{len(chunks)}..."
    )

    try:

        data = extract_knowledge(chunk)

        all_results.append(data)

        print("   ✅ Extracted successfully")

    except Exception as e:

        print(
            f"   ❌ Error in chunk {index + 1}: {e}"
        )


# --------------------------------
# Save extracted knowledge
# --------------------------------

output_file = Path(
    "data/extracted_knowledge.json"
)

output_file.write_text(
    json.dumps(
        all_results,
        indent=4
    ),
    encoding="utf-8"
)


print()
print("🎉 Knowledge extraction completed!")
print(
    f"📁 Saved to: {output_file}"
)