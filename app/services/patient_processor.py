from app.engines.diplotype_engine import DiplotypeEngine
from app.engines.phenotype_engine import PhenotypeEngine
from app.engines.drug_risk_engine import DrugRiskEngine
from app.engines.cpic_engine import CPICEngine
from app.services.json_builder import JSONBuilder
from app.core.constants import DRUG_GENE_MAP
from app.services.llm_service import GeminiService
from app.core.llm_prompts import DUAL_MODE_PGX_PROMPT as EXPLANATION_JSON_PROMPT
import traceback

class PatientProcessor:
    print("🚀 PatientProcessor.process CALLED")
    @staticmethod
    def get_llm():
        return GeminiService()

    @staticmethod
    def process(patient_data: dict, drugs: list):

        results = []

        print("Incoming drugs:", drugs)
        print("Available variants:", patient_data.get("pharmacogene_variants", []))

        for drug in drugs:

            drug = drug.strip().upper()
            print("\nProcessing drug:", drug)

            gene = DRUG_GENE_MAP.get(drug)
            print("Mapped gene:", gene)

            # -------------------------------------
            # 1️⃣ Unsupported Drug Handling
            # -------------------------------------
            if not gene:
                result = JSONBuilder.build(
                    patient_id=patient_data["patient_id"],
                    drug=drug,
                    gene="Unknown",
                    diplotype="Unknown",
                    phenotype="Unknown",
                    variants=[],
                    risk_label="Unknown",
                    severity="low",
                    recommendation={
                        "action": "Unsupported drug",
                        "details": f"{drug} is not supported in the system."
                    },
                    explanation={
                        "summary": f"{drug} is not supported in the pharmacogenomic engine.",
                        "genetic_factors": [],
                        "clinical_implications": "No pharmacogenomic assessment could be performed.",
                        "patient_friendly_explanation": f"{drug} is not supported yet.",
                        "references": []
                    }
                )
                results.append(result)
                continue

            # -------------------------------------
            # 2️⃣ Find Variant
            # -------------------------------------
            gene_variant = next(
                (
                    v for v in patient_data.get("pharmacogene_variants", [])
                    if v.get("gene", "").upper() == gene
                ),
                None
            )

            print("Found variant:", gene_variant)

            if not gene_variant:
                result = JSONBuilder.build(
                    patient_id=patient_data["patient_id"],
                    drug=drug,
                    gene=gene,
                    diplotype="Unknown",
                    phenotype="Unknown",
                    variants=[],
                    risk_label="Unknown",
                    severity="low",
                    recommendation={
                        "action": "No variant detected",
                        "details": f"No pharmacogenomic variants detected for {gene}."
                    },
                    explanation={
                        "summary": f"No variants detected for {gene}.",
                        "genetic_factors": [],
                        "clinical_implications": "No genotype-based change recommended.",
                        "patient_friendly_explanation": "Your genetics show no major impact on this drug.",
                        "references": []
                    }
                )
                results.append(result)
                continue

            # -------------------------------------
            # 3️⃣ Core Engines
            # -------------------------------------
            diplotype = DiplotypeEngine.build_diplotype(
                gene_variant.get("star_allele"),
                gene_variant.get("genotype")
            )

            phenotype = PhenotypeEngine.get_phenotype(gene, diplotype)
            risk_label, severity = DrugRiskEngine.assess(drug, phenotype)
            recommendation = CPICEngine.get_recommendation(drug, phenotype)

            # -------------------------------------
            # 4️⃣ Gemini Layer (SAFE)
            # -------------------------------------
            explanation = None

            try:
                prompt = EXPLANATION_JSON_PROMPT.format(
                    gene=gene,
                    diplotype=diplotype,
                    phenotype=phenotype,
                    drug=drug
                )

                raw_llm = PatientProcessor.get_llm().generate_json(prompt)
                print("🧠 Gemini keys:", raw_llm.keys())

                # Normalize dual-mode output
                if isinstance(raw_llm, dict) and "doctor_explanation" in raw_llm:
                    doc = raw_llm["doctor_explanation"] or {}
                    patient = raw_llm.get("patient_explanation", {}) or {}

                    explanation = {
                        "summary": doc.get("clinical_summary") or f"{gene} affects {drug} response.",
                        "genetic_factors": [
                            f"Gene: {gene}",
                            f"Diplotype: {diplotype}",
                            f"Phenotype: {phenotype}",
                        ],
                        "clinical_implications": doc.get("prescription_guidance") or "Refer to pharmacogenomic guidelines.",
                        "patient_friendly_explanation": patient.get("simple_summary") or "Your genetics may affect how this drug works.",
                        "references": [doc.get("evidence_basis")] if doc.get("evidence_basis") else [],
                    }

                elif isinstance(raw_llm, dict):
                    explanation = raw_llm

            except Exception as e:
                print("🚨 LLM failure FULL TRACE:")
                traceback.print_exc()

            # -------------------------------------
            # 5️⃣ Final Fallback (Never crash)
            # -------------------------------------
            if not explanation:
                explanation = {
                    "summary": f"{gene} {diplotype} may influence response to {drug}.",
                    "genetic_factors": [gene, diplotype, phenotype],
                    "clinical_implications": "Pharmacogenomic variation detected.",
                    "patient_friendly_explanation": "Your genetics may affect this medicine.",
                    "references": ["CPIC", "PharmGKB"]
                }

            # -------------------------------------
            # 6️⃣ Build Response
            # -------------------------------------
            result = JSONBuilder.build(
                patient_id=patient_data["patient_id"],
                drug=drug,
                gene=gene,
                diplotype=diplotype,
                phenotype=phenotype,
                variants=[gene_variant],
                risk_label=risk_label,
                severity=severity,
                recommendation=recommendation,
                explanation=explanation
            )

            results.append(result)

        return results