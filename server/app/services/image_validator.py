import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from PIL import Image, ImageOps

# from app.shared.validation.rules import validate_rules

UPLOAD_DIR = Path("server/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def validate_image_service(uploaded_file: UploadFile):

   # from app.shared.spreadsheet.reader import read_spreadsheet

    # Configurations
    #SPREADSHEET_PATH = "data/spreadsheet/product_references.xlsx"
    MAX_IMAGE_SIZE_BYTES = 5242880  # 5 MB
    EXPECTED_DIMENSIONS = (1024, 768)  # width, height

    # Read product references from spreadsheet
    #product_references = read_spreadsheet(SPREADSHEET_PATH, column="Referencia")

    # Save uploaded file to disk
    file_path = UPLOAD_DIR / uploaded_file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    checks = []

    EXPECTED_FORMATS = ".jpg"

    # Validate file format
    if not uploaded_file.filename.lower().endswith(EXPECTED_FORMATS):
        return {
            "approved": False,
            "summary": "Formato inválido",
            "checks": [{
            "name": "Formato do arquivo",
            "status": "error",
            "errors": [{
                "code": "invalid_format",
                "message": [f"O formato do arquivo deve ser {EXPECTED_FORMATS}."]
            }]
            }]
        }
    
    # Validate file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_IMAGE_SIZE_BYTES:
        checks.append({
            "name": "Tamanho do arquivo",
            "status": "error",
            "value": str(f"{file_size / 1024 / 1024:.2f}") + " mb",
            "errors": [{
                "code": "file_too_large",
                "message": [f"O tamanho do arquivo excede o limite de {MAX_IMAGE_SIZE_BYTES / 1024 / 1024} mb."]
            }]
        })
    else:
        checks.append({
            "name": "Tamanho do arquivo",
            "status": "ok",
            "value": str(f"{file_size / 1024 / 1024:.2f}") + " mb",
            "errors": None
        })

    # Validate image dimensions
    with Image.open(file_path) as img:
        img = ImageOps.exif_transpose(img)
        width, height = img.size

    if (width, height) != EXPECTED_DIMENSIONS:
        checks.append({
            "name": "Dimensões da imagem",
            "status": "error",
            "value": f"{width}x{height}",
            "errors": [{
                "code": "invalid_dimensions",
                "message": [f"As dimensões da imagem devem ser {EXPECTED_DIMENSIONS[0]}x{EXPECTED_DIMENSIONS[1]} pixels."]
            }]
        })
    else: 
        checks.append({
            "name": "Dimensões da imagem",
            "status": "ok",
            "value": f"{width}x{height}",
            "errors": None
        })


    approved = not any(c["status"] == "error" for c in checks)

    return {
        "approved": approved,
        "summary": "Imagem validada com sucesso" if approved else "Falha na validação da imagem",
        "checks": checks
    }


   # results = []

    #for reference in product_references:
    #    for archive in os.listdir(IMAGE_DIR):
#
 #           if reference in archive:
#
#
 #               if not errors:
  #                  status = True
   #             else:
    #                status = False
     #           break

        #results.append({"Referencia": reference, "Status": status, "Erros": errors if errors != True else None})

#return results
