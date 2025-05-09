from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

input_wav = str(os.environ['HOME'])+ "/BohPJ/opencamp/test_audio/test4.mp3"

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://piano-scribe.glitch.me/")

WebDriverWait(driver, 360).until(EC.visibility_of_element_located((By.ID, "btnUpload")))
driver.find_element(By.ID, "fileInput").send_keys(input_wav)

WebDriverWait(driver, 360).until(EC.visibility_of_element_located((By.ID, "saveBtn")))
driver.find_element(By.ID, "saveBtn").click()
time.sleep(10)

if "transcription.mid" in os.listdir(str(os.environ['HOME'])+"/Downloads"):
    driver.quit()

else:
    driver.quit()
    print('Error: No such file "transcription.mid"')