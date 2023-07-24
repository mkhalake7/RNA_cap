from fastapi import FastAPI, Query
import cairosvg
import RBA

app = FastAPI()

@app.get("/generate_png/")
async def generate_png(seq: str = Query(..., description="RNA sequence"),
                       ss: str = Query(..., description="Secondary structure")):
    fc, mfe_struct = RNA.fold_compound(seq)

    # Generate the PNG using cairosvg
    # Example:
    svg_data = f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="300" height="200">
            <text x="10" y="20">RNA Sequence: {seq}</text>
            <text x="10" y="40">Secondary Structure: {ss}</text>
            <text x="10" y="60">Free Energy: {fc}</text>
            <text x="10" y="80">MFE Structure: {mfe_struct}</text>
        </svg>
    """
    png_data = cairosvg.svg2png(bytestring=svg_data.encode())

    return {
        "png_image": png_data,
        "RNA_sequence": seq,
        "Secondary_structure": ss,
        "Free_energy": fc,
        "MFE_structure": mfe_struct
    }
    # print(seq)
    # print(ss)

    # return {"message": "API not implemented yet!"}

# Add Swagger UI at /docs and ReDoc at /redoc
if __name__ == "__main__":
    import uvicorn
    from fastapi.openapi.docs import get_swagger_ui_html
    from fastapi.openapi.utils import get_openapi

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="RNA API Docs")

    @app.get("/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint():
        return get_openapi(title="RNA API", version="1.0.0", routes=app.routes)

    uvicorn.run(app, host="0.0.0.0", port=8000)
