from datetime import datetime
from app.schemas.output_schema import (
    PharmacogenomicResponse,
    RiskAssessment,
    PharmacogenomicProfile,
    ClinicalRecommendation,
    LLMGeneratedExplanation,
    QualityMetrics,
    DetectedVariant
)
from app.engines.confidence_engine import ConfidenceEngine



class JSONBuilder:

    @staticmethod
    def build(
        patient_id: str,
        drug: str,
        gene: str,
        diplotype: str,
        phenotype: str,
        variants: list,
        risk_label: str,
        severity: str,
        recommendation: dict,
        explanation: str,
        parsing_success: bool = True
    ) -> PharmacogenomicResponse:

        # ----------------------------
        # Build detected variants
        # ----------------------------
        detected_variants = [
            DetectedVariant(
                rsid=v.get("rsid"),
                star_allele=v.get("star_allele"),
                genotype=v.get("genotype"),
                ref=v.get("ref"),
                alt=v.get("alt"),
                position=v.get("position"),
                filter_status=v.get("filter_status")
            )
            for v in variants
        ]

        # ----------------------------
        # Risk Assessment
        # ----------------------------
        risk_assessment = RiskAssessment(
            risk_label=risk_label,
            confidence_score=ConfidenceEngine.calculate(
                variants=variants,
                phenotype=phenotype,
                risk_label=risk_label
            ),
            # deterministic logic → high confidence
            severity=severity
        )

        # ----------------------------
        # Pharmacogenomic Profile
        # ----------------------------
        pharmacogenomic_profile = PharmacogenomicProfile(
            primary_gene=gene,
            diplotype=diplotype,
            phenotype=phenotype,
            detected_variants=detected_variants
        )

        # ----------------------------
        # Clinical Recommendation
        # ----------------------------
        clinical_recommendation = ClinicalRecommendation(
            action=recommendation.get("action"),
            details=recommendation.get("details")
        )

        # ----------------------------
        # LLM Explanation
        # ----------------------------
        llm_generated_explanation = LLMGeneratedExplanation(
            summary=explanation
        )

        # ----------------------------
        # Quality Metrics
        # ----------------------------
        quality_metrics = QualityMetrics(
            vcf_parsing_success=parsing_success,
            gene_match_confidence=1.0 if variants else 0.0
        )

        # ----------------------------
        # Final Structured Response
        # ----------------------------
        return PharmacogenomicResponse(
            patient_id=patient_id,
            drug=drug,
            timestamp=datetime.utcnow(),
            risk_assessment=risk_assessment,
            pharmacogenomic_profile=pharmacogenomic_profile,
            clinical_recommendation=clinical_recommendation,
            llm_generated_explanation=llm_generated_explanation,
            quality_metrics=quality_metrics
        )
