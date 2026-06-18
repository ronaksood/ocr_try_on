import re
import statistics

_NUMBER_PATTERN = re.compile(r"-?\d+\.?\d*")

_LEADING_ARTIFACTS = set("'\"~,;:!?_})]>#@")
_TRAILING_ARTIFACTS = set("'\"~,;:!?_})]>#@-")
_ALLOWED_NUMERIC_CHARS = set("0123456789.- ")

# Gauge scale values almost never exceed 4 digits.
_MAX_GAUGE_VALUE = 10_000


def _clean_text(text: str) -> str:
    """Strip common OCR artifacts from edges of text."""
    stripped = text.strip()
    while stripped and stripped[0] in _LEADING_ARTIFACTS:
        stripped = stripped[1:]
    while stripped and stripped[-1] in _TRAILING_ARTIFACTS:
        stripped = stripped[:-1]
    return stripped.strip()


def _is_numeric_text(text: str) -> bool:
    """Check if OCR text is a clean numeric entry with no embedded letters.

    Rejects entries like 'EN 13190', '62544HO', 'CL 1.0', 'i1b06JS9'.
    """
    cleaned = _clean_text(text)
    if not cleaned:
        return False
    return all(c in _ALLOWED_NUMERIC_CHARS for c in cleaned)


def _filter_outliers(numbers: list[float]) -> list[float]:
    """Remove statistical outliers using IQR method."""
    if len(numbers) < 4:
        return numbers
    quantile_points = statistics.quantiles(numbers, n=4)
    q1, q3 = quantile_points[0], quantile_points[2]
    iqr = q3 - q1
    if iqr == 0:
        return numbers
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return [x for x in numbers if lower <= x <= upper]


def extract_numbers(texts: list[str]) -> list[float]:
    """Extract numeric values from clean OCR text entries.

    Three-stage noise filtering:
      1. Clean text filter — reject entries with embedded letters
      2. Magnitude cap — reject values >= 10,000 (serial/model numbers)
      3. IQR outlier removal — reject statistical outliers in the cluster
    """
    numbers: list[float] = []
    for text in texts:
        if not _is_numeric_text(text):
            continue
        cleaned = _clean_text(text)
        matches = _NUMBER_PATTERN.findall(cleaned)
        for match in matches:
            try:
                value = float(match)
                if abs(value) < _MAX_GAUGE_VALUE:
                    numbers.append(value)
            except ValueError:
                continue
    numbers = sorted(set(numbers))
    return _filter_outliers(numbers)


def infer_zero(numbers: list[float]) -> list[float]:
    """Infer a missing 0 starting value for gauge scales.

    Gauge scales are arithmetic progressions (0, 10, 20, ...).
    OCR commonly misses the '0' marking near the dial edge.
    If the smallest detected value equals the step size of the
    sequence, 0 was very likely missed.
    """
    if len(numbers) < 3 or 0.0 in numbers or numbers[0] <= 0:
        return numbers

    diffs = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    positive_diffs = sorted(d for d in diffs if d > 0)
    if not positive_diffs:
        return numbers

    step = positive_diffs[len(positive_diffs) // 2]  # median

    if step > 0 and abs(numbers[0] - step) / step <= 0.15:
        return [0.0] + numbers

    return numbers
