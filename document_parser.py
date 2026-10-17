import re


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def clean_spaces(text):
    """
    Entfernt überflüssige Leerzeichen.
    """
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def normalize_date(date):
    """
    Vereinheitlicht ein Datum auf TT.MM.JJJJ.
    Unterstützt ., , und / als Trennzeichen.
    """

    if not date:
        return None

    date = (
        date
        .replace(",", ".")
        .replace("/", ".")
        .replace("'", ".")
    )

    match = re.search(
        r"(\d{1,2})\.(\d{1,2})\.(\d{2,4})",
        date
    )

    if not match:
        return None

    day = match.group(1).zfill(2)
    month = match.group(2).zfill(2)
    year = match.group(3)

    if len(year) == 2:
        year = "19" + year

    return f"{day}.{month}.{year}"


def is_valid_date(date):
    """
    Prüft grob, ob ein Datum plausibel ist.
    """

    if not date:
        return False

    match = re.match(
        r"^(\d{2})\.(\d{2})\.(\d{4})$",
        date
    )

    if not match:
        return False

    day = int(match.group(1))
    month = int(match.group(2))
    year = int(match.group(3))

    if not 1 <= day <= 31:
        return False

    if not 1 <= month <= 12:
        return False

    if not 1900 <= year <= 2100:
        return False

    return True


def is_plausible_name_part(word):
    """
    Prüft, ob ein Wort grundsätzlich wie ein Name aussehen kann.
    """

    if not word:
        return False

    if not 2 <= len(word) <= 30:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]+",
            word
        )
    )


# ============================================================
# NAME
# ============================================================

def extract_name(text: str):

    if not text:
        return None

    lines = [
        clean_spaces(line)
        for line in text.splitlines()
        if clean_spaces(line)
    ]

    # --------------------------------------------------------
    # 1. SPEZIALFALL:
    #
    # Nachname, Vorname; Geburtsdatum
    #
    # Beispiel:
    #
    # Kassel, Sarah; '27.03.1999,
    #
    # Das ist für die Notaufnahme sehr wichtig.
    # --------------------------------------------------------

    name_date_pattern = re.compile(
        r"^\s*"
        r"([A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30})"
        r"\s*,\s*"
        r"([A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30})"
        r"\s*"
        r"[;,]?"
        r"\s*"
        r"['\"]?"
        r"\d{1,2}[.,/]\d{1,2}[.,/]\d{4}"
        r"\s*[;,]?"
        r"\s*$",
        re.IGNORECASE
    )

    for line in lines:

        match = name_date_pattern.match(line)

        if not match:
            continue

        nachname = match.group(1)
        vorname = match.group(2)

        return f"{vorname} {nachname}"

    # --------------------------------------------------------
    # 2. Variante:
    #
    # Nachname, Vorname; Datum + weitere Informationen
    #
    # Beispiel:
    #
    # Kassel, Sarah; 27.03.1999, 27j
    #
    # Hier darf hinter dem Datum noch weiterer Text stehen.
    # --------------------------------------------------------

    for line in lines:

        match = re.search(
            r"^\s*"
            r"([A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30})"
            r"\s*,\s*"
            r"([A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30})"
            r"\s*"
            r"[;,]?"
            r"\s*"
            r"['\"]?"
            r"\d{1,2}[.,/]\d{1,2}[.,/]\d{4}",
            line,
            re.IGNORECASE
        )

        if match:

            nachname = match.group(1)
            vorname = match.group(2)

            return f"{vorname} {nachname}"

    # --------------------------------------------------------
    # 3. Explizite Patientenangaben
    # --------------------------------------------------------

    explicit_patterns = [

        r"\bPatient(?:en)?name\s*[:\-]\s*"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)"
        r"\s+"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)",

        r"\bPatient(?:in)?\s*[:\-]\s*"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)"
        r"\s+"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)",

        r"\bName\s*[:\-]\s*"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)"
        r"\s+"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)"
    ]

    for pattern in explicit_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return (
                f"{match.group(1)} "
                f"{match.group(2)}"
            )

    # --------------------------------------------------------
    # 4. Patientenblock
    # --------------------------------------------------------

    for i, line in enumerate(lines):

        if re.search(
            r"\b(Patientin|Patient)\b",
            line,
            re.IGNORECASE
        ):

            block = " ".join(
                lines[i:i + 8]
            )

            # Alles nach Geburtsangabe abschneiden
            block = re.split(
                r"\bgeb(?:oren|urtsdatum)?\.?\b",
                block,
                flags=re.IGNORECASE
            )[0]

            block = re.sub(
                r"\b(Patientin|Patient|Frau|Herr)\b",
                " ",
                block,
                flags=re.IGNORECASE
            )

            block = re.sub(
                r"\b\d{1,2}[.,/]\d{1,2}[.,/]\d{2,4}\b",
                " ",
                block
            )

            words = re.findall(
                r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]+",
                block
            )

            forbidden = {
                "patient",
                "patientin",
                "geb",
                "geboren",
                "geburtsdatum",
                "datum",
                "fallnummer",
                "fallnr",
                "behandlung",
                "behandlungsdatum",
                "vorname",
                "nachname"
            }

            words = [
                word
                for word in words
                if word.lower() not in forbidden
            ]

            candidates = [
                word
                for word in words
                if (
                    len(word) >= 2
                    and (
                        word[0].isupper()
                        or word.isupper()
                    )
                )
            ]

            if len(candidates) >= 2:

                return (
                    f"{candidates[0]} "
                    f"{candidates[1]}"
                )

            if len(candidates) == 1:
                return candidates[0]

    # --------------------------------------------------------
    # 5. NOTAUFNAHME-SPEZIALFALL
    #
    # Beispiel:
    #
    # Riepl
    # '27.03.1999
    # Friedenspromenade 85
    #
    # Hier steht nur der Nachname vor dem Geburtsdatum.
    # --------------------------------------------------------

    forbidden_names = {
        "patient",
        "patientin",
        "herr",
        "frau",
        "arztbericht",
        "notaufnahme",
        "vorerkrankungen",
        "diagnosen",
        "behandlung",
        "anamnese",
        "geburtsdatum",
        "münchen",
        "munchen",
        "klinikum",
        "universität",
        "universitaet",
        "arztbrief"
    }

    for i in range(len(lines) - 2):

        name_line = lines[i]
        birth_line = lines[i + 1]
        address_line = lines[i + 2]

        birth_match = re.search(
            r"['\"]?"
            r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{4})",
            birth_line
        )

        if not birth_match:
            continue

        if not re.fullmatch(
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30}",
            name_line
        ):
            continue

        if name_line.lower() in forbidden_names:
            continue

        # Adresse plausibilisieren
        address_match = re.search(
            r"\d+",
            address_line
        )

        if not address_match:
            continue

        return name_line

    # --------------------------------------------------------
    # 6. Name direkt vor einem Datum
    # --------------------------------------------------------

    for i in range(len(lines) - 1):

        name_line = lines[i]
        date_line = lines[i + 1]

        if not re.fullmatch(
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30}",
            name_line
        ):
            continue

        date_match = re.search(
            r"['\"]?"
            r"\d{1,2}[.,/]\d{1,2}[.,/]\d{4}",
            date_line
        )

        if not date_match:
            continue

        if name_line.lower() in forbidden_names:
            continue

        return name_line

    # --------------------------------------------------------
    # 7. Frau/Herr + Vorname + Nachname
    #
    # Nur als letzter Fallback.
    # --------------------------------------------------------

    match = re.search(
        r"\b(Frau|Herr)\s+"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)\s+"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüßÀ-ÿ'-]+)",
        text
    )

    if match:

        return (
            f"{match.group(2)} "
            f"{match.group(3)}"
        )

    return None


# ============================================================
# GEBURTSDATUM
# ============================================================

def extract_birthdate(text: str):

    if not text:
        return None

    # --------------------------------------------------------
    # 1. Explizite Angaben
    # --------------------------------------------------------

    patterns = [

        r"\bgeb\.?\s*(?:am\s*)?"
        r"['\"]?"
        r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{2,4})",

        r"\bgeboren\s*(?:am\s*)?"
        r"['\"]?"
        r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{2,4})",

        r"\bgeb\s*[:\-]\s*"
        r"['\"]?"
        r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{2,4})",

        r"\bgeburtsdatum\s*[:\-]?\s*"
        r"['\"]?"
        r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{2,4})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            date = normalize_date(
                match.group(1)
            )

            if is_valid_date(date):
                return date

    # --------------------------------------------------------
    # 2. NAME + GEBURTSDATUM IN EINER ZEILE
    #
    # Beispiel:
    #
    # Kassel, Sarah; '27.03.1999,
    # --------------------------------------------------------

    lines = [
        clean_spaces(line)
        for line in text.splitlines()
        if clean_spaces(line)
    ]

    for line in lines:

        match = re.search(
            r"\b"
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30}"
            r"\s*,\s*"
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30}"
            r"\s*[;,]?\s*"
            r"['\"]?"
            r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{4})",
            line
        )

        if match:

            date = normalize_date(
                match.group(1)
            )

            if is_valid_date(date):
                return date

    # --------------------------------------------------------
    # 3. NOTAUFNAHME-SPEZIALFALL
    #
    # Beispiel:
    #
    # Riepl
    # '27.03.1999
    # Friedenspromenade 85
    # --------------------------------------------------------

    for i in range(1, len(lines)):

        current_line = lines[i]

        date_match = re.search(
            r"['\"]?"
            r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{4})",
            current_line
        )

        if not date_match:
            continue

        date = normalize_date(
            date_match.group(1)
        )

        if not is_valid_date(date):
            continue

        previous_line = lines[i - 1]

        if re.fullmatch(
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30}",
            previous_line
        ):

            if previous_line.lower() not in forbidden_names:
                return date

    # --------------------------------------------------------
    # 4. Patientenblock ohne Schlüsselwort
    #
    # Name
    # Datum
    # --------------------------------------------------------

    for i in range(len(lines) - 1):

        current = lines[i]
        following = lines[i + 1]

        if not re.fullmatch(
            r"[A-Za-zÄÖÜäöüßÀ-ÿ'-]{2,30}",
            current
        ):
            continue

        match = re.search(
            r"['\"]?"
            r"(\d{1,2}[.,/]\d{1,2}[.,/]\d{4})",
            following
        )

        if match:

            date = normalize_date(
                match.group(1)
            )

            if is_valid_date(date):
                return date

    return None


# ============================================================
# BEHANDLUNGSZEITRAUM
# ============================================================

def extract_treatment_period(text: str):

    if not text:
        return {
            "start": None,
            "ende": None
        }

    clean = clean_spaces(
        text.replace("\n", " ")
    )

    # --------------------------------------------------------
    # "vom 01.01.2025 bis 05.01.2025"
    # --------------------------------------------------------

    match = re.search(
        r"\bvom\s+"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})"
        r"\s+bis\s+"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})",
        clean,
        re.IGNORECASE
    )

    if match:

        return {
            "start": normalize_date(match.group(1)),
            "ende": normalize_date(match.group(2))
        }

    # --------------------------------------------------------
    # "vom 01.01.2025 05.01.2025"
    # --------------------------------------------------------

    match = re.search(
        r"\bvom\s+"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})"
        r"\s+"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})",
        clean,
        re.IGNORECASE
    )

    if match:

        return {
            "start": normalize_date(match.group(1)),
            "ende": normalize_date(match.group(2))
        }

    # --------------------------------------------------------
    # "ab dem 03.07.2024"
    # --------------------------------------------------------

    match = re.search(
        r"\bab\s+dem\s+"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})",
        clean,
        re.IGNORECASE
    )

    if match:

        return {
            "start": normalize_date(match.group(1)),
            "ende": None
        }

    # --------------------------------------------------------
    # OCR-Variante:
    #
    # "Behandlung anab 03.07.2024"
    # --------------------------------------------------------

    match = re.search(
        r"\bBehandlung\b.{0,30}?"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})",
        clean,
        re.IGNORECASE
    )

    if match:

        return {
            "start": normalize_date(match.group(1)),
            "ende": None
        }

    # --------------------------------------------------------
    # "ab 03.07.2024"
    # --------------------------------------------------------

    match = re.search(
        r"\bab\s+"
        r"(\d{1,2}[.,]\d{1,2}[.,]\d{2,4})",
        clean,
        re.IGNORECASE
    )

    if match:

        return {
            "start": normalize_date(match.group(1)),
            "ende": None
        }

    return {
        "start": None,
        "ende": None
    }


# ============================================================
# MAIN PARSER
# ============================================================

def parse_document(text: str):

    period = extract_treatment_period(text)

    return {
        "name": extract_name(text),
        "geburtsdatum": extract_birthdate(text),
        "behandlungszeitraum": period
    }
