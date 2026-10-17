import os
import certifi
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from processing.pipeline import run_pipeline

os.environ["SSL_CERT_FILE"] = certifi.where()


def select_image():
    Tk().withdraw()
    return askopenfilename(
        title="Arztbrief auswählen",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.tiff")]
    )


def main():
    print("\n[1] Datei auswählen...")
    path = select_image()

    if not path:
        print("Keine Datei gewählt.")
        return

    result = run_pipeline(path)

    print("\n--- RESULT ---\n")
    print(result)


if __name__ == "__main__":
    main()
