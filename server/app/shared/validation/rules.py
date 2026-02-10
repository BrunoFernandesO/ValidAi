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


def validate_nomenclature(filename: str) -> bool:
    if not filename:
        raise ValueError("Filename inválido")
    
    name = Path(filename).stem
    rule = "^\d{4} \d{2} \d{5}#\d$"
    
    if re.match(rule, name):
        return True
    return False