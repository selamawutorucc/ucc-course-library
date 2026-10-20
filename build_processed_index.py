
import csv
import json
import shutil
from pathlib import Path, PurePosixPath
from collections import Counter

REPO = Path(
    r"C:\Users\FM Selasie\Documents\GitHub\ucc-course-library"
)
OUTPUT = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output"
)
INVENTORY = OUTPUT / "inventory.csv"
EXTRACTED = OUTPUT / "extracted_text"

PROCESSED = REPO / "processed-content"
TEXT_DESTINATION = PROCESSED / "extracted_text"
INDEX = PROCESSED / "index.csv"
SUMMARY = PROCESSED / "processing_summary.json"

if not INVENTORY.exists():
    raise FileNotFoundError(f"Inventory not found: {INVENTORY}")

if not EXTRACTED.exists():
    raise FileNotFoundError(f"Extracted-text folder not found: {EXTRACTED}")

PROCESSED.mkdir(parents=True, exist_ok=True)
TEXT_DESTINATION.mkdir(parents=True, exist_ok=True)

index_rows = []
counts = Counter()
copied = 0
missing = 0
empty = 0
skipped_sensitive = 0

with INVENTORY.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    required = {"file", "type", "status"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError(
            "Unexpected inventory columns. Found: "
            + str(reader.fieldnames)
        )

    for row in reader:
        original = (row.get("file") or "").strip()
        file_type = (row.get("type") or "").strip()
        extraction_status = (row.get("status") or "").strip()

        # Never process or copy the password file.
        if PurePosixPath(original.replace("\\", "/")).name.lower() == "password.txt":
            skipped_sensitive += 1
            continue

        if not original:
            continue

        # Recreate the extractor's flattened output filename.
        flattened_name = original.replace("\\", "_").replace("/", "_") + ".txt"
        extracted_file = EXTRACTED / flattened_name

        text_path = ""
        character_count = 0
        text_status = "MISSING"
        review_status = "NOT_REVIEWED"
        note = ""

        if extracted_file.is_file():
            try:
                text = extracted_file.read_text(
                    encoding="utf-8", errors="replace"
                )
                character_count = len(text)
                text_status = "EXTRACTED_TEXT_FOUND"

                if character_count == 0 or not text.strip():
                    text_status = "EMPTY_TEXT"
                    review_status = "NEEDS_INSPECTION"
                    note = "No readable text; check whether scanned or empty."
                    empty += 1
                else:
                    # Preserve the original relative folder structure.
                    relative = PurePosixPath(
                        original.replace("\\", "/")
                    )

                    if relative.is_absolute() or ".." in relative.parts:
                        text_status = "UNSAFE_PATH"
                        review_status = "NEEDS_INSPECTION"
                        note = "Unusual path; text was not copied."
                    else:
                        destination = TEXT_DESTINATION.joinpath(
                            *relative.parts
                        )
                        destination = Path(str(destination) + ".txt")
                        destination.parent.mkdir(
                            parents=True, exist_ok=True
                        )
                        shutil.copy2(extracted_file, destination)

                        text_path = destination.relative_to(
                            PROCESSED
                        ).as_posix()
                        copied += 1

                        if character_count < 100:
                            review_status = "NEEDS_INSPECTION"
                            note = (
                                "Very little text; verify completeness."
                            )
                        else:
                            review_status = "NOT_REVIEWED"

            except OSError as error:
                text_status = "READ_ERROR"
                review_status = "NEEDS_INSPECTION"
                note = f"Could not read or copy text: {error}"
        else:
            missing += 1
            review_status = "NEEDS_PROCESSING"
            note = (
                "No matching extracted text file; investigate "
                "conversion, OCR, or unsupported format."
            )

        index_rows.append({
            "original_file": original,
            "file_type": file_type,
            "extraction_status": extraction_status,
            "text_status": text_status,
            "extracted_text_path": text_path,
            "character_count": character_count,
            "review_status": review_status,
            "notes": note,
        })

        counts[text_status] += 1

columns = [
    "original_file",
    "file_type",
    "extraction_status",
    "text_status",
    "extracted_text_path",
    "character_count",
    "review_status",
    "notes",
]

with INDEX.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(index_rows)

summary = {
    "inventory": str(INVENTORY),
    "indexed_records": len(index_rows),
    "text_files_copied": copied,
    "missing_extracted_text": missing,
    "empty_text_files": empty,
    "sensitive_files_skipped": skipped_sensitive,
    "text_status_counts": dict(counts),
    "index_file": str(INDEX),
    "text_folder": str(TEXT_DESTINATION),
    "note": (
        "Text extraction does not mean a document has been fully "
        "read or reviewed. Verify scanned pages, tables, images, "
        "and short or missing text."
    ),
}

SUMMARY.write_text(
    json.dumps(summary, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

readme = """# UCC Processed Content

This folder contains extracted text and a searchable inventory.

- `index.csv` maps original repository paths to extracted text.
- `extracted_text/` preserves the original folder structure.
- `processing_summary.json` records the indexing results.

`NOT_REVIEWED` means the text has not yet been fully checked.
Missing or short text may require conversion, OCR, or manual review.

Original course files remain in their original locations.
Sensitive password files are excluded from this process.
"""

(PROCESSED / "README.md").write_text(readme, encoding="utf-8")

print("INDEX BUILD COMPLETE")
print("-" * 40)
print("Records indexed:", len(index_rows))
print("Text files copied:", copied)
print("Missing extracted text:", missing)
print("Empty text files:", empty)
print("Sensitive files skipped:", skipped_sensitive)
print("\nIndex saved to:", INDEX)
print("Summary saved to:", SUMMARY)

