import sqlite3


DB_PATH = "database/icd.db"


def load_icd_entries():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT code, label
        FROM icd
    """)

    rows = cursor.fetchall()

    connection.close()

    catalog = []

    for code, label in rows:

        catalog.append({
            "code": code,
            "label": label,
            "synonyms": []
        })

    return catalog
