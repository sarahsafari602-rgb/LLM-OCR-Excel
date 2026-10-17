import csv
from pathlib import Path
from rapidfuzz import process, fuzz


BASE_DIR = Path(__file__).resolve().parent.parent

OCR_FILE = BASE_DIR / "data" / "ocr_corrections.tsv"


def load_ocr_corrections():

    corrections = {}

    with open(
        OCR_FILE,
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(
            f,
            delimiter="\t"
        )

        for row in reader:

            corrections[
                row["ocr_term"].lower()
            ] = row["normalized_term"]


    print(
        f"OCR-Korrekturen geladen: {len(corrections)}"
    )

    return corrections



OCR_CORRECTIONS = load_ocr_corrections()



def correct_diagnosis(text):

    key = text.lower().strip()


    # exakter OCR-Fehler
    if key in OCR_CORRECTIONS:
        return OCR_CORRECTIONS[key]


    # fuzzy Suche
    result = process.extractOne(
        key,
        OCR_CORRECTIONS.keys(),
        scorer=fuzz.WRatio
    )


    if result:

        match, score, _ = result

        if score >= 85:
            return OCR_CORRECTIONS[match]


    return text
