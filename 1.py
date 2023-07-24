from fastapi import FastAPI, Query
import subprocess
import cairosvg

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

    # Create the PNG image from the dot-bracket structure
    svg_content = f"({seq})[{structure}]"
    png_filename = "rna_structure.png"
    cairosvg.svg2png(bytestring=svg_content, write_to=png_filename)

    # Return the PNG image
    with open(png_filename, "rb") as f:
        png_data = f.read()

    return {"png_image": png_data}
