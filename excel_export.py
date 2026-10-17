import pandas as pd
from datetime import datetime


def format_filename_date(date_value):

    if not date_value:
        return None

    date_value = str(date_value).strip()

    # Bereits deutsches Format: 20.06.2025
    try:
        return datetime.strptime(
            date_value,
            "%d.%m.%Y"
        ).strftime("%d.%m.%Y")
    except ValueError:
        pass

    # ISO-Format: 2025-06-20
    try:
        return datetime.strptime(
            date_value,
            "%Y-%m-%d"
        ).strftime("%d.%m.%Y")
    except ValueError:
        pass

    # ISO-Format mit Uhrzeit:
    # 2025-06-20T00:00:00
    try:
        return datetime.fromisoformat(
            date_value
        ).strftime("%d.%m.%Y")
    except ValueError:
        pass

    # Falls ein anderes Format vorliegt,
    # versuchen wir pandas
    try:
        parsed = pd.to_datetime(
            date_value,
            dayfirst=True,
            errors="coerce"
        )

        if not pd.isna(parsed):
            return parsed.strftime("%d.%m.%Y")

    except Exception:
        pass

    # Wenn nichts funktioniert, ursprünglichen Wert behalten
    return date_value


def build_filename(data):

    name = data.get("name")

    if not name or not isinstance(name, str):
        name = "unknown_patient"

    name = name.strip().replace(" ", "_")

    if not name:
        name = "unknown_patient"


    # Immer das START-Datum des Behandlungszeitraums verwenden
    period = data.get("behandlungszeitraum")

    treatment_date = None

    if isinstance(period, dict):
        treatment_date = period.get("start")


    if treatment_date:

        treatment_date = format_filename_date(
            treatment_date
        )

        return f"{name}_{treatment_date}_Arztbrief.xlsx"


    # Fallback, falls kein Startdatum vorhanden ist
    return f"{name}_Arztbrief.xlsx"


def format_treatment_period(period):

    if not period or not isinstance(period, dict):
        return None

    start = period.get("start")
    ende = period.get("ende")

    if start and ende:
        return f"{start} - {ende}"

    if start:
        return start

    return None


def export_excel(data: dict, enriched: list):

    filename = build_filename(data)

    rows = []
    seen = set()


    for d in enriched:

        key = d["diagnose_normalized"].lower().strip()

        if key in seen:
            continue

        seen.add(key)

        confidence = d["confidence"]


        if confidence >= 0.90:
            status = "HIGH"

        elif confidence >= 0.75:
            status = "MEDIUM"

        else:
            status = "LOW"


        rows.append({

            "Name": data.get("name"),

            "Geburtsdatum": data.get("geburtsdatum"),

            "Behandlungszeitraum": format_treatment_period(
                data.get("behandlungszeitraum")
            ),

            "Diagnose (normalisiert)": d["diagnose_normalized"],

            "Diagnose (roh)": d["diagnose_raw"],

            "ICD-10": d["icd10"],

            "Confidence": confidence,

            "Status": status

        })


    df = pd.DataFrame(rows)


    if df.empty:

        print("⚠️ Keine ICD-Daten zum Export vorhanden.")

        return


    df = df.sort_values(
        by="Confidence",
        ascending=False
    )


    df.to_excel(
        filename,
        index=False
    )


    print(f"\nExcel gespeichert: {filename}")
