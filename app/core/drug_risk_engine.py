DRUG_GENE_MAP = {
    "CLOPIDOGREL": "CYP2C19",
    "FLUOROURACIL": "DPYD"
}

class DrugRiskEngine:

    @staticmethod
    def assess(drug: str, phenotype: str):

        if drug == "CLOPIDOGREL":
            if phenotype == "PM":
                return "Ineffective", "high"
            elif phenotype == "IM":
                return "Adjust Dosage", "moderate"
            else:
                return "Safe", "none"

        if drug == "FLUOROURACIL":
            if phenotype == "PM":
                return "Toxic", "critical"
            elif phenotype == "IM":
                return "Adjust Dosage", "high"
            else:
                return "Safe", "none"

        return "Unknown", "low"
