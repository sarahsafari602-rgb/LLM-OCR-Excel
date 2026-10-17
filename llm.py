import json
import re
import ollama


# ============================================================
# SAFE JSON PARSER
# ============================================================

def safe_json_parse(text: str) -> dict:

    text = text.replace("```json", "")
    text = text.replace("```", "")

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            f"No JSON found:\n{text}"
        )

    return json.loads(
        match.group(0)
    )


# ============================================================
# LLM EXTRACTION
# ============================================================

def extract_medical_data(ocr_text: str) -> dict:

    prompt = f"""
Du bist ein medizinisches Extraktionssystem.

Du erhältst OCR-Text aus einem medizinischen Dokument.

Deine Aufgabe ist es, strukturierte Informationen aus dem Dokument
zu extrahieren.

============================================================
PATIENTENIDENTIFIKATION
============================================================

Extrahiere den Namen und das Geburtsdatum der behandelten Person.

WICHTIG:

Der Patientenname darf NICHT einfach der erste Personenname sein,
der im Dokument vorkommt.

Ein medizinischer Brief kann mehrere Personen enthalten, zum Beispiel:

- Patient oder Patientin
- behandelnder Arzt
- Hausarzt
- überweisender Arzt
- Empfänger des Briefes
- Angehörige
- sonstige Personen

Du musst deshalb anhand des KONTEXTS bestimmen, welcher Name zum
Patienten gehört.

Besonders starke Hinweise sind:

- "Patient"
- "Patientin"
- "Patientenname"
- "Name"
- "Frau" oder "Herr" direkt im Patienten-Kontext
- "geb."
- "geboren"
- "Geburtsdatum"
- Fallnummer oder andere Patientenstammdaten in unmittelbarer Nähe
- Formulierungen wie "wir berichten über ... Patient(in)"
- ein Name in unmittelbarer Nähe des Geburtsdatums

Ignoriere Namen von Ärzten oder Empfängern.

Beispiel:

"Sehr geehrte Frau Dr. Müller"

bedeutet NICHT, dass Müller der Patientenname ist.

Wenn im Briefkopf eine Arztadresse oder Empfängeradresse steht,
darf diese Person NICHT als Patient übernommen werden.

Wenn Name und Geburtsdatum in einem gemeinsamen Patientenblock
stehen, ist dieser Block besonders wichtig.

Wenn der Name aufgrund von OCR-Fehlern beschädigt ist, darfst du
offensichtliche OCR-Fehler korrigieren.

Beispiel:

"Sarah Kassel" kann auch als "Sarah KasseI" oder ähnlich erkannt
worden sein.

Du darfst jedoch KEINEN Nachnamen erfinden.

Wenn nur ein Vorname oder nur ein Nachname sicher erkannt wurde,
gib nur diesen tatsächlich erkannten Namen zurück.

Wenn der Patientenname nicht eindeutig bestimmbar ist, gib
für "name" einen leeren String zurück.

============================================================
GEBURTSDATUM
============================================================

Extrahiere das Geburtsdatum der Patientin bzw. des Patienten.

Achte insbesondere auf:

- "geb."
- "geb.:"
- "geboren"
- "Geburtsdatum"

Das Datum kann beispielsweise folgende Formen haben:

27.03.1999
27,03,1999
27/03/1999
1999-03-27

Normalisiere das Datum auf:

TT.MM.JJJJ

Wenn das Geburtsdatum nicht eindeutig erkennbar ist,
gib einen leeren String zurück.

Verwechsle das Geburtsdatum NICHT mit:

- Behandlungsdatum
- Aufnahmedatum
- Entlassungsdatum
- Briefdatum
- Geburtsdaten anderer Personen

============================================================
BEHANDLUNGSDATUM
============================================================

Extrahiere das Datum, an dem die Behandlung begonnen hat.

Besonders relevant sind Formulierungen wie:

- "Behandlung ab"
- "ab dem"
- "Aufnahme"
- "aufgenommen am"
- "stationäre Aufnahme"

Wenn ein Behandlungsbeginn vorhanden ist, gib ihn als
TT.MM.JJJJ zurück.

============================================================
DIAGNOSEN
============================================================

Extrahiere alle sichtbaren medizinischen Diagnosen.

Achte insbesondere auf Abschnitte wie:

- Diagnosen
- Aktuelle Diagnosen
- Abschlussdiagnose
- Abschlussdiagnosen
- Vorerkrankungen
- Nebendiagnosen
- Hauptdiagnose

Erlaube Tippfehler und OCR-Fehler.

Korrigiere nur offensichtliche OCR-Fehler.

Beispiel:

"Depressicnen" → "Depressionen"

Extrahiere mehrere Diagnosen, wenn vorhanden.

Keine Diagnose erfinden.

============================================================
WICHTIG
============================================================

Nutze ausschließlich Informationen aus dem gegebenen OCR-Text.

Keine medizinischen Informationen ergänzen.

Keine Personen erfinden.

Keine ICD-Codes selbst bestimmen.

============================================================
OUTPUT
============================================================

Gib ausschließlich valides JSON zurück:

{{
    "name": "",
    "geburtsdatum": "",
    "behandlungsdatum": "",
    "diagnosen": [
        {{
            "diagnose": "..."
        }}
    ]
}}

TEXT:

{ocr_text}
"""


    response = ollama.chat(
        model="llama3.1",
        format="json",
        messages=[
            {
                "role": "system",
                "content": (
                    "Du extrahierst medizinische Informationen "
                    "aus OCR-Text. "
                    "Du unterscheidest sorgfältig zwischen "
                    "Patienten, Ärzten und anderen Personen. "
                    "Du erfindest niemals fehlende Informationen."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return safe_json_parse(
        response["message"]["content"]
    )
