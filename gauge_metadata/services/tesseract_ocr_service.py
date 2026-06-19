import io
import logging
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)


class TesseractOcrService:
    """Service wrapper around Tesseract for gauge image text extraction."""

    def read_image(self, image: str | bytes) -> list[str]:
        """Run OCR on an image (path or bytes) and return detected text lines."""
        if isinstance(image, bytes):
            img = Image.open(io.BytesIO(image))
        else:
            img = Image.open(image)

        text = pytesseract.image_to_string(img)
        texts = [line.strip() for line in text.splitlines() if line.strip()]
        logger.debug("Tesseract OCR detected %d text regions", len(texts))
        return texts
