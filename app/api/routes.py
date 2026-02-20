from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import tempfile
import os

from app.schemas.output_schema import PharmacogenomicResponse
from app.services.patient_processor import PatientProcessor
from app.services.vcf_parser import parse_vcf

router = APIRouter()


@router.post(
    "/analyze",
    response_model=List[PharmacogenomicResponse]
)
async def analyze(
    file: UploadFile = File(...),
    drugs: str = Form(...)
):
    # -----------------------------------
    # 1️⃣ Validate file extension
    # -----------------------------------
    print("🔥 /analyze endpoint hit")
    if not file.filename.endswith((".vcf", ".vcf.gz")):
        raise HTTPException(
            status_code=400,
            detail="Only .vcf or .vcf.gz files are supported"
        )

    # -----------------------------------
    # 2️⃣ Validate file size (≤ 5MB)
    # -----------------------------------
    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File exceeds 5MB limit"
        )

    # -----------------------------------
    # 3️⃣ Save file temporarily (preserve extension)
    # -----------------------------------
    suffix = ".vcf.gz" if file.filename.endswith(".vcf.gz") else ".vcf"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        temp_path = tmp.name

    try:
        # -----------------------------------
        # 4️⃣ Parse VCF
        # -----------------------------------
        parsed_data = parse_vcf(temp_path)
        print("PARSED:", parsed_data)


        if not parsed_data["vcf_metadata"]["parsing_success"]:
            raise HTTPException(
                status_code=400,
                detail="VCF parsing failed"
            )

        # -----------------------------------
        # 5️⃣ Process drugs
        # -----------------------------------
        drug_list = [d.strip().upper() for d in drugs.split(",")]

        results = PatientProcessor.process(parsed_data, drug_list)

        return results

    finally:
        # -----------------------------------
        # 6️⃣ Always cleanup temp file
        # -----------------------------------
        if os.path.exists(temp_path):
            os.remove(temp_path)
