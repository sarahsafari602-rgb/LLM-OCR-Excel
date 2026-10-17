import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "database" / "icd.db"

SYNONYM_FILE = BASE_DIR / "data" / "medical_synonyms.tsv"



def load_icd_catalog():

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            code,
            term,
            rubric
        FROM icd_terms
    """)


    rows = cursor.fetchall()


    catalog = {}


    for row in rows:

        code = row["code"]


        if code not in catalog:

            catalog[code] = {

                "code": code,

                "label": row["term"],

                "synonyms": [],

                "rubrics": []

            }


        else:

            if row["term"] != catalog[code]["label"]:

                catalog[code]["synonyms"].append(
                    row["term"]
                )


    connection.close()


    return list(catalog.values())





def load_medical_synonyms(
        path=None
):

    if path is None:

        path = SYNONYM_FILE



    synonyms = {}



    with open(
        path,
        encoding="utf-8"
    ) as f:


        reader = csv.DictReader(
            f,
            delimiter="\t"
        )



        for row in reader:


            synonym = row.get("synonym", "")
            target = row.get("target", "")
            code = row.get("icd", "")



            if synonym and target:


                synonyms[
                    synonym.lower().strip()
                ] = {


                    "target": target.strip(),

                    "icd": code.strip()

                }



    print(
        f"Medizinische Synonyme geladen: {len(synonyms)}"
    )


    return synonyms





def load_medical_vocabulary():


    vocabulary = []


    synonyms = load_medical_synonyms()



    for term, data in synonyms.items():


        vocabulary.append({

            "term": term,

            "synonyms": data

        })



    return vocabulary





if __name__ == "__main__":


    syn = load_medical_synonyms()


    print(
        list(syn.items())[:10]
    )
