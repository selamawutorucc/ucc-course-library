
import csv
from pathlib import Path

inventory = Path(
    r"C:\Users\FM Selasie\Documents\ucc-processing-output\inventory.csv"
)

if not inventory.exists():
    print("ERROR: inventory.csv was not found.")
else:
    with inventory.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        print("Column headings:", reader.fieldnames)
        print("\nFirst 5 sample rows:\n")

        shown = 0

        for row in reader:
            filename = str(row.get("file", ""))

            # Do not display the password file's row.
            if "password.txt" in filename.lower():
                continue

            print(row)
            shown += 1

            if shown == 5:
                break

        if shown == 0:
            print("No sample rows were found.")

