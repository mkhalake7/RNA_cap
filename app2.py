import subprocess
import base64
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class RNAData(BaseModel):
    seq: str = Query(..., description="RNA sequence")
    ss: str = Query(..., description="Secondary structure")

def generate_rna_png(seq: str, ss: str) -> bytes:
    # Write the RNA sequence and secondary structure to temporary files
    seq_file = "seq.txt"
    ss_file = "ss.txt"
    with open(seq_file, "w") as f_seq, open(ss_file, "w") as f_ss:
        f_seq.write(seq)
        f_ss.write(ss)

    # Call the RNAplot command-line tool to generate the image
    output_file = "rna_structure.png"
    subprocess.run(["RNAplot", "--input", seq_file, "--structure", ss_file, "--output-format", "png", "--output", output_file])

    # Read the generated image file
    with open(output_file, "rb") as f_image:
        png_data = f_image.read()

    # Cleanup temporary files
    subprocess.run(["rm", seq_file, ss_file, output_file])

    return png_data

@app.post("/generate_png/")
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
