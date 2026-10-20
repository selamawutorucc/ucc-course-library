
from pathlib import Path

source = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output\extracted_text"
)
output = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output"
) / "CSC101_chapters"

output.mkdir(parents=True, exist_ok=True)

for number in range(1, 6):
    matches = [
        p for p in source.glob("*.txt")
        if "CSC101" in p.name.upper()
        and f"CHAPTER {number}" in p.name.upper()
    ]

    destination = output / f"CSC101_CHAPTER_{number}.txt"

    with destination.open("w", encoding="utf-8") as result:
        for file in matches:
            result.write(f"SOURCE FILE: {file.name}\n\n")
            result.write(
                file.read_text(encoding="utf-8", errors="replace")
            )
            result.write("\n\n")

    print(
        f"Chapter {number}: {len(matches)} matching file(s) "
        f"-> {destination.name}"
    )

print(f"\nFiles saved in: {output}")
