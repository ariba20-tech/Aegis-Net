"""
Cross-Agent Debate & Conflict Detection Engine
Owner: Padmini Rao
Compares findings across Vision, EHR, and Vitals to surface clinical inconsistencies.
"""

from typing import List, Dict, Any
from aegis.contracts.findings import AgentFindingReport, ClinicalFinding, ModalityType
from aegis.contracts.evaluation import ConflictItem


class DebateEngine:
    """Detects discrepancies between modalities and orchestrates cross-agent consensus."""

    def evaluate_consensus(self, reports: List[AgentFindingReport]) -> List[ConflictItem]:
        """
        Scans findings across modalities for contradictory clinical signals.
        Example: Severe hypoxemia on vitals with completely normal chest radiograph.
        """
        conflicts: List[ConflictItem] = []
        modality_map: Dict[ModalityType, AgentFindingReport] = {r.modality: r for r in reports}

        # Check: Vitals hypoxia vs Imaging lung opacity
        if ModalityType.VITALS in modality_map and ModalityType.VISION in modality_map:
            vitals = modality_map[ModalityType.VITALS]
            vision = modality_map[ModalityType.VISION]

            has_hypoxia = any("hypox" in f.concept_name.lower() or "spo2" in f.concept_name.lower() for f in vitals.findings)
            has_lung_finding = any("opacity" in f.concept_name.lower() or "infiltrate" in f.concept_name.lower() for f in vision.findings)

            # If hypoxia is present but vision confidence is marginal (< 0.70), flag for review
            if has_hypoxia and vision.overall_confidence < 0.70:
                conflicts.append(
                    ConflictItem(
                        conflict_id=f"CONF-{len(conflicts)+1:03d}",
                        modalities_involved=["vitals", "vision"],
                        description="Severe hypoxemia detected on telemetry, but radiological confidence in pulmonary source is low.",
                        severity="high",
                        recommended_resolution="Re-examine pulmonary vascular vs parenchymal findings on CXR."
                    )
                )

        return conflicts
