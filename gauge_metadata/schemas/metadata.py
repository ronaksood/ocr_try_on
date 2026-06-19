from pydantic import BaseModel, Field


class GaugeMetadataResponse(BaseModel):
    """Pydantic model representing the extracted gauge metadata."""

    unit: str | None = Field(
        default=None,
        description="The detected engineering unit of the gauge (e.g., 'bar', 'psi').",
    )
    min_value: float | None = Field(
        default=None,
        description="The minimum scale value of the gauge.",
    )
    max_value: float | None = Field(
        default=None,
        description="The maximum scale value of the gauge.",
    )


class HealthResponse(BaseModel):
    """Pydantic model representing the health check response."""

    status: str = Field(
        default="healthy",
        description="Status of the module.",
    )
