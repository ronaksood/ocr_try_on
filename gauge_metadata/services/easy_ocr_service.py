import logging
import easyocr

logger = logging.getLogger(__name__)


class EasyOcrService:
    """Service wrapper around EasyOCR for gauge image text extraction."""

    def __init__(self, languages: list[str] | None = None) -> None:
        langs = languages or ["en"]
        logger.info("Initializing EasyOCR reader with languages: %s", langs)
        self._reader = easyocr.Reader(langs, verbose=False)

    def read_image(self, image: str | bytes) -> list[str]:
        """Run OCR on an image (path or bytes) and return detected text strings."""
        results = self._reader.readtext(image)
        texts = [entry[1] for entry in results if entry[1]]
        logger.debug("EasyOCR detected %d text regions", len(texts))
        return texts
