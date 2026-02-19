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
                    explanation={
    "summary": f"{drug} is not supported in the pharmacogenomic engine.",
    "genetic_factors": [],
    "clinical_implications": "No pharmacogenomic assessment could be performed.",
    "patient_friendly_explanation": (
        f"The medication {drug} is not currently supported in our genetic analysis system."
    ),
    "references": []
}

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
                    explanation={
    "summary": f"No relevant pharmacogenomic variants were detected for {gene}.",
    "genetic_factors": [],
    "clinical_implications": (
        "Without detected variants, no genotype-based drug modification is recommended."
    ),
    "patient_friendly_explanation": (
        "Your genetic test did not show any significant variations affecting this medication."
    ),
    "references": []
}

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
                explanation = {
    "summary": (
        f"Genetic analysis identified a {gene} {diplotype} diplotype consistent with "
        f"{phenotype} status. This genotype alters enzymatic activity and may "
        f"impact therapeutic response to {drug}."
    ),
    "genetic_factors": [
        f"Gene involved: {gene}",
        f"Diplotype detected: {diplotype}",
        f"Phenotype classification: {phenotype}"
    ],
    "clinical_implications": (
        f"Patients with {phenotype} status for {gene} may experience altered "
        f"drug metabolism affecting efficacy or toxicity. Clinical monitoring "
        f"and guideline-based adjustments are recommended."
    ),
    "patient_friendly_explanation": (
        f"Your genetic test shows that your body processes {drug} differently "
        f"due to variations in the {gene} gene. This may affect how well the "
        f"medicine works or increase side effects. Your doctor may adjust the "
        f"dose or recommend an alternative medication."
    ),
    "references": [
        f"CPIC Guideline for {gene} and {drug}",
        "Clinical Pharmacogenetics Implementation Consortium (CPIC)",
        "PharmGKB Database"
    ]
}

            )

            results.append(result)

        return results
