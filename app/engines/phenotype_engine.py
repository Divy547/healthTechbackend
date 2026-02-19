from app.core.constants import PHENOTYPE_TABLES


class PhenotypeEngine:

    @staticmethod
    def get_phenotype(gene: str, diplotype: str):

        gene_table = PHENOTYPE_TABLES.get(gene)

        if not gene_table:
            return "Unknown"

        return gene_table.get(diplotype, "Unknown")
