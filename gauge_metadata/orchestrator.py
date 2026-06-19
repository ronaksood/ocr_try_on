import logging
from gauge_metadata.schemas.metadata import GaugeMetadataResponse, HealthResponse
from gauge_metadata.services.ocr_service import OcrService

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrator that coordinates gauge metadata processing and module health checks."""

    def __init__(self) -> None:
        self._ocr_service = OcrService()

    def health_check(self) -> HealthResponse:
        """Returns the overall health status of the gauge metadata module."""
        logger.info("Executing health check")
        return HealthResponse(status="healthy")

    def process(self, engine: str, image_bytes: bytes) -> GaugeMetadataResponse:
        """Process the image bytes using the requested OCR engine by delegating

        to the main OCR service.
        """
        logger.info("Delegating process request for engine: %s", engine)
        return self._ocr_service.process_image(engine=engine, image=image_bytes)
