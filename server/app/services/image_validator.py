import os
import shutil
from pathlib import Path

from fastapi import UploadFile
from PIL import Image, ImageOps

from app.shared.validation.rules import sanitize_filename, validate_nomenclature

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

BATCH_DIR = Path("data/batches")
BATCH_DIR.mkdir(parents=True, exist_ok=True)

JPEG_EXTENSIONS = {".jpg", ".jpeg"}


def _normalize_expected_extensions(expected_extensions: str | None) -> set[str]:
    if expected_extensions is None:
        return set()

    normalized: set[str] = set()
    for raw_extension in expected_extensions.split(","):
        clean_extension = raw_extension.strip().lower().lstrip(".")
        if clean_extension:
            normalized.add(f".{clean_extension}")
    return normalized


def _save_canvas(canvas: Image.Image, output_path: Path, source_extension: str) -> None:
    if source_extension in JPEG_EXTENSIONS:
        canvas.save(output_path, format="JPEG", quality=92, optimize=True)
        return

    canvas.save(output_path)


def _resize_with_white_padding(
    source_path: Path,
    output_path: Path,
    target_width: int,
    target_height: int,
) -> dict:
    if target_width <= 0 or target_height <= 0:
        raise ValueError("Target dimensions must be greater than zero.")

    with Image.open(source_path) as original_image:
        transposed_image = ImageOps.exif_transpose(original_image).convert("RGB")
        original_width, original_height = transposed_image.size

        scale = min(target_width / original_width, target_height / original_height)
        fitted_width = max(1, int(round(original_width * scale)))
        fitted_height = max(1, int(round(original_height * scale)))

        if (fitted_width, fitted_height) != transposed_image.size:
            transposed_image = transposed_image.resize(
                (fitted_width, fitted_height),
                Image.Resampling.LANCZOS,
            )

        canvas = Image.new("RGB", (target_width, target_height), "#FFFFFF")
        offset_x = (target_width - fitted_width) // 2
        offset_y = (target_height - fitted_height) // 2
        canvas.paste(transposed_image, (offset_x, offset_y))

        _save_canvas(canvas, output_path, source_path.suffix.lower())

    return {
        "original_size": (original_width, original_height),
        "fitted_size": (fitted_width, fitted_height),
        "canvas_size": (target_width, target_height),
        "adjusted": (original_width, original_height) != (target_width, target_height),
    }


def validate_image_service(
    uploaded_file: UploadFile,
    max_size_mb: float | None,
    expected_width: int | None,
    expected_height: int | None,
    expected_extensions: str | None,
):
    checks: list[dict] = []

    safe_filename = sanitize_filename(uploaded_file.filename)
    original_file_path = UPLOAD_DIR / safe_filename

    with open(original_file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    output_file_path = original_file_path
    requested_resize = expected_width is not None or expected_height is not None

    allowed_extensions = _normalize_expected_extensions(expected_extensions)
    uploaded_extension = Path(uploaded_file.filename).suffix.lower()

    if allowed_extensions:
        if uploaded_extension not in allowed_extensions:
            checks.append(
                {
                    "name": "Formato",
                    "status": "error",
                    "value": uploaded_extension.lstrip(".") or "sem extensão",
                    "errors": [
                        {
                            "code": "invalid_format",
                            "message": f"O formato do arquivo deve ser {expected_extensions}.",
                        }
                    ],
                }
            )
        else:
            checks.append(
                {
                    "name": "Formato",
                    "status": "ok",
                    "value": uploaded_extension.lstrip("."),
                    "errors": None,
                }
            )

    if requested_resize and (expected_width is None or expected_height is None):
        checks.append(
            {
                "name": "Ajuste automático",
                "status": "error",
                "value": "Parâmetros incompletos",
                "errors": [
                    {
                        "code": "invalid_target_dimensions",
                        "message": "Informe largura e altura para aplicar o ajuste automático.",
                    }
                ],
            }
        )
    elif expected_width is not None and expected_height is not None:
        if expected_width <= 0 or expected_height <= 0:
            checks.append(
                {
                    "name": "Ajuste automático",
                    "status": "error",
                    "value": f"{expected_width}x{expected_height}",
                    "errors": [
                        {
                            "code": "invalid_target_dimensions",
                            "message": "As dimensões esperadas devem ser maiores que zero.",
                        }
                    ],
                }
            )
        else:
            adjusted_output_path = original_file_path.with_name(
                f"{original_file_path.stem}__autofit{original_file_path.suffix}"
            )
            resize_metadata = _resize_with_white_padding(
                source_path=original_file_path,
                output_path=adjusted_output_path,
                target_width=expected_width,
                target_height=expected_height,
            )
            output_file_path = adjusted_output_path

            original_width, original_height = resize_metadata["original_size"]
            fitted_width, fitted_height = resize_metadata["fitted_size"]
            canvas_width, canvas_height = resize_metadata["canvas_size"]
            adjusted_label = "Aplicado" if resize_metadata["adjusted"] else "Não necessário"

            checks.append(
                {
                    "name": "Ajuste automático",
                    "status": "ok",
                    "value": (
                        f"{adjusted_label} | Original: {original_width}x{original_height} | "
                        f"Ajustada: {fitted_width}x{fitted_height} | Canvas: {canvas_width}x{canvas_height}"
                    ),
                    "errors": None,
                }
            )
            checks.append(
                {
                    "name": "Dimensões",
                    "status": "ok",
                    "value": f"Canvas final: {canvas_width}x{canvas_height}",
                    "errors": None,
                }
            )

    if max_size_mb is not None:
        max_size_bytes = max_size_mb * 1024 * 1024
        original_size_bytes = os.path.getsize(original_file_path)
        original_size_mb = original_size_bytes / 1024 / 1024

        if original_size_bytes > max_size_bytes:
            checks.append(
                {
                    "name": "Tamanho",
                    "status": "error",
                    "value": f"Original: {original_size_mb:.2f} mb",
                    "errors": [
                        {
                            "code": "file_too_large",
                            "message": f"O tamanho do arquivo excede o limite de {max_size_mb} mb.",
                        }
                    ],
                }
            )
        else:
            checks.append(
                {
                    "name": "Tamanho",
                    "status": "ok",
                    "value": f"Original: {original_size_mb:.2f} mb",
                    "errors": None,
                }
            )

        if output_file_path != original_file_path:
            adjusted_size_bytes = os.path.getsize(output_file_path)
            adjusted_size_mb = adjusted_size_bytes / 1024 / 1024
            checks.append(
                {
                    "name": "Tamanho (arquivo ajustado)",
                    "status": "ok",
                    "value": f"Ajustado: {adjusted_size_mb:.2f} mb",
                    "errors": None,
                }
            )

    if not validate_nomenclature(uploaded_file.filename):
        checks.append(
            {
                "name": "Nomenclatura",
                "status": "error",
                "value": uploaded_file.filename,
                "errors": [
                    {
                        "code": "invalid_nomenclature",
                        "message": "A nomenclatura não corresponde ao esperado (ex: 9999 99 99999#1.jpg).",
                    }
                ],
            }
        )
    else:
        checks.append(
            {
                "name": "Nomenclatura",
                "status": "ok",
                "value": uploaded_file.filename,
                "errors": None,
            }
        )

    approved = not any(check["status"] == "error" for check in checks)
    output_file_url = f"/uploads/{output_file_path.name}"

    return {
        "stage": "validation",
        "approved": approved,
        "summary": "Imagem validada com sucesso" if approved else "Falha na validação da imagem",
        "file_url": output_file_url,
        "download_url": output_file_url,
        "is_adjusted_output": output_file_path != original_file_path,
        "output_filename": output_file_path.name,
        "checks": checks,
    }
