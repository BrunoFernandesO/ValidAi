import uuid
import zipfile
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, Form, UploadFile

from app.api.schemas import ValidationResponse
from app.services.image_validator import BATCH_DIR, UPLOAD_DIR, validate_image_service

router = APIRouter(prefix="/api", tags=["validation"])


@router.post("/validate", response_model=ValidationResponse)
async def validate_image(
    files: List[UploadFile] = File(...),
    max_size: float | None = Form(None),
    expected_width: int | None = Form(None),
    expected_height: int | None = Form(None),
    expected_extensions: str | None = Form(None),
):
    results = []

    for file in files:
        result = validate_image_service(
            file,
            max_size,
            expected_width,
            expected_height,
            expected_extensions,
        )
        results.append({"filename": file.filename, **result})

    adjusted_outputs = [
        item["output_filename"]
        for item in results
        if item.get("is_adjusted_output") is True
    ]

    batch_download_url = None
    if len(adjusted_outputs) > 1:
        batch_id = uuid.uuid4().hex
        zip_name = f"adjusted_images_{batch_id}.zip"
        zip_path = BATCH_DIR / zip_name

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for output_name in adjusted_outputs:
                output_path = UPLOAD_DIR / output_name
                if output_path.exists():
                    archive.write(output_path, arcname=output_name)

        batch_download_url = f"/batches/{zip_name}"

    sanitized_results = [
        {
            key: value
            for key, value in result.items()
            if key not in {"is_adjusted_output", "output_filename"}
        }
        for result in results
    ]

    return {"results": sanitized_results, "batch_download_url": batch_download_url}
