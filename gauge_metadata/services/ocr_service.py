import logging

from gauge_metadata.schemas.metadata import GaugeMetadataResponse
from gauge_metadata.services.easy_ocr_service import EasyOcrService
from gauge_metadata.services.paddle_ocr_service import PaddleOcrService
from gauge_metadata.services.rapid_ocr_service import RapidOcrService
from gauge_metadata.services.tesseract_ocr_service import TesseractOcrService
from gauge_metadata.utils.numbers import extract_numbers, infer_zero
from gauge_metadata.utils.units import match_unit

logger = logging.getLogger(__name__)


class OcrService:
    """
    Main OCR service layer that dispatches image extraction requests
    to the specified engine 
    and runs the common metadata post-processing logic.
    """

    def __init__(self) -> None:
        self._engines = {
            "easy_ocr": EasyOcrService(),
            "paddle_ocr": PaddleOcrService(),
            "rapid_ocr": RapidOcrService(),
            "tesseract_ocr": TesseractOcrService(),
        }

    def process_image(
        self,
        engine: str,
        image: str | bytes,
    ) -> GaugeMetadataResponse:
        """
        Process an image using the selected OCR engine and
        return extracted gauge metadata.
        """

        texts = self._engines[engine].read_image(image)

        unit = match_unit(texts)

        numbers = extract_numbers(texts)
        numbers = infer_zero(numbers)

        min_value: float | None = None
        max_value: float | None = None

        if len(numbers) >= 2:
            min_value = numbers[0]
            max_value = numbers[-1]
        else:
            logger.warning(
                "Less than 2 numeric values detected. "
                "min_value and max_value will be null."
            )

        return GaugeMetadataResponse(
            unit=unit,
            min_value=min_value,
            max_value=max_value,
        )