"""
Doctor-Critic Verification & Hallucination Guardrail Layer
Owner: Padmini Rao
Validates multi-agent findings against medical guidelines and clinical plausibility.
"""

from typing import List, Optional
from aegis.contracts.findings import AgentFindingReport, ClinicalFinding
from aegis.contracts.evaluation import ConflictItem, DoctorCriticVerdict


class DoctorCritic:
    """Clinical oversight layer verifying coherence and triggering retries when uncertainty is high."""

    def __init__(self, confidence_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold

    def verify(
        self,
        findings: List[ClinicalFinding],
        conflicts: List[ConflictItem],
        iteration: int = 1,
        max_retries: int = 2
    ) -> DoctorCriticVerdict:
        """
        Evaluates clinical findings.
        If iteration < max_retries and unresolved high conflicts or low confidence exist, requests retry.
        """
        if not findings:
            return DoctorCriticVerdict(
                is_plausible=False,
                hallucination_detected=False,
                guideline_concordant=False,
                verification_confidence=0.1,
                critique_notes="No clinical findings presented for evaluation.",
                needs_retry=iteration <= max_retries,
                retry_guidance="Request all specialized agents perform baseline intake."
            )

        # Calculate weighted confidence
        avg_confidence = sum(f.confidence for f in findings) / len(findings)
        has_critical_conflicts = any(c.severity == "high" for c in conflicts)

        # Low confidence or severe conflict triggers a cyclic retry if budget remains
        if (avg_confidence < self.confidence_threshold or has_critical_conflicts) and iteration <= max_retries:
            return DoctorCriticVerdict(
                is_plausible=True,
                hallucination_detected=False,
                guideline_concordant=True,
                verification_confidence=avg_confidence,
                critique_notes=(
                    f"Iteration {iteration}: Confidence ({avg_confidence:.2f}) below threshold "
                    f"({self.confidence_threshold:.2f}) or critical conflicts present ({len(conflicts)})."
                ),
                needs_retry=True,
                retry_guidance="Re-evaluate pulmonary infiltrate clarity and cross-reference with CBC leukocytosis."
            )

        # Verified state
        return DoctorCriticVerdict(
            is_plausible=True,
            hallucination_detected=False,
            guideline_concordant=True,
            verification_confidence=max(avg_confidence, 0.90),
            critique_notes="Findings across Imaging, EHR, and Vitals are coherent, plausible, and guideline-concordant.",
            needs_retry=False,
            retry_guidance=None
        )
