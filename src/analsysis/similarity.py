from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np
import os
from insightface.app import FaceAnalysis

similarity_router = APIRouter(prefix="/in")

@similarity_router.post("/upimg")
async def upload_img(file: UploadFile = File(...)):
    # 업로드된 파일이 이미지인지 확인
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    try:
        # 파일을 임시 디렉토리에 저장
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # FaceAnalysis 객체 생성 및 설정
        app = FaceAnalysis(providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        # 얼굴 인식 및 처리
        faces = app.get(img)

        # 각 얼굴에 대해 사각형을 그립니다.
        for face in faces:
            bbox = face['bbox'].astype(int)
            img = cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

        # 수정된 이미지를 저장합니다.
        output_path = "t1_output.jpg"
        cv2.imwrite(output_path, img)

        return {"message": "이미지 처리가 성공적으로 완료되었습니다.", "output_path": output_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        await file.close()
