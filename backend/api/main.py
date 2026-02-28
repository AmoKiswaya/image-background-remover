from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from rembg import remove
from PIL import Image  
import io 

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"} 


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)) -> Response:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Can't support this file type. Allowed types: PNG, JPEG or JPG"
        )
    
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()