from typing import List
from fastapi import APIRouter, UploadFile, File
from app.api.schemas import ValidationResponse
from app.services.image_validator import validate_image_service

router = APIRouter(prefix="/api", tags=["validation"])

@router.post("/validate", response_model=ValidationResponse)
async def validate_image(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        result = validate_image_service(file)

        results.append({
            "filename": file.filename,
            **result
        })
    
    return {"results": results}