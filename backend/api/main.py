from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from rembg import remove
from PIL import Image, UnidentifiedImageError  
import io 

MAX_DIMENSION = 1500 

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"} 


def downscale_image(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")

    if max(image.width, image.height) <= MAX_DIMENSION:
        return image

    scale_factor = MAX_DIMENSION / max(image.width, image.height)
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor) 

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)  

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

    image = downscale_image(image) 
    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    output_bytes = buffer.getvalue()

    return Response(content=output_bytes, media_type="image/png")