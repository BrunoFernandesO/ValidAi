from app.shared.image.metadata import get_size, get_dimensions

def validate_rules(path, max_size_bytes, expected_dimensions):
    size = get_size(path)
    dimensions = get_dimensions(path)

    if size < max_size_bytes and dimensions == expected_dimensions:
        return True
    else:
        errors = []
        if size >= max_size_bytes:
            errors.append(f"Tamanho invalido: {size} bytes (maximo permitido: {max_size_bytes} bytes)")
            if dimensions != expected_dimensions:
                errors.append(f"Dimensoes invalidas: {dimensions} (esperado: {expected_dimensions})")
        return errors