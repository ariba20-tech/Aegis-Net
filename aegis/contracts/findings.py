"""
AEGIS-NET Universal Data Contracts: Agent Findings
Defines the standard schemas returned by Sanjoli's specialized agents (Vision, EHR, Vitals)
and ingested by Ariba's LangGraph orchestrator.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ModalityType(str, Enum):
    VISION = "vision"
    EHR = "ehr"
    VITALS = "vitals"


class SeverityLevel(str, Enum):
    NORMAL = "NORMAL"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class ClinicalFinding(BaseModel):
    """A standardized clinical observation extracted by any specialized agent."""
    finding_id: str = Field(..., description="Unique finding ID e.g., 'F-VIS-001'")
    modality: ModalityType = Field(..., description="Modality source (vision, ehr, vitals)")
    concept_name: str = Field(..., description="Medical concept e.g., 'Bilateral Infiltrate', 'SpO2 Desaturation'")
    observation: str = Field(..., description="Detailed textual description of the clinical observation")
    evidence_or_roi: Optional[str] = Field(None, description="Bounding box, slice number, or clinical note quote")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Agent confidence score between 0.0 and 1.0")
    severity: SeverityLevel = Field(default=SeverityLevel.UNKNOWN, description="Severity assessment")
    timestamp: Optional[str] = Field(None, description="Timestamp or time offset if time-series")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom modality-specific metadata")


class AgentFindingReport(BaseModel):
    """Standardized envelope returned by any specialized agent to the orchestrator."""
    agent_name: str = Field(..., description="e.g., 'VisionAgent', 'EHRAgent', 'VitalsAgent'")
    modality: ModalityType
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    findings: List[ClinicalFinding] = Field(default_factory=list)
    raw_summary: str = Field(..., description="High-level text summary from the agent")
    execution_time_ms: Optional[float] = None
