class ConfidenceEngine:

    @staticmethod
    def calculate(
        variants: list,
        phenotype: str,
        risk_label: str
    ) -> float:

        score = 0.0

        # -----------------------------------
        # 1️⃣ Variant Quality (30%)
        # -----------------------------------
        if variants:
            if all(v.get("filter_status") == "PASS" for v in variants):
                score += 0.30
            else:
                score += 0.15  # partial confidence
        else:
            score += 0.0

        # -----------------------------------
        # 2️⃣ Genotype Clarity (20%)
        # -----------------------------------
        if variants and all("genotype" in v for v in variants):
            score += 0.20

        # -----------------------------------
        # 3️⃣ Phenotype Certainty (20%)
        # -----------------------------------
        if phenotype != "Unknown":
            score += 0.20

        # -----------------------------------
        # 4️⃣ Risk Determinism (20%)
        # -----------------------------------
        if risk_label != "Unknown":
            score += 0.20

        # -----------------------------------
        # 5️⃣ CPIC Coverage (10%)
        # -----------------------------------
        if phenotype in ["PM", "IM", "NM"]:
            score += 0.10

        return round(min(score, 1.0), 2)
