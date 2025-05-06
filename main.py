from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image, ImageEnhance
import io
import os
import uvicorn

app = FastAPI()

@app.post("/tint-image/")
async def tint_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGBA")
    print(f"Received image: {file.filename}, size: {image.size}, mode: {image.mode}")
    grayscale_image = image.convert("L")

    img_byte_arr = io.BytesIO()
    grayscale_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")


if __name__ == "__main__":
    print("Starting Service 2")
    port = int(os.getenv("PORT", 8001))
    print(f"Service 2 running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)