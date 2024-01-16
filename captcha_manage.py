import requests
import speech_recognition as sr
from pydub import AudioSegment
import sys
import time
import glob
import os
from turtle import down
import pyotp
import re
import random
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("The statement took too long to execute.")

def run_with_timeout(statement, timeout):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)  # Set the alarm to trigger after the specified timeout

    try:
        result = statement()  # Execute the statement
        signal.alarm(0)  # Cancel the alarm if the statement finishes before the timeout
        return result
    except TimeoutError as e:
        print(e)
        return None
# download the audio file
def process_captcha(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[5]/div[4]/iframe'))
    driver.find_element_by_xpath('//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[2]').click()
    n=0
    checkbox="false"
    time.sleep(3)
    while checkbox=="false" and n<5:
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[5]/div[4]/iframe'))
            url = driver.find_element(By.ID, "audio-source").get_attribute("src")
            # url = "https://www.google.com/recaptcha/api2/payload?p=06AKH6MRHCkpRc1XLhMLGDWxlYXVxmA4emIs_10wDwwv3iUmUSPFv5PDtjNypxPkI2vKRrjn5laDPBQXMiHf1lbb7Xp0jNJ24vEE2Zq63b3aHZOqT1JAeiN4Zugv70KBSLyt3SitRvcS_OlNT_75BAqwaGiy3J62dEEZXKUmAtC-K6zZjFh18zVJ4hq_BLu8IxjC99PFUJWdeOeokwtaMiZbBHnIs3DjkaBLF77qC3R6JJMX_Psol-VcU&k=6LdEyyQUAAAAACuau_3HiFNBBU6SEHapaY1Ksspc"
            r = requests.get(url)
            # r=run_with_timeout(requests.get(url), 8)
            if r==None:
                continue
            with open("audio\Audio.mp3", "wb") as f:
                f.write(r.content)
        except:
            n+=1
            continue


        # transcribe the audio file
        try:
            # convert the MP3 file to a WAV file
            sound = AudioSegment.from_mp3("audio\Audio.mp3")
            sound.export("audio\Audio.wav", format="wav")

            r = sr.Recognizer()
            with sr.AudioFile("audio\Audio.wav") as source:
                audio = r.record(source)
            test=""
            text = r.recognize_google(audio)
        except:
            n+=1
            continue
        print(text)
        driver.find_element_by_id("audio-response").send_keys(text)
        time.sleep(random.choice([3])) 
        driver.find_element_by_id('recaptcha-verify-button').click()
        time.sleep(random.choice([3])) 
        driver.switch_to.default_content()
        time.sleep(3)
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="reCaptcha"]/div/div/iframe'))
        checkbox = driver.find_element_by_id("recaptcha-anchor").get_attribute("aria-checked")
        n+=1

    
