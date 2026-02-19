import gzip
from datetime import datetime, timezone


TARGET_GENES = {
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "SLCO1B1",
    "TPMT",
    "DPYD"
}


def open_vcf(file_path):
    if file_path.endswith(".gz"):
        return gzip.open(file_path, "rt")
    return open(file_path, "r")


def parse_info(info_string):
    info_dict = {}
    if info_string == ".":
        return info_dict

    for item in info_string.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            info_dict[key] = value
        else:
            info_dict[item] = True
    return info_dict


def parse_vcf(file_path, patient_id=None):
    result = {
        "patient_id": patient_id if patient_id else file_path.split("/")[-1].replace(".vcf.gz", "").replace(".vcf", ""),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vcf_metadata": {
            "file_format": None,
            "parsing_success": False,
            "total_variants_scanned": 0,
            "pharmacogene_variants_detected": 0
        },
        "pharmacogene_variants": []
    }

    try:
        with open_vcf(file_path) as f:
            for line in f:
                line = line.strip()

                # Meta lines
                if line.startswith("##"):
                    if line.startswith("##fileformat="):
                        result["vcf_metadata"]["file_format"] = line.split("=")[1]
                    continue

                # Header line
                if line.startswith("#CHROM"):
                    continue

                # Data lines
                columns = line.split("\t")

                if len(columns) < 8:
                    continue

                result["vcf_metadata"]["total_variants_scanned"] += 1

                chrom = columns[0]
                pos = columns[1]
                rsid = columns[2]
                ref = columns[3]
                alt = columns[4]
                filter_status = columns[6]
                info = columns[7]

                if filter_status not in ["PASS", "."]:
                    continue

                info_dict = parse_info(info)

                gene = (
                    info_dict.get("GENE")
                    or info_dict.get("Gene")
                    or info_dict.get("SYMBOL")
                )

                if not gene:
                    continue

                gene = gene.upper()

                if gene not in TARGET_GENES:
                    continue

                # Extract genotype
                genotype = None
                if len(columns) > 9:
                    format_keys = columns[8].split(":")
                    sample_values = columns[9].split(":")
                    format_dict = dict(zip(format_keys, sample_values))
                    genotype = format_dict.get("GT")

                # Clean star allele (remove *)
                star_raw = info_dict.get("STAR")
                star_clean = star_raw.replace("*", "") if star_raw else None

                result["pharmacogene_variants"].append({
                    "gene": gene,
                    "rsid": rsid,
                    "star_allele": star_clean,
                    "genotype": genotype,
                    "ref": ref,
                    "alt": alt,
                    "position": pos,
                    "filter_status": filter_status
                })

                result["vcf_metadata"]["pharmacogene_variants_detected"] += 1

        result["vcf_metadata"]["parsing_success"] = True

    except Exception as e:
        result["vcf_metadata"]["parsing_success"] = False
        result["error"] = str(e)

    return result
