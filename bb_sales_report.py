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
from selenium.webdriver.support.ui import Select


#-------setting up download path and chrome-----------------

download_path = r"C:\Trailytics\crawlers\Automation"
chrome_options = Options()
prefs = {"download.default_directory": download_path}
chrome_options.add_experimental_option("prefs",prefs)


#----------------connect to database--------------
DB_HOST = 'your_host_address'
DB_USER = 'user_name'
DB_PASSWORD = 'pass_word'
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


# your chrome drive path  --> make sure you use same version of your browser
driver = webdriver.Chrome(service=Service(r"C:\Trailytics\crawlers\chromedriver.exe"), options=chrome_options)
driver.implicitly_wait(random.choice([4, 5, 6, 7]))
driver.get("https://partner.bigbasket.com/partner/login/")
driver.maximize_window()
time.sleep(random.choice([4, 5, 6, 7]))


#----------------login setup-----------------------------------
def login_step(email_id, pass_word):
    #--------- Login email password ----------
    driver.find_element(By.ID, "id_username").send_keys(email_id)
    time.sleep(random.choice([3,4,5,6]))
    
    driver.find_element(By.ID, "id_password").send_keys(pass_word)
    time.sleep(random.choice([3,4,5]))
    
    dropdown = driver.find_element(By.ID, "id_entityname")
    select = Select(dropdown)
    select.select_by_value('2')
    
    driver.find_element(By.XPATH, "//*[@id='uiv2-loginform']/button").click()
    time.sleep(random.choice([3,4,5]))

#--------------login credentials---------------------
login_step("your@email.in", "your_password")
print('Login Success :) ')


# Redirecting to Download page to avoid error
driver.get("https://partner.bigbasket.com/partner/marketeer/tpv_product_reports/")
time.sleep(2)


# clicking download button
driver.find_element(By.XPATH, "//*[@id='QoH']/div/table/tbody/tr[2]/td[3]/button").click()
print("Download Requested")
time.sleep(3)


driver.refresh()
print('Popup gone')
time.sleep(3)
print("Moving to another section")
driver.find_element(By.XPATH, "//*[@id='stitch_report']").click()


print("Selecting from Dropdown option")
# drop down selection
option_to_select = "analytics_manufacturer_bbdaily-sales-report"

try:
    # Find the dropdown element by ID
    dropdown = Select(driver.find_element(By.ID, "selectreport"))

    # Select the desired option by its value
    dropdown.select_by_value(option_to_select)

    # Wait for the changes to take effect (adjust timeout as needed)
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "//span[@id='output']"), f'You selected: {option_to_select}'))
except:
    print("Not done")

print('Option choosed')


# Calculate the date 7 days before the current date
print('selecting start date')
seven_days_ago = datetime.now() - timedelta(days=7)
formatted_date = seven_days_ago.strftime('%Y-%m-%d')


try:
    # Find the date input element by ID
    date_input = driver.find_element(By.ID, 'selected_date_start_date')

    # Execute JavaScript to set the date directly (some websites require this)
    driver.execute_script("arguments[0].value = arguments[1]", date_input, formatted_date)

except:
    print('Not done')

print("Starting date choosen")
print('Now selecting end date')


# Get the current date in the required format (YYYY-MM-DD)
current_date = datetime.now().strftime('%Y-%m-%d')

try:
    # Find the date input element by ID
    date_input = driver.find_element(By.ID, 'selected_date_end_date')

    # Execute JavaScript to set the date directly (some websites require this)
    driver.execute_script("arguments[0].value = arguments[1]", date_input, current_date)

except:
    print('not done')

print("End date choosen")
# pushing columns to download
driver.find_element(By.XPATH, "//*[@id='2052_select_rightAll']/i").click()
print("Pushed columns")

# clicking download report
driver.find_element(By.XPATH, "//*[@id='download']").click()
print('Download requested')
driver.refresh()
print("Popup gone")


# goto download report
driver.find_element(By.XPATH, "//*[@id='download_tab']").click()
print("Now inside Download Report Section")


driver.find_element(By.XPATH, "/html/body/div[2]/div[1]").click()
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/button").click()
print("Landed on Download Page")


# waiting for the report to get generated
# time.sleep(30) 
n=0
while(1):
    
    try:
        print("Download Attempt:",n+1)
        time.sleep(30)
        element = driver.find_element(By.XPATH, "//*[@id='QoH']/div/table/tbody/tr[3]/td[4]")
        status = element.text
        
        print("Status:", status)
        
        if status != "Pending":
            driver.find_element(By.XPATH,"//a[contains(text(), 'Download')]").click()
            time.sleep(random.choice([7,8,10]))
            break
        time.sleep(120)
        n+=1

        if n > 10:
            break

    except Exception as e:
        print("Waiting exception:",e)

print('Done')
