import sqlite3
import csv
import re


DB_PATH = "database/icd.db"
OUTPUT = "data/medical_synonyms.tsv"


def normalize_variant(text):
    """
    Erzeugt einfache Schreibvarianten
    """

    variants = set()

    text = text.lower().strip()

    variants.add(text)

    # Leerzeichen entfernen
    variants.add(text.replace(" ", ""))

    # ae/oe/ue Varianten
    variants.add(
        text.replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
        )

    # deutsche Umschreibung zurück
    variants.add(
        text.replace("ae", "ä")
            .replace("oe", "ö")
            .replace("ue", "ü")
    )

    # Bindestriche entfernen
    variants.add(text.replace("-", " "))

    # Mehrfachleerzeichen
    variants.add(
        re.sub(r"\s+", " ", text)
    )

    return variants


def generate_synonyms():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT code, term
        FROM icd_terms
        WHERE term IS NOT NULL
    """)

    rows = cursor.fetchall()

    synonyms = []


    for code, term in rows:

        for variant in normalize_variant(term):

            if variant != term.lower():

                synonyms.append(
                    [
                        variant,
                        term.lower(),
                        code
                    ]
                )


    conn.close()


    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.writer(
            f,
            delimiter="\t"
        )

        writer.writerow(
            [
                "synonym",
                "target",
                "icd"
            ]
        )

        writer.writerows(
            synonyms
        )


    print(
        f"Synonyme erzeugt: {len(synonyms)}"
    )


if __name__ == "__main__":
    generate_synonyms()
