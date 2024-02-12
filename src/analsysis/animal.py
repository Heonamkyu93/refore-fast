from keras.models import load_model  # TensorFlow is required for Keras to work
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException,APIRouter
from PIL import Image, ImageOps
import io

app = FastAPI()

model_path = 'E:/dev/fast/refore-inference/src/analsysis/keras_model.h5'
model = load_model(model_path)
text_path = 'E:/dev/fast/refore-inference/src/analsysis/labels.txt'

class_names = [line.strip() for line in open(text_path, 'r', encoding='utf-8')]

animal_router = APIRouter(prefix="/in")

@animal_router.post("/img")
async def upload_image(file: UploadFile = File(...)):
    # 파일 확장자 검사
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    # 이미지 읽기
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    
    # 이미지 처리
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    # 예측
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    return {"class": class_name, "confidence": float(confidence_score)}

app.include_router(animal_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
