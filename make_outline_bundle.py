
from pathlib import Path

# Folder containing the extracted lecture text
source_folder = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output\extracted_text"
)

# Where the combined outline document will be saved
output_file = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output\course_outlines_bundle.txt"
)

# Search filenames for these words
keywords = [
    "course description",
    "course outline",
    "course_outline",
    "syllabus",
    "scheme of work",
    "csc101 intro",
]

if not source_folder.exists():
    print("ERROR: The extracted_text folder was not found.")
else:
    matches = [
        file for file in source_folder.rglob("*.txt")
        if any(word in file.name.lower() for word in keywords)
        and file.resolve() != output_file.resolve()
    ]

    matches.sort()

    with output_file.open("w", encoding="utf-8") as bundle:
        bundle.write("UCC LEVEL 100 COURSE OUTLINES\n")
        bundle.write("=" * 60 + "\n\n")

        for number, file in enumerate(matches, start=1):
            bundle.write("\n\n")
            bundle.write("=" * 60 + "\n")
            bundle.write(f"DOCUMENT {number}: {file.name}\n")
            bundle.write("=" * 60 + "\n\n")

            try:
                content = file.read_text(
                    encoding="utf-8", errors="replace"
                )
                bundle.write(content)
                bundle.write("\n")
            except OSError as error:
                bundle.write(f"Could not read this file: {error}\n")

    print("OUTLINE BUNDLE CREATED")
    print(f"Documents included: {len(matches)}")
    print(f"Saved to: {output_file}")
