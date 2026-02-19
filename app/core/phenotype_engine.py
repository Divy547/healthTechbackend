class PhenotypeEngine:

    @staticmethod
    def get_phenotype(gene: str, diplotype: str):

        tables = {
            "CYP2C19": CYP2C19_TABLE,
            "DPYD": DPYD_TABLE
        }

        gene_table = tables.get(gene, {})
        return gene_table.get(diplotype, "Unknown")
