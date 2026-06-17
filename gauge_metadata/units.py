from typing import Optional

# Set-based vocabulary for O(1) exact word matching.
# No longer needs longest-match-first ordering because we match
# whole word tokens, not substrings.
UNIT_VOCABULARY: frozenset[str] = frozenset({
    "bar", "mbar", "psi", "kpa", "mpa", "pa",
    "kg/cm2", "kg/cm²", "kgf/cm2", "kgf/cm²",
    "mmwc", "mmh2o", "inh2o", "mmhg", "inhg",
    "vac", "%", "°c", "°f",
    "v", "ma", "a", "hz", "khz",
    "rpm", "lpm", "l/min", "gpm",
})

_STRIP_CHARS = "'\"~,;:!?_.})]>#@"


def match_unit(texts: list[str]) -> Optional[str]:
    """Match OCR-detected text against the engineering unit vocabulary.

    Splits each text into word tokens and checks for exact matches,
    preventing false positives from substring matching (e.g. 'a' inside 'WKAU').
    """
    for text in texts:
        tokens = text.strip().lower().split()
        for token in tokens:
            cleaned = token.strip(_STRIP_CHARS)
            if cleaned in UNIT_VOCABULARY:
                return cleaned
    return None
