from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from rembg import remove
from PIL import Image, UnidentifiedImageError  
import io 

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"} 


def downscale_image(image: Image.Image) -> Image.Image:
    pass 

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)) -> Response:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="File type not supported. Allowed types: PNG, JPEG or JPG"
        )
    
    image_bytes = await file.read()

    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Could not read image file")

    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    output_bytes = buffer.getvalue()

    return Response(content=output_bytes, media_type="image/png")