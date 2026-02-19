class DiplotypeEngine:

    @staticmethod
    def build_diplotype(star_allele: str, genotype: str):
        alleles = genotype.split("/")

        allele_map = []
        for g in alleles:
            if g == "0":
                allele_map.append("*1")
            else:
                allele_map.append(f"*{star_allele}")

        return f"{allele_map[0]}/{allele_map[1]}"
