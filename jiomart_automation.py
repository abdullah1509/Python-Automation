#------------Import important libraries----------------

import sys
import time
import glob
import os
import pyotp
import re
import random
import pandas as pd
import pymysql
import configparser
from datetime import date, datetime, timedelta
from tabulate import tabulate
from IPython.display import display
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from amazoncaptcha import AmazonCaptcha
from pyshadow.main import Shadow

#-------setting up download path and chrome-----------------

download_path = r"C:\Trailytics\crawlers\Automation"
chrome_options = Options()
prefs = {"download.default_directory": download_path}
chrome_options.add_experimental_option("prefs",prefs)

#----------------connect to database--------------
DB_HOST = 'database-1.cs7wneoxj0b8.us-east-1.rds.amazonaws.com'
DB_USER = 'abdullah'
DB_PASSWORD = 'Trailytics@789'
DB_PORT = 3306
DB_DATABASE = 'idam'

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_DATABASE,
                             port=DB_PORT,
                             connect_timeout=1000,
                             autocommit=True)

cursor = connection.cursor()

driver = webdriver.Chrome(service=Service(r"C:\Trailytics\crawlers\chromedriver.exe"), options=chrome_options)
driver.implicitly_wait(random.choice([4, 5, 6, 7]))
driver.get("https://identity.seller.jiomart.com/sso/login")
driver.maximize_window()
time.sleep(random.choice([4, 5, 6, 7]))


#----------------login setup-----------------------------------
def login_step(email_id, pass_word):
    #--------- Login email password ----------
    driver.find_element(By.ID, "user_user_id").send_keys(email_id)
    time.sleep(random.choice([3,4,5,6]))
    driver.find_element(By.ID, "user_password").send_keys(pass_word)
    time.sleep(random.choice([3,4,5]))
    
    # click captcha checkbox
    driver.find_element(By.XPATH, "//*[@id='new_user']/div[4]").click()
    time.sleep(random.choice([3,4,5]))

    ###############################################################
    #                 MANUALLY SOLVE CAPTCHA
    ###############################################################
    print("Going to sleep for 30s. Solve the captcha manually")
    time.sleep(30)
    
    # submit button
    driver.find_element(By.XPATH, "//*[@id='new_user']/div[5]").click()


#--------------login credentials---------------------
login_step("idamwellness", "Idam@1234")
print('Login Success :) ')


# redirecting to shipment page
time.sleep(random.choice([3,4,5,6]))
driver.get("https://seller.jiomart.com/oms/reports/ShipmentReport?page=1&per_page=20")


try:
    date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "start_date")))
    date_element.click()
    
    desired_date = '10 Jan 2024'
    driver.switch_to.active_element.send_keys(desired_date, Keys.RETURN)
except:
    print("Error")

time.sleep(random.choice([3,4,5,6]))

try:
    date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "end_date")))
    date_element.click()
    
    desired_date = '14 Jan 24'
    driver.switch_to.active_element.send_keys(desired_date, Keys.RETURN)
except:
    print("Error")

time.sleep(random.choice([3,4,5,6]))

# writing the file name
file_name_input = driver.find_element(By.CLASS_NAME, "form-control")

time.sleep(random.choice([3,4,5,6]))

# Text to be entered in the input field
text_to_enter = "jiomart " + datetime.now().strftime("%Y-%m-%d")

# Fill the input field with the text
file_name_input.send_keys(text_to_enter)

time.sleep(random.choice([3,4,5,6]))


# submit button
driver.find_element(By.XPATH, "//*[@id='generate_report']/button").click()

#pending time for the report to get generated
#time.sleep(30) 
n=0
while(1):
    
    try:
        print("Download Attempt:",n+1)
        driver.refresh()
        time.sleep(30)
        element = driver.find_element(By.XPATH, "//*[@id='content']/div/div/reports-show/div/div/div[2]/iweb-list/table/tbody/tr[1]/td[5]")
        status = element.text
        
        print("Status:", status)
        
        if status != "Requested":
            driver.find_element(By.CLASS_NAME,"download-btn").click()
            time.sleep(random.choice([7,8,10]))
            break
        time.sleep(120)
        n+=1

        if n > 10:
            break

    except Exception as e:
        print("Waiting exception:",e)
    

print("Report Downloaded")