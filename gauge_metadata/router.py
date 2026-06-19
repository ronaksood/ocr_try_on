from fastapi import APIRouter, File, HTTPException, UploadFile
from gauge_metadata.orchestrator import Orchestrator
from gauge_metadata.schemas.metadata import GaugeMetadataResponse, HealthResponse

router = APIRouter(prefix="/analog_gauge", tags=["Analog Gauge OCR"])
orchestrator = Orchestrator()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Check the health status of the module."""
    try:
        return orchestrator.health_check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/easy_ocr", response_model=GaugeMetadataResponse)
async def easy_ocr(
    file: UploadFile = File(
        ..., description="The gauge image file to process with EasyOCR."
    )
):
    """Run EasyOCR on the uploaded gauge image to extract metadata."""

    image_bytes = await file.read()
    return orchestrator.process(engine="easy_ocr", image_bytes=image_bytes)



@router.post("/paddle_ocr", response_model=GaugeMetadataResponse)
async def paddle_ocr(
    file: UploadFile = File(
        ..., description="The gauge image file to process with PaddleOCR."
    )
):
    """Run PaddleOCR on the uploaded gauge image to extract metadata."""

    image_bytes = await file.read()
    return orchestrator.process(engine="paddle_ocr", image_bytes=image_bytes)



@router.post("/rapid_ocr", response_model=GaugeMetadataResponse)
async def rapid_ocr(
    file: UploadFile = File(
        ..., description="The gauge image file to process with RapidOCR."
    )
):
    """Run RapidOCR on the uploaded gauge image to extract metadata."""

    image_bytes = await file.read()
    return orchestrator.process(engine="rapid_ocr", image_bytes=image_bytes)


@router.post("/tesseract_ocr", response_model=GaugeMetadataResponse)
async def tesseract_ocr(
    file: UploadFile = File(
        ..., description="The gauge image file to process with Tesseract OCR."
    )
):
    """Run Tesseract OCR on the uploaded gauge image to extract metadata."""

    image_bytes = await file.read()
    return orchestrator.process(engine="tesseract_ocr", image_bytes=image_bytes)
