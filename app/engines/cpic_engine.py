class CPICEngine:

    @staticmethod
    def get_recommendation(drug: str, phenotype: str) -> dict:

        drug = drug.upper()

        # ----------------------------------------
        # CODEINE — CYP2D6
        # ----------------------------------------
        if drug == "CODEINE":

            if phenotype == "PM":
                return {
                    "action": "Avoid codeine",
                    "details": "Poor metabolizers cannot convert codeine to morphine effectively. Consider alternative analgesic."
                }

            if phenotype == "UM":
                return {
                    "action": "Avoid codeine",
                    "details": "Ultra-rapid metabolizers convert codeine to morphine rapidly, increasing toxicity risk."
                }

            if phenotype == "IM":
                return {
                    "action": "Use caution",
                    "details": "Intermediate metabolizers may have reduced analgesic response. Monitor efficacy."
                }

            return {
                "action": "Standard dosing",
                "details": "Normal CYP2D6 function supports standard dosing."
            }

        # ----------------------------------------
        # CLOPIDOGREL — CYP2C19
        # ----------------------------------------
        if drug == "CLOPIDOGREL":

            if phenotype == "PM":
                return {
                    "action": "Use alternative therapy",
                    "details": "Poor metabolizers have reduced activation of clopidogrel. Consider prasugrel or ticagrelor."
                }

            if phenotype == "IM":
                return {
                    "action": "Consider alternative therapy",
                    "details": "Intermediate metabolizers may have reduced antiplatelet effect. Consider alternative therapy."
                }

            return {
                "action": "Standard dosing",
                "details": "Normal metabolizers can use standard dosing."
            }

        # ----------------------------------------
        # WARFARIN — CYP2C9
        # ----------------------------------------
        if drug == "WARFARIN":

            if phenotype in ["PM", "IM"]:
                return {
                    "action": "Dose reduction recommended",
                    "details": "Reduced CYP2C9 activity decreases warfarin metabolism. Initiate lower dose and monitor INR closely."
                }

            return {
                "action": "Standard dosing",
                "details": "Normal CYP2C9 function supports standard initiation dosing."
            }

        # ----------------------------------------
        # SIMVASTATIN — SLCO1B1
        # ----------------------------------------
        if drug == "SIMVASTATIN":

            if phenotype == "Poor":
                return {
                    "action": "Avoid high doses",
                    "details": "Poor SLCO1B1 function increases simvastatin plasma levels and myopathy risk."
                }

            if phenotype == "Reduced":
                return {
                    "action": "Use lower dose",
                    "details": "Reduced transporter function increases statin exposure. Consider lower dose."
                }

            return {
                "action": "Standard dosing",
                "details": "Normal transporter function supports standard dosing."
            }

        # ----------------------------------------
        # AZATHIOPRINE — TPMT
        # ----------------------------------------
        if drug == "AZATHIOPRINE":

            if phenotype == "PM":
                return {
                    "action": "Avoid or drastically reduce dose",
                    "details": "Poor TPMT activity increases risk of severe myelosuppression."
                }

            if phenotype == "IM":
                return {
                    "action": "Reduce dose",
                    "details": "Intermediate TPMT activity increases toxicity risk. Start with reduced dose."
                }

            return {
                "action": "Standard dosing",
                "details": "Normal TPMT activity supports standard dosing."
            }

        # ----------------------------------------
        # FLUOROURACIL — DPYD
        # ----------------------------------------
        if drug == "FLUOROURACIL":

            if phenotype == "PM":
                return {
                    "action": "Avoid or major dose reduction",
                    "details": "DPD deficiency significantly increases risk of life-threatening toxicity."
                }

            if phenotype == "IM":
                return {
                    "action": "Reduce initial dose",
                    "details": "Partial DPD deficiency increases toxicity risk. Start with reduced dose."
                }

            return {
                "action": "Standard dosing",
                "details": "Normal DPD activity supports standard dosing."
            }

        # Default fallback
        return {
            "action": "Unknown",
            "details": "No CPIC guideline available for this drug."
        }
