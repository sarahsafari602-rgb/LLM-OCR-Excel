import cv2


def preprocess_image(image_path: str):
    """
    Verbessert die Bildqualität für die OCR.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Bild konnte nicht geladen werden: {image_path}")

    # Graustufen
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # leichtes Entrauschen
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Histogramm ausgleichen
    gray = cv2.equalizeHist(gray)

    # Adaptive Binarisierung
    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    return processed
