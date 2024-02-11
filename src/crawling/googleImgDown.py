from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request

driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
elem = driver.find_element(By.NAME, "q")
elem.send_keys("고화질 고양이상 여자 연예인 정면 ")  # 검색어 수정
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

max_images = 10000  # 최대 다운로드할 이미지 수

count = 1

for image in images[:max_images]:
    try:
        # 원본 이미지 URL을 직접 추출합니다.
        imgUrl = image.get_attribute("src") or image.get_attribute("data-src")
        if imgUrl:
            filename = f"{count}.jpg"
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imgUrl, filename)
            print(f"Image {count} saved.")
            count += 1
        else:
            print(f"Image {count} URL not found.")
    except Exception as e:
        print(f"Error downloading image {count}: {e}")

driver.close()
