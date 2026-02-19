from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -----------------------------
# Risk Assessment
# -----------------------------
class RiskAssessment(BaseModel):
    risk_label: str = Field(
        ...,
        description="Safe | Adjust Dosage | Toxic | Ineffective | Unknown"
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )
    severity: str = Field(
        ...,
        description="none | low | moderate | high | critical"
    )


# -----------------------------
# Detected Variant
# -----------------------------
class DetectedVariant(BaseModel):
    rsid: str
    star_allele: Optional[str] = None
    genotype: Optional[str] = None
    ref: Optional[str] = None
    alt: Optional[str] = None
    position: Optional[str] = None
    filter_status: Optional[str] = None


# -----------------------------
# Pharmacogenomic Profile
# -----------------------------
class PharmacogenomicProfile(BaseModel):
    primary_gene: str
    diplotype: str
    phenotype: str = Field(
        ...,
        description="PM | IM | NM | RM | URM | Unknown"
    )
    detected_variants: List[DetectedVariant]


# -----------------------------
# Clinical Recommendation
# -----------------------------
class ClinicalRecommendation(BaseModel):
    action: str
    details: str


# -----------------------------
# LLM Generated Explanation
# -----------------------------
class LLMGeneratedExplanation(BaseModel):
    summary: str


# -----------------------------
# Quality Metrics
# -----------------------------
class QualityMetrics(BaseModel):
    vcf_parsing_success: bool
    gene_match_confidence: Optional[float] = None


# -----------------------------
# FINAL REQUIRED RESPONSE
# -----------------------------
class PharmacogenomicResponse(BaseModel):
    patient_id: str
    drug: str
    timestamp: datetime

    risk_assessment: RiskAssessment
    pharmacogenomic_profile: PharmacogenomicProfile
    clinical_recommendation: ClinicalRecommendation
    llm_generated_explanation: LLMGeneratedExplanation
    quality_metrics: QualityMetrics
