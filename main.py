from PIL import Image
import base64
import io
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
from typing import Union
from fastapi import FastAPI, UploadFile

app = FastAPI()


def process_image_with_cpu_model(image):
    processor = BlipProcessor.from_pretrained("./model")
    model = BlipForConditionalGeneration.from_pretrained("./model")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    answer = processor.decode(out[0], skip_special_tokens=True)



@app.post("/upload")
async def create_upload_file(file: UploadFile):
    try:
        print("test")
        image_data = await file.read()
        print("Received image data:", image_data)
        image = Image.open(io.BytesIO(image_data))
        result_caption = process_image_with_cpu_model(image)
        return result_caption
    except Exception as e:
        print("Error:", str(e))
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)