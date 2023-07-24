from fastapi import FastAPI, Query
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any
import RNA
import cairosvg
import io

app = FastAPI()

def generate_rna_png(seq: str, ss: str) -> bytes:
    fc, mfe_structure = RNA.fold(seq)
    svg_data = RNA.draw_rna(seq, mfe_structure)
    png_data = cairosvg.svg2png(bytestring=svg_data)
    return png_data

@app.get("/generate_png/")
async def generate_png(seq: str = Query(..., description="RNA sequence"),
                       ss: str = Query(..., description="Secondary structure")):
    try:
        png_data = generate_rna_png(seq, ss)
        return {"png_image": png_data}
    except Exception as e:
        return {"error": str(e)}

# Function to customize the OpenAPI schema to include servers information
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RNA Secondary Structure API",
        version="1.0.0",
        description="API to generate PNG image of RNA secondary structure using viennaRNA and cairosvg.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png",
        "altText": "RNA Secondary Structure API",
    }
    openapi_schema["servers"] = [{"url": "http://127.0.0.1:8000"}]  # Update with your server URL
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
