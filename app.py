from fastapi import FastAPI, Query
import subprocess
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.get("/predict/")
async def predict_structure(seq: str = Query(..., title="RNA sequence"), ss: str = Query(..., title="Secondary Structure")):
    # Prepare the RNA input file
    with open("rna_input.seq", "w") as f:
        f.write(f"{seq}\n{ss}\n")

    # Run RNAfold command to get the MGE structure in dot-bracket notation
    subprocess.run(["RNAfold", "-i", "rna_input.seq", "-o", "rna_output"])

    # Read the resulting dot-bracket structure
    with open("rna_output") as f:
        structure = f.readlines()[1].strip()

    # Create the PNG image from the dot-bracket structure using PIL
    svg_content = f"({seq})[{structure}]"
    pil_image = Image.new("RGB", (100, 100), (255, 255, 255))  # Replace (100, 100) with your desired image size
    pil_image.save("rna_structure.png")

    # Return the PNG image
    with open("rna_structure.png", "rb") as f:
        png_data = f.read()

    return {"png_image": png_data}
