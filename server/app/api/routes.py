from fastapi import APIRouter, UploadFile, File
from app.api.schemas import ValidationResult
from app.services.image_validator import validate_image_service

router = APIRouter(prefix="/api", tags=["validation"])

@router.post("/validate", response_model=ValidationResult)
async def validate_image(file: UploadFile = File(...)):
    return validate_image_service(file)
