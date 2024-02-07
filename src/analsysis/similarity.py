import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import os

# 이미지 파일 경로
file_path = 'E:/dev/fast/refore-inference/src/analsysis/test2.jpeg'

# OpenCV를 사용하여 이미지 읽기
img = cv2.imread(file_path)
if img is None:
    print(f"이미지를 불러오는 데 실패했습니다: {file_path}")
else:
    print(f"이미지를 성공적으로 불러왔습니다: {file_path}")

# FaceAnalysis 객체 생성 및 설정
app = FaceAnalysis(providers=['CPUExecutionProvider'])  # CUDAExecutionProvider가 사용 불가능한 경우
app.prepare(ctx_id=0, det_size=(640, 640))

# 얼굴 인식 및 처리
faces = app.get(img)
rimg = cv2.rectangle

# 결과 이미지 저장
cv2.imwrite("./t1_output.jpg", rimg)
