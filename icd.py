from processing.normalization import normalize_diagnosis, clean_diagnosis_text
from icd_engine import match_icd, normalize_medical_term


def enrich_with_icd(data: dict) -> list:

    enriched = []
    seen = set()

    for d in data.get("diagnosen", []):

        raw = d.get("diagnose", "")

        if not raw:
            continue

        cleaned = clean_diagnosis_text(raw)

        norm = normalize_diagnosis(cleaned)
        norm = normalize_medical_term(norm)

        key = norm.lower().strip()

        if key in seen:
            continue

        seen.add(key)

        print(f"\nRAW:  {raw}")
        print(f"NORM: {norm}")

        result = match_icd(norm)

        if result is None:
            icd = None
            confidence = 0.0
        else:
            icd = result["code"]
            confidence = result["confidence"]

        print(
            f"ICD:  {icd} ({confidence:.2f})"
        )

        if icd is None:
            continue

        enriched.append({
            "diagnose_raw": raw,
            "diagnose_normalized": norm,
            "icd10": icd,
            "confidence": round(confidence, 2)
        })

    return enriched
