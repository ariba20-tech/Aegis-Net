"""
FHIR Unit Normalization & Standardizer
Owner: Sanjoli Vaibhav
Ensures all continuous signals, lab units, and imaging parameters align with standard FHIR conventions.
"""

from typing import Dict, Any


class FHIRNormalizer:
    """Normalizes laboratory units and vitals to standard UCUM / LOINC representation."""

    @staticmethod
    def normalize_temperature(val: float, unit: str = "F") -> float:
        """Converts Fahrenheit to Celsius if needed."""
        if unit.upper() == "F":
            return round((val - 32.0) * 5.0 / 9.0, 1)
        return val

    @staticmethod
    def format_fhir_observation(code: str, display: str, value: Any, unit: str) -> Dict[str, Any]:
        """Creates a standardized FHIR Observation resource stub."""
        return {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": code,
                    "display": display
                }]
            },
            "valueQuantity": {
                "value": value,
                "unit": unit,
                "system": "http://unitsofmeasure.org"
            }
        }
