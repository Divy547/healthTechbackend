SUPPORTED_GENES = [
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "SLCO1B1",
    "TPMT",
    "DPYD"
]


SUPPORTED_DRUGS = [
    "CODEINE",
    "WARFARIN",
    "CLOPIDOGREL",
    "SIMVASTATIN",
    "AZATHIOPRINE",
    "FLUOROURACIL"
]


DRUG_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}


PHENOTYPE_TABLES = {

    "CYP2C19": {
        "*1/*1": "NM",
        "*1/*2": "IM",
        "*2/*2": "PM"
    },

    "DPYD": {
        "*1/*1": "NM",
        "*1/*2A": "IM",
        "*2A/*2A": "PM"
    },

    "CYP2D6": {
        "*1/*1": "NM",
        "*1/*4": "IM",
        "*4/*4": "PM"
    },

    "CYP2C9": {
        "*1/*1": "NM",
        "*1/*2": "IM",
        "*2/*2": "PM"
    },

    "SLCO1B1": {
        "*1/*1": "NM",
        "*1/*5": "IM",
        "*5/*5": "PM"
    },

    "TPMT": {
        "*1/*1": "NM",
        "*1/*3A": "IM",
        "*3A/*3A": "PM"
    }
}
