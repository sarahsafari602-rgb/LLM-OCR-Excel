from ocr import run_ocr
from llm import extract_medical_data
from icd import enrich_with_icd
from excel_export import export_excel
from processing.document_parser import parse_document


def run_pipeline(path: str):

    print("\n[2] OCR...")
    ocr_result = run_ocr(path)

    ocr_text = ocr_result.get("raw_text", "") if isinstance(ocr_result, dict) else ocr_result

    print("\n[3] Document Parsing...")
    meta = parse_document(ocr_text)

    print("\n[4] LLM Extraction...")
    data = extract_medical_data(ocr_text)

    data.update(meta)

    # Fallback: wenn Parser keinen Zeitraum findet,
    # aber LLM ein Behandlungsdatum erkannt hat
    if (
            data.get("behandlungszeitraum", {}).get("start") is None
            and data.get("behandlungsdatum")
    ):
        data["behandlungszeitraum"] = {
            "start": data["behandlungsdatum"],
            "ende": None
        }

    print("\n[5] ICD Matching...")
    enriched = enrich_with_icd(data)

    print("\n[6] Excel Export...")
    export_excel(data, enriched)

    return {
        "ocr_text": ocr_text,
        "structured_data": data,
        "icd_enriched": enriched
    }
