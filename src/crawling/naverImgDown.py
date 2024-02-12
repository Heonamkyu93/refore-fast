from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from urllib.request import urlretrieve

# 폴더를 생성하는 함수
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f'{directory} 폴더 생성 완료')
    except OSError:
        print(f'Error: Creating directory. {directory}')

# 사용자로부터 이미지를 검색할 동물 이름 입력 받기
input_name = input('이미지를 수집할 사진 입력 >> ')
driver = webdriver.Chrome()

# 네이버 이미지 탭에 접근
driver.get(f'https://search.naver.com/search.naver?where=image&sm=tab_jum&query={input_name}')
time.sleep(2)  # 페이지가 완전히 로드되도록 잠시 대기

# 스크롤 다운하여 이미지 로드
for i in range(6):  # 스크롤을 6번 내림
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
    time.sleep(2)

print('스크롤 다운 완료')

images = driver.find_elements(By.CSS_SELECTOR, 'img')

# 수정된 이미지 URL 추출 로직
srcs = []
for image in images:
    src = image.get_attribute('src') or image.get_attribute('data-src')
    if src and 'http' in src:
        srcs.append(src)
# 검색 이름 폴더 만들기
folder_name = f'./{input_name}'
createFolder(folder_name)




# 이미지 파일 저장
for idx, src in enumerate(srcs):
    if idx >= 30:  
        break
    try:
        # src가 None이 아니고, 'http'로 시작하는 경우에만 저장
        if src and src.startswith('http'):
            file_name = f'{folder_name}/{input_name}_{idx+1}.jpg'
            urlretrieve(src, file_name)
            print(f'{file_name} 저장 완료')
    except Exception as e:
        print(f'Error saving image: {src}, error: {e}')

driver.close()  # 브라우저 닫기
print(f'{input_name} 이미지 수집, 저장 작업 완료')
