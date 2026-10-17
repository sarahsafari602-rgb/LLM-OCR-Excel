import re

def normalize_diagnosis(text):

    text = text.lower()

    # OCR-Reste entfernen
    text = re.sub(r"[^\w\säöüß\-]", "", text)

    # Mehrfach-Leerzeichen
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def clean_diagnosis_text(text):

    if not text:
        return ""


    # ICD-Code am Anfang entfernen
    text = re.sub(
        r'^[A-Z]\d{2}(?:[.,]\d+)?\s*',
        '',
        text
    )


    # Inhalte in eckigen Klammern entfernen
    text = re.sub(
        r'\[[^\]]*\]',
        '',
        text
    )


    # ICD-10 Angaben entfernen
    text = re.sub(
        r'\(ICD[- ]?10[^)]*\)',
        '',
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r'\b(v\.?\s*a\.?|verdacht auf)\b',
        '',
        text,
        flags=re.IGNORECASE
    )


    # Beschreibung nach Doppelpunkt entfernen
    text = text.split(":")[0]


    return re.sub(r'\s+', ' ', text).strip()
