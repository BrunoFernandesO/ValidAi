import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from PIL import Image, ImageOps
from app.shared.validation.rules import sanitize_filename
from app.shared.validation.rules import validate_nomenclature

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _resize_with_white_padding(
    image_path: Path,
    target_width: int,
    target_height: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Resize (only downscale) and center image on a white canvas."""
    with Image.open(image_path) as original_img:
        img = ImageOps.exif_transpose(original_img).convert("RGB")
        original_size = img.size

        scale = min(target_width / img.width, target_height / img.height)
        should_downscale = scale < 1

        if should_downscale:
            resized_width = max(1, int(round(img.width * scale)))
            resized_height = max(1, int(round(img.height * scale)))
            img = img.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (target_width, target_height), "#FFFFFF")
        offset_x = (target_width - img.width) // 2
        offset_y = (target_height - img.height) // 2
        canvas.paste(img, (offset_x, offset_y))

        if image_path.suffix.lower() in {".jpg", ".jpeg"}:
            canvas.save(image_path, quality=95, optimize=True)
        else:
            canvas.save(image_path)

    return original_size, (target_width, target_height)

def validate_image_service(uploaded_file: UploadFile, max_size_mb: float | None, expected_width: int | None, expected_height: int | None, expected_extensions: str | None):
    
    f"Esperado: {expected_extensions}, {max_size_mb}mb, {expected_width}x{expected_height}px"
    
    if max_size_mb is not None:
        max_size_bytes = max_size_mb * 1024 * 1024 
        

    # Save uploaded file
    safe_filename = sanitize_filename(uploaded_file.filename)
    file_path = UPLOAD_DIR / safe_filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    file_url = f"/uploads/{safe_filename}"
    

    checks = []
    
    # Validate file format
    if expected_extensions:   
        file_extension = Path(uploaded_file.filename).suffix.lower()
        allowed_formats = [f.lower().lstrip('.') for f in expected_extensions.split(',')]
        if not any(file_extension.lstrip('.') == fmt or file_extension == f'.{fmt}' for fmt in allowed_formats):
            return {
                "approved": False,
                "summary": "Formato inválido",
                "checks": [{
                "name": "Formato",
                "status": "error",
                "errors": [{
                    "code": "invalid_format",
                    "message": f"O formato do arquivo deve ser {expected_extensions}."
                }]
                }]
            }
    
    # Resize/fit image into expected dimensions without distortion
    if expected_width is not None and expected_height is not None:
        original_size, (width, height) = _resize_with_white_padding(
            file_path,
            expected_width,
            expected_height,
        )

        checks.append({
            "name": "Ajuste automático",
            "status": "ok",
            "value": (
                f"Original: {original_size[0]}x{original_size[1]} -> "
                f"Canvas: {width}x{height} (fundo branco)"
            ),
            "errors": None
        })

        checks.append({
            "name": "Dimensões",
            "status": "ok",
            "value": f"{width}x{height}",
            "errors": None
        })

    # Validate file size
    if max_size_mb:
        file_size = os.path.getsize(file_path)
        if file_size > max_size_bytes:
            checks.append({
                "name": "Tamanho",
                "status": "error",
                "value": str(f"{file_size / 1024 / 1024:.2f}") + " mb",
                "errors": [{
                    "code": "file_too_large",
                    "message": f"O tamanho do arquivo excede o limite de {max_size_mb} mb."
                }]
            })
        else:
            checks.append({
                "name": "Tamanho",
                "status": "ok",
                "value": str(f"{file_size / 1024 / 1024:.2f}") + " mb",
                "errors": None
            })
        
    # Validate nomenclature
    if not validate_nomenclature(uploaded_file.filename):
        checks.append({
            "name": "Nomenclatura",
            "status": "error",
            "value": uploaded_file.filename,
            "errors": [{
                "code": "invalid_nomenclature",
                "message": "A nomenclatura não corresponde ao esperado (ex: 9999 99 99999#1.jpg)."
            }]
        })
    else:
        checks.append({
            "name": "Nomenclatura",
            "status": "ok",
            "value": uploaded_file.filename,
            "errors": None        
    })

    approved = not any(c["status"] == "error" for c in checks)

    return {
        "stage": "validation",
        "approved": approved,
        "summary": "Imagem validada com sucesso" if approved else "Falha na validação da imagem",
        "file_url": file_url,
        "checks": checks
    }
