from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

input_wav = str(os.environ['HOME'])+ "/BohPJ/opencamp/test_audio/test.mp3"

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

import pretty_midi
import numpy as np
import scipy.io.wavfile as wavfile

midi_data = pretty_midi.PrettyMIDI('/Users/tachibananoyushou/Downloads/transcription.mid')

fs = 44100
duration = midi_data.get_end_time()  

samples = np.zeros(int(fs * duration))

for instrument in midi_data.instruments:
    for note in instrument.notes:
        start_sample = int(note.start * fs)
        end_sample = int(note.end * fs)
        frequency = pretty_midi.note_number_to_hz(note.pitch)
        phase = 2.0 * np.pi * frequency / fs
        t = np.arange(start_sample, end_sample)
        samples[t] += np.sin(phase * t)

samples /= np.max(np.abs(samples))

wavfile.write('output.wav', fs, samples)

