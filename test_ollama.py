import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one short sentence."
        }
    ]
)

print("✅ Ollama is working!")
print()
print(response["message"]["content"])