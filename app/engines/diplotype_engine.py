class DiplotypeEngine:

    @staticmethod
    def build_diplotype(star_allele: str, genotype: str):
        """
        Converts genotype like 0/1 and star allele into diplotype.
        0 = reference (*1)
        1 = variant (*X)
        """

        alleles = genotype.split("/")

        diplotype = []
        for g in alleles:
            if g == "0":
                diplotype.append("*1")
            else:
                diplotype.append(f"*{star_allele}")

        return f"{diplotype[0]}/{diplotype[1]}"
