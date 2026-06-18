from dataclasses import dataclass, field


@dataclass
class GaugeMetadata:
    """Data contract representing the extracted gauge metadata."""

    unit: str | None = None
    min_value: float | None = None
    max_value: float | None = None
    all_detected_text: list[str] = field(default_factory=list)
    all_detected_numbers: list[float] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize metadata instance to a dictionary."""
        return {
            "unit": self.unit,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "all_detected_text": self.all_detected_text,
            "all_detected_numbers": self.all_detected_numbers,
        }
