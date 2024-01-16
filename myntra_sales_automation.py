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
DB_HOST = 'your_database_connection'
DB_USER = 'db_username'
DB_PASSWORD = 'pass@word'
DB_PORT = 0000
DB_DATABASE = 'db_name'

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
driver.get("https://partners.myntrainfo.com/")
driver.maximize_window()
time.sleep(random.choice([4, 5, 6, 7]))

# ---------------- login page --------------------------
login_click = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/div/div/div[3]/div/button").click()
print('login pe 1st click hua')
email_click = driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[2]/button[1]/div[2]").click()
print('Now enter email....')


#----------------login setup-----------------------------------
def login_step(email_id, pass_word):
    #--------- Login email password ----------
    driver.find_element(By.ID, "email").send_keys(email_id)
    time.sleep(random.choice([3,4,5,6]))
    driver.find_element(By.ID, "password").send_keys(pass_word)
    time.sleep(random.choice([3,4,5]))
    driver.find_element(By.XPATH, "//*[@id='__next']/div/div[2]/div[3]/div[6]").click()
    time.sleep(random.choice([3,4,5]))

#--------------login credentials---------------------
login_step("prakhar.dhamija@idamwellness.com", "Idam@123")
print('Login Success :) ')
time.sleep(100)
