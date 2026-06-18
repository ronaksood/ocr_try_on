import logging

from paddleocr import PaddleOCR

logger = logging.getLogger(__name__)


class OcrService:
    """Service wrapper around PaddleOCR for gauge image text extraction."""

    def __init__(self) -> None:
        logger.info("Initializing PaddleOCR")

        self._ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            lang="en",
        )

    def read_image(self, image_path: str) -> list[str]:
        """Run OCR on an image and return detected text strings."""

        result = self._ocr.predict(image_path)

        texts: list[str] = []

        for page in result:
            for item in page["rec_texts"]:
                if item:
                    texts.append(item)

        logger.debug(
            "OCR detected %d text regions in %s",
            len(texts),
            image_path,
        )

        return texts