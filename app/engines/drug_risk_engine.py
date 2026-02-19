class DrugRiskEngine:

    @staticmethod
    def assess(drug: str, phenotype: str):

        drug = drug.upper()

        # CODEINE → CYP2D6
        if drug == "CODEINE":
            if phenotype == "PM":
                return "Ineffective", "high"
            elif phenotype == "UM":
                return "Toxic", "critical"
            elif phenotype == "IM":
                return "Adjust Dosage", "moderate"
            else:
                return "Safe", "none"

        # CLOPIDOGREL → CYP2C19
        if drug == "CLOPIDOGREL":
            if phenotype == "PM":
                return "Ineffective", "high"
            elif phenotype == "IM":
                return "Adjust Dosage", "moderate"
            else:
                return "Safe", "none"

        # WARFARIN → CYP2C9
        if drug == "WARFARIN":
            if phenotype == "PM":
                return "Adjust Dosage", "high"
            elif phenotype == "IM":
                return "Adjust Dosage", "moderate"
            else:
                return "Safe", "none"

        # SIMVASTATIN → SLCO1B1
        if drug == "SIMVASTATIN":
            if phenotype == "Poor":
                return "Toxic", "high"
            elif phenotype == "Reduced":
                return "Adjust Dosage", "moderate"
            else:
                return "Safe", "none"

        # AZATHIOPRINE → TPMT
        if drug == "AZATHIOPRINE":
            if phenotype == "PM":
                return "Toxic", "critical"
            elif phenotype == "IM":
                return "Adjust Dosage", "high"
            else:
                return "Safe", "none"

        # FLUOROURACIL → DPYD
        if drug == "FLUOROURACIL":
            if phenotype == "PM":
                return "Toxic", "critical"
            elif phenotype == "IM":
                return "Adjust Dosage", "high"
            else:
                return "Safe", "none"

        return "Unknown", "low"
