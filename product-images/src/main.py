import os
import sys
from PIL import Image, ImageOps

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../")
)
sys.path.append(ROOT_DIR)

from shared.spreadsheet.reader import read_spreadsheet
from shared.validation.rules import validate_image

# Configurations
SPREADSHEET_PATH = "scripts/validate-image/product-images/data/product_references.xlsx"
IMAGE_DIR = "scripts/validate-image/product-images/data/product_images/"
MAX_IMAGE_SIZE_BYTES = 5000000  # 5 MB
EXPECTED_DIMENSIONS = (1024, 768)  # width, height

# Read product references from spreadsheet
product_references = read_spreadsheet(SPREADSHEET_PATH, column="Referencia")

for file in os.listdir(IMAGE_DIR):
    if not file.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    path = os.path.join(IMAGE_DIR, file)

    size_kb = os.path.getsize(path) / 1024  # size in KB

    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        width, height = img.size

# Validate images for each product reference
results = []

for reference in product_references:
    status = "Image invalid or not found"
    for archive in os.listdir(IMAGE_DIR):



        if reference in archive:
            path = os.path.join(IMAGE_DIR, archive)
            if validate_image(path, MAX_IMAGE_SIZE_BYTES, EXPECTED_DIMENSIONS):
                status = "Valid image"
                print(f"DEBUG | {file} | size={size_kb:.2f}kb | res={width}x{height} | status={status}")
                break
    results.append({"Referência": reference, "Status": status})

# Print results
import pandas as pd
df_results = pd.DataFrame(results)
df_results.to_csv("scripts/validate-image/product-images/data/reports/image_status.csv", index = False)
print("Image validation report generated at ../../../data/reports/image_status.csv")