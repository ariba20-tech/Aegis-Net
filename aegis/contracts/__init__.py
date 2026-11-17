"""
Universal contracts exposed for all modules.
Imported across Sanjoli's ingestion, Ariba's orchestrator, and Padmini's evaluation layer.
"""

from aegis.contracts.findings import (
    ModalityType,
    SeverityLevel,
    ClinicalFinding,
    AgentFindingReport,
)
from aegis.contracts.evaluation import (
    TriageLevel,
    ConflictItem,
    DoctorCriticVerdict,
    FinalClinicalReport,
)
from aegis.contracts.state import EncounterState

__all__ = [
    "ModalityType",
    "SeverityLevel",
    "ClinicalFinding",
    "AgentFindingReport",
    "TriageLevel",
    "ConflictItem",
    "DoctorCriticVerdict",
    "FinalClinicalReport",
    "EncounterState",
]

