
from pathlib import Path

output_folder = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output"
)
extracted_folder = output_folder / "extracted_text"
chapters_folder = output_folder / "CSC101_chapters"

print("EXTRACTED TEXT FOLDER")
print("-" * 40)

if extracted_folder.exists():
    files = sorted(extracted_folder.glob("*.txt"))
    print("Number of extracted text files:", len(files))

    for file in files[:10]:
        print(file.name)
else:
    print("Folder not found:", extracted_folder)

print("\nCSC101 CHAPTER BUNDLE")
print("-" * 40)

if chapters_folder.exists():
    for file in sorted(chapters_folder.glob("*.txt")):
        print(file.name)
else:
    print("Folder not found:", chapters_folder)
