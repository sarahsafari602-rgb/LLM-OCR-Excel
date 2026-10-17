from rapidfuzz import process, fuzz

from icd_loader import (
    load_icd_catalog,
    load_medical_synonyms
)


# ---------------------------------------------------
# Daten laden
# ---------------------------------------------------

ICD_CATALOG = load_icd_catalog()

MEDICAL_SYNONYMS = load_medical_synonyms()



# ---------------------------------------------------
# Normalisierung
# ---------------------------------------------------

def normalize_key(text):

    if not text:
        return ""

    text = text.lower().strip()

    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)


    for char in [
        " ",
        "-",
        "_",
        ".",
        ",",
        ";",
        ":",
        "(",
        ")",
        "[",
        "]",
        "/"
    ]:
        text = text.replace(char, "")


    return text



# ---------------------------------------------------
# Suchindex
# ---------------------------------------------------

SYNONYM_INDEX = {
    normalize_key(key): value
    for key, value in MEDICAL_SYNONYMS.items()
}


ICD_INDEX = {
    normalize_key(item["label"]): item
    for item in ICD_CATALOG
}



# ---------------------------------------------------
# ICD Matching
# ---------------------------------------------------

def match_icd(term):

    if not term:
        return None


    key = normalize_key(term)



    # -----------------------------------------------
    # 1. Exakter Treffer
    # -----------------------------------------------

    if key in SYNONYM_INDEX:

        data = SYNONYM_INDEX[key]

        return {
            "label": data["target"],
            "code": data["icd"],
            "confidence": 1.0
        }



    # -----------------------------------------------
    # 2. Fuzzy gegen medizinische Synonyme
    # -----------------------------------------------

    result = process.extractOne(
        key,
        SYNONYM_INDEX.keys(),
        scorer=fuzz.WRatio
    )


    if result:

        match, score, _ = result


        if score >= 85:

            data = SYNONYM_INDEX[match]

            return {
                "label": data["target"],
                "code": data["icd"],
                "confidence": round(score / 100, 2)
            }



    # -----------------------------------------------
    # 3. Fuzzy gegen ICD-Bezeichnungen
    # -----------------------------------------------

    result = process.extractOne(
        key,
        ICD_INDEX.keys(),
        scorer=fuzz.WRatio
    )


    if result:

        match, score, _ = result


        if score >= 90:

            data = ICD_INDEX[match]

            return {
                "label": data["label"],
                "code": data["code"],
                "confidence": round(score / 100, 2)
            }
    return None

def normalize_medical_term(term):

    key = normalize_key(term)

    if key in SYNONYM_INDEX:

        data = SYNONYM_INDEX[key]

        return data["target"]

    # Fuzzy-Suche
    results = process.extract(
        key,
        list(SYNONYM_INDEX.keys()),
        scorer=fuzz.ratio,
        limit=1
    )

    if results:

        best, score, _ = results[0]

        if score >= 85:
            return SYNONYM_INDEX[best]["target"]

    return term
