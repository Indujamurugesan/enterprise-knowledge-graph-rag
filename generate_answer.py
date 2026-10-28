
import ollama

from hybrid_search import hybrid_search


def generate_answer(question):

    print("🔍 Getting hybrid context...")

    context = hybrid_search(question)

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer the question using the provided context.

Important rules:
1. Read all the document context carefully.
2. If the answer appears anywhere in the context,
   give that answer directly.
3. Combine relevant facts from document and graph context.
4. Do not say information is missing if it is present.
5. If the answer is genuinely absent, say:
   "I could not find this information in the company documents."

USER QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

    print()
    print("🤖 Generating answer...")

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":

    question = "Who works on Project Alpha?"

    answer = generate_answer(question)

    print()
    print("=" * 60)
    print("💬 AI ANSWER")
    print("=" * 60)
    print()

    print(answer)
