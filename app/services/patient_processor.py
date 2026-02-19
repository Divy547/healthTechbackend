from app.engines.diplotype_engine import DiplotypeEngine
from app.engines.phenotype_engine import PhenotypeEngine
from app.engines.drug_risk_engine import DrugRiskEngine
from app.engines.cpic_engine import CPICEngine
from app.services.json_builder import JSONBuilder
from app.core.constants import DRUG_GENE_MAP


class PatientProcessor:

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
                    explanation="The requested drug is not supported in the pharmacogenomic engine."
                )

                results.append(result)
                continue

            # -------------------------------------
            # 2️⃣ Find Variant For Gene
            # -------------------------------------
            gene_variant = next(
                (
                    v for v in patient_data.get("pharmacogene_variants", [])
                    if v.get("gene", "").upper() == gene
                ),
                None
            )

            print("Found variant:", gene_variant)

            # -------------------------------------
            # 3️⃣ No Variant Found
            # -------------------------------------
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
                    explanation="No relevant pharmacogenomic variants were found in the uploaded VCF."
                )

                results.append(result)
                continue

            # -------------------------------------
            # 4️⃣ Build Diplotype
            # -------------------------------------
            diplotype = DiplotypeEngine.build_diplotype(
                gene_variant.get("star_allele"),
                gene_variant.get("genotype")
            )

            # -------------------------------------
            # 5️⃣ Determine Phenotype
            # -------------------------------------
            phenotype = PhenotypeEngine.get_phenotype(gene, diplotype)

            # -------------------------------------
            # 6️⃣ Risk Assessment
            # -------------------------------------
            risk_label, severity = DrugRiskEngine.assess(drug, phenotype)

            # -------------------------------------
            # 7️⃣ CPIC Recommendation
            # -------------------------------------
            recommendation = CPICEngine.get_recommendation(drug, phenotype)

            # -------------------------------------
            # 8️⃣ Build Final JSON
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
                explanation="LLM explanation placeholder for now."
            )

            results.append(result)

        return results
