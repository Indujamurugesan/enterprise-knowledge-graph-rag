from pathlib import Path

file_path = Path("data/sample_company.txt")

text = file_path.read_text(
    encoding="utf-8"
)

print("✅ Document loaded successfully!")
print()
print(text)