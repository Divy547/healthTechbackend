class CPICEngine:

    @staticmethod
    def get_recommendation(drug: str, phenotype: str):

        if drug == "CLOPIDOGREL" and phenotype in ["PM", "IM"]:
            return "Consider alternative antiplatelet therapy."

        if drug == "FLUOROURACIL" and phenotype == "PM":
            return "Avoid standard dosing. Consider dose reduction."

        return "Standard dosing recommended."
