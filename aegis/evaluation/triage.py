"""
Clinical Triage Classifier (RED / YELLOW / GREEN)
Owner: Padmini Rao
Determines the clinical urgency and acuity of the encounter based on findings.
"""

from typing import List
from aegis.contracts.findings import ClinicalFinding, SeverityLevel
from aegis.contracts.evaluation import TriageLevel


class TriageEngine:
    """Categorizes patients according to emergency acuity protocols."""

    def classify(self, findings: List[ClinicalFinding]) -> TriageLevel:
        """
        Applies clinical decision rules:
        - RED: Any CRITICAL finding or multiple SEVERE findings (e.g., severe hypoxia + respiratory distress).
        - YELLOW: MODERATE findings requiring urgent diagnostic workup.
        - GREEN: Mild or normal findings suitable for outpatient management.
        """
        has_critical = any(f.severity == SeverityLevel.CRITICAL for f in findings)
        severe_count = sum(1 for f in findings if f.severity == SeverityLevel.SEVERE)
        moderate_count = sum(1 for f in findings if f.severity == SeverityLevel.MODERATE)

        if has_critical or severe_count >= 1:
            # e.g., Resting SpO2 < 90% constitutes high acuity / urgent oxygenation
            return TriageLevel.RED

        if moderate_count >= 1:
            return TriageLevel.YELLOW

        return TriageLevel.GREEN
