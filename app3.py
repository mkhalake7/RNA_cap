import base64
from fastapi import FastAPI, Query
from pydantic import BaseModel
import RNA
import cairosvg

app = FastAPI()

class RNAData(BaseModel):
    seq: str = Query(..., description="RNA sequence")
    ss: str = Query(..., description="Secondary structure")

def generate_rna_png(seq: str, ss: str) -> bytes:
    # Ensure that the sequence and structure have the same length
    if len(seq) != len(ss):
        raise ValueError("RNA sequence and secondary structure must have the same length.")

    # Calculate the secondary structure using viennaRNA
    fc, mfe_structure = RNA.fold(seq)

    # Check if the calculated secondary structure matches the input structure
    if mfe_structure != ss:
        raise ValueError("The calculated secondary structure does not match the provided secondary structure.")

    # Generate the SVG representation of the secondary structure
    svg_data = RNA.svg_rna_plot(seq, ss)

    # Convert SVG to PNG using cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_data)

    return png_data

@app.get("/generate_png/")
async def generate_png(data: RNAData):
    try:
        png_data = generate_rna_png(data.seq, data.ss)
        # Encode the PNG image data as base64
        encoded_png = base64.b64encode(png_data).decode("utf-8")
        return {"png_image": encoded_png}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
