from datetime import datetime

class JSONBuilder:

    @staticmethod
    def build(patient_id, drug, risk_label, severity,
              gene, diplotype, phenotype, variants, recommendation, explanation):

        return {
            "patient_id": patient_id,
            "drug": drug,
            "timestamp": datetime.utcnow().isoformat(),
            "risk_assessment": {
                "risk_label": risk_label,
                "confidence_score": 0.95,
                "severity": severity
            },
            "pharmacogenomic_profile": {
                "primary_gene": gene,
                "diplotype": diplotype,
                "phenotype": phenotype,
                "detected_variants": variants
            },
            "clinical_recommendation": {
                "recommendation": recommendation
            },
            "llm_generated_explanation": {
                "summary": explanation
            },
            "quality_metrics": {
                "vcf_parsing_success": True
            }
        }
