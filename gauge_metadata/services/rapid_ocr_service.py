import logging
import cv2
import numpy as np

from rapidocr_onnxruntime import RapidOCR

logger = logging.getLogger(__name__)

class RapidOcrService:
    """Service wrapper around RapidOCR."""

    def __init__(self) -> None:
        logger.info("Initializing RapidOCR")
        self._ocr = RapidOCR()

    def read_image(self, image: str | bytes) -> list[str]:
        """Run OCR on an image (path or bytes) and return detected text strings."""
        if isinstance(image, bytes):
            nparr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Failed to decode image bytes for RapidOCR")
        else:
            img = image

        result, _ = self._ocr(img)
        texts: list[str] = []

        if result:
            for item in result:
                # Structure: [bbox, text, confidence]
                text = item[1]
                if text:
                    texts.append(text)

        logger.debug("RapidOCR detected %d text regions", len(texts))
        return texts
