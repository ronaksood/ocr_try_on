import logging
import cv2
import numpy as np
from paddleocr import PaddleOCR

logger = logging.getLogger(__name__)


class PaddleOcrService:
    """Service wrapper around PaddleOCR for gauge image text extraction."""

    def __init__(self) -> None:
        logger.info("Initializing PaddleOCR")
        self._ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            lang="en",
            use_gpu=True,  # leverage the DGX server GPUs if available
        )

    def read_image(self, image: str | bytes) -> list[str]:
        """Run OCR on an image (path or bytes) and return detected text strings."""
        if isinstance(image, bytes):
            nparr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Failed to decode image bytes for PaddleOCR")
        else:
            img = image

        result = self._ocr.ocr(img)
        texts: list[str] = []

        # PaddleOCR returns a list of pages
        if result:
            for page in result:
                if page is None:
                    continue
                for line in page:
                    # Line structure: [[[x1,y1], ...], ('Text', confidence)]
                    detected_text = line[1][0]
                    if detected_text:
                        texts.append(detected_text)

        logger.debug("PaddleOCR detected %d text regions", len(texts))
        return texts
