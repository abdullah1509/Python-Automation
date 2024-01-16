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
DB_USER = 'database_username'
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


cursor.execute("SELECT MAX(OrderDate) FROM tb_wh_dtd_tatacliq;")
max_date = cursor.fetchone()[0]
print('Latest order date present is : ', max_date)
s_date = max_date 
s_date = s_date.strftime('%d/%m/%Y')
e_date = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')
print('New date to fetch data is :', s_date, ' => ', e_date)

driver = webdriver.Chrome(service=Service(r"C:\Trailytics\crawlers\chromedriver.exe"), options=chrome_options)
driver.implicitly_wait(random.choice([4, 5, 6, 7]))
driver.get("https://sellerzone.tatacliq.com/faces/report/orderSalesReport.jsp")
driver.maximize_window()
time.sleep(random.choice([4, 5, 6, 7]))


#----------------login setup-----------------------------------
def login_step(email_id, pass_word):
    #--------- Login email password ----------
    driver.find_element(By.ID, "loginId").send_keys(email_id)
    time.sleep(random.choice([3,4,5,6]))
    driver.find_element(By.ID, "password").send_keys(pass_word)
    time.sleep(random.choice([3,4,5]))
    driver.find_element(By.ID, "loginbutton").click()
    time.sleep(random.choice([3,4,5]))

    
#--------------login credentials---------------------
login_step("your@email.com", "Pass@word")
time.sleep(3)

print('login done')
driver.find_element(By.XPATH, "/html/body/form/article/div[3]/div[2]/a").click()
time.sleep(random.choice([3,4,5]))

driver.find_element(By.XPATH, "//*[@id='reportAndDashboard']/div[2]/div/ul[3]/li[3]/a").click()
time.sleep(random.choice([3,4,5]))

driver.find_element(By.ID, "slaveName").send_keys("Bella Vita Organic Gurgaon WH(126441-INGURWH)")
time.sleep(random.choice([3,4,5]))

driver.find_element(By.ID, "startDate").send_keys(str(s_date))  # START DATE INPUT
time.sleep(random.choice([3,4,5]))

#----------THE DAY GAP BETWEEN START DATE AND END SHOULD BE LESS THAN OR EQUAL TO 15--------

driver.find_element(By.ID, "endDate").send_keys(str(e_date))  # END DATE INPUT
time.sleep(random.choice([3,4,5]))

driver.find_element(By.CLASS_NAME, "dvSlaveList").click()
time.sleep(random.choice([3,4,5]))

driver.find_element(By.ID, "orderSalesReport").click()
time.sleep(random.choice([3,4,5]))
print('Downloading Report')
#time.sleep(100)

try:
    time.sleep(9)
    driver.find_element(By.XPATH, '//*[@id="showDetails"]/div').click()
    print("Option 1 executed")
except:
    try:
        time.sleep(9)
        driver.find_element(By.CLASS_NAME, "DownloadReportouter").click()
        print("Option 2 executed")
    except:
        time.sleep(9)
        driver.find_element(By.XPATH, '//*[@id="showDetails"]/div/input[1]').click()
        print("Option 3 executed")

print('<--- report downloaded --->')
