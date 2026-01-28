import re
from pathlib import Path
from app.shared.image.metadata import get_size, get_dimensions


def sanitize_filename(filename: str) -> str:
    if not filename:
        raise ValueError("Filename inválido")

    name = Path(filename).stem
    ext = Path(filename).suffix

    name = name.lower()
    name = re.sub(r"[^\w\-]", "_", name)  # remove espaces, #, etc
    name = re.sub(r"_+", "_", name)

    return f"{name}{ext}"