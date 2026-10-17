import re


def extract_diagnoses(raw_text: str):

    diagnoses = []

    for line in raw_text.splitlines():

        line = line.strip()

        if not line:
            continue

        # sehr kurze Zeilen ignorieren
        if len(line) < 5:
            continue

        # Seitenköpfe usw. ignorieren
        if re.search(r"\d{2}\.\d{2}\.\d{4}", line):
            continue

        diagnoses.append(line)

    return diagnoses
