import ollama

from hybrid_search import hybrid_search


def generate_answer(question):

    print("🔍 Getting hybrid context...")

    context = hybrid_search(question)

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer the user's question using ONLY the
information provided in the context.

If the answer is not available in the context,
say:

"I could not find this information
in the company documents."

Be clear and concise.

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