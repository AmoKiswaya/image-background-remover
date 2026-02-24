from fastapi import FastAPI, UploadFile, File
from rembg import remove
from PIL import Image  
import io 

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"} 


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()