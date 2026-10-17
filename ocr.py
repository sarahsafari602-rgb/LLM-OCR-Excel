import easyocr
from preprocessing import preprocess_image

reader = easyocr.Reader(['de'], gpu=False)


def run_ocr(path: str):
    print("OCR INPUT:", path)

    result = reader.readtext(path)

    print("OCR RAW RESULT LENGTH:", len(result))

    raw_text = "\n".join([t[1] for t in result])

    print("\n--- OCR AUSGABE ---")
    print(raw_text)
    print("-------------------\n")

    return {
        "raw_text": raw_text,
        "structured": result
    }
