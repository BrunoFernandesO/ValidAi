from typing import List
from fastapi import APIRouter, UploadFile, File
from app.api.schemas import ValidationResponse
from app.services.image_validator import validate_image_service

router = APIRouter(prefix="/api", tags=["validation"])

@router.post("/validate", response_model=ValidationResponse)
async def validate_image(files: List[UploadFile] = File(...)):
    results = []

    approved_count = 0
    failed_count = 0

    for file in files:
        result = validate_image_service(file)

        if result["approved"]:
            approved_count += 1
        else:
            failed_count += 1

        results.append({
            "filename": file.filename,
            **result
        })

    return {
        "total": len(files),
        "approved": approved_count,
        "failed": failed_count,
        "results": results
    }