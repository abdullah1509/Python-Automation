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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from amazoncaptcha import AmazonCaptcha
from pyshadow.main import Shadow

idam_vc = "7----------------------------------------------" #--- change the  security key
# totp = pyotp.TOTP(idam_vc)
# curr_otp = str(totp.now())
# print('otp is : ', curr_otp)
# exit(0)

start_date = datetime(2024, 1, 4)
end_date = datetime(2024, 1, 4)
current_date = start_date

DB_HOST = "your_database_connection"
DB_USER = ""
DB_PASSWORD = ""
DB_DATABASE = ""
DB_PORT = 0000

download_path = r"C:\download_data"
chromeOptions = webdriver.ChromeOptions()
print("hey")

prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "browser.helperApps.alwaysAsk.force": False,
    "browser.download.manager.useWindow": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
}
chromeOptions.add_experimental_option("prefs",prefs)
service = Service(r"C:\chromedriverextension\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chromeOptions)
print('hoo')
driver.maximize_window()
driver.get("https://www.vendorcentral.in/")
driver.implicitly_wait(random.choice([6,7,8,9]))

def handle_captcha():
    captcha_text = "we just need to make sure you're not a robot"
    n=5
    for i in range(0,n):
        if captcha_text in driver.page_source:
            print("Handling Captcha...")
            img_element = driver.find_element(By.CSS_SELECTOR, '.a-row.a-text-center img')
            img_url = img_element.get_attribute('src')
            print(img_url)
            captcha = AmazonCaptcha.fromlink(img_url)
            solution = captcha.solve()
            print('solution : ', solution)
            driver.find_element(By.ID, "captchacharacters").send_keys(str(solution))
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, ".a-button-inner").click()
            time.sleep(3)
        else:
            print("No Captcha :) ")
            break    

def login_step(email_id, pass_word):
    #--------- Login email password ----------
    handle_captcha()
    time.sleep(3)
    driver.find_element(By.ID, "ap_email").send_keys(email_id)
    # 
    time.sleep(random.choice([3,4,5,6]))
    driver.find_element(By.ID, "ap_password").send_keys(pass_word)
    # Change password
    time.sleep(random.choice([3,4,5]))

    driver.find_element(By.ID, "signInSubmit").click()
    time.sleep(random.choice([3,4,5]))

    # ----------------- Enter OTP-------------------

    ots07_pidilite = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    totp = pyotp.TOTP(ots07_pidilite)
    curr_otp = str(totp.now())
    print('OTP is : ', curr_otp)
    driver.find_element(By.ID, "auth-mfa-otpcode").send_keys(curr_otp)
    time.sleep(random.choice([3,4,5]))
    driver.find_element(By.ID, "auth-signin-button").click()
    print('Login Successful to Vendor Central')


# ----------------- select the account ---------------
login_step("your@email.com", "pass@word")
handle_captcha()
time.sleep(3)

#-----------------login again if the vc not opened-------
print('fir se vendor Central')

try:
    driver.find_element(By.XPATH, '//*[@id="sc-content-container"]/div/div[1]/div[2]/div/button[2]/span').click()
    driver.find_element(By.XPATH, '//*[@id="sc-content-container"]/div/div[1]/div[3]/button').click()


except:
    driver.find_element(By.XPATH, '//*[@id="sc-content-container"]/div/div[1]/div[2]/div/button[2]/span')


try:
    driver.find_element(By.ID, 'vc-navigation-tab-reports').click()
    driver.find_element(By.ID, 'vc-navigation-item-retail-analytics').click()
    time.sleep(random.choice([3,4,5]))
except:
    driver.get("https://www.vendorcentral.in/")
    time.sleep(random.choice([4, 5, 6, 7]))
    login_step("your@email.com", "pass@word")
    handle_captcha()
    time.sleep(3)
    driver.find_element(By.ID, 'vc-navigation-tab-reports').click()
    driver.find_element(By.ID, 'vc-navigation-item-retail-analytics').click()
    time.sleep(random.choice([3,4,5]))

sales_element = driver.find_element(By.XPATH, '//a[@href="/retail-analytics/dashboard/sales"]')
inv_element = driver.find_element(By.XPATH,   '//a[@href="/retail-analytics/dashboard/inventory"]')
shadow = Shadow(driver)
time.sleep(3)
inv_element.click()
# ------------------------------- loop through the date range-------------------------------
while current_date <= end_date:
    print('current date : ', current_date.strftime('%Y-%m-%d'))
    current_day = int(current_date.strftime('%d'))
    current_month = int(current_date.strftime('%m'))
    current_year = int(current_date.strftime('%Y'))
    current_date_dash = f"{current_day}-{current_month}-{current_year}"
    
    current_date_slash = str(current_date.strftime('%d/%m/%Y'))
    
    print(current_date_dash)
    print(current_date_slash)
    

    # ------------- customize columns : add more columns-------------
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "css-4g6ai3").click()
    time.sleep(1)
    shadow.find_element('div[aria-label="Brand Code"]').click()
    time.sleep(1)
    shadow.find_element('div[aria-label="Category"]').click()
    time.sleep(1)
    shadow.find_element('div[aria-label="Subcategory"]').click()
    time.sleep(1)
    sv_button = driver.find_element(By.CSS_SELECTOR, 'kat-button[label="Save"]')
    # print(sv_button)
    sv_button.click()
    time.sleep(2)

    #------------ select the start-date in calendar -------------
    time.sleep(3)
    shadow_host = driver.find_element(By.ID, "custom-period_start_date")
    script = 'return arguments[0].shadowRoot.children'
    shadow_root = driver.execute_script(script, shadow_host)
    # print(shadow_root)
    date_picker = shadow_root[0].find_element(By.CSS_SELECTOR, "kat-input[part='date-picker-input']")
    # print(date_picker)
    date_picker.click()
    time.sleep(2)
    print('click hua : date start')

    time.sleep(2)
    date_picker.send_keys(Keys.CONTROL, 'a')
    date_picker.send_keys(Keys.DELETE)
    date_picker.send_keys(str(current_date_slash))

    # ---------------- selecting the end-date in calendar ---------------
    time.sleep(3)
    shadow_host = driver.find_element(By.ID, "custom-period_end_date")
    script = 'return arguments[0].shadowRoot.children'
    shadow_root = driver.execute_script(script, shadow_host)
    # print(shadow_root)
    date_picker_ = shadow_root[0].find_element(By.CSS_SELECTOR, "kat-input[part='date-picker-input']")
    # print(date_picker_)
    date_picker_.click()
    time.sleep(2)
    print('click hua : date end')

    time.sleep(2)
    date_picker_.send_keys(Keys.CONTROL, 'a')
    date_picker_.send_keys(Keys.DELETE)
    date_picker_.send_keys(str(current_date_slash))

    # ------------ Sourcing ----------------
    #shadow_host = driver.find_element(By.XPATH, '//*[@id="distributorView"]')
    script = 'return arguments[0].shadowRoot.children'
    shadow_root = driver.execute_script(script, shadow_host)
    date_picker_ = shadow_root[0].find_element(By.XPATH, '//*[@id="distributorView"]').click()
    #shadow_root.send_keys(KEYS.DOWN).click()

    # ----------- now click on apply buttion ------------
    apply_button = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[6]/kat-button")
    apply_button.click()
    # ----------------- select csv file -----------
    time.sleep(3)
    csv_file = shadow.find_element("button[value='csv']")
    csv_file.click()

    # --------view and manage section to download

    view_and_manage = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/a')
    view_and_manage.click()

    # --------- wait for sometime to download ------
    time.sleep(9)
    file_name =  f"Inventory_Manufacturing_Retail_India_Custom_{current_date_dash}_{current_date_dash}.csv"
    print('searching for file : ', file_name)
    num_attempts = 9
    download_status = False
    for _ in range(num_attempts):
        try:
            download_button = driver.find_element(By.CSS_SELECTOR, f'kat-table-cell[role="cell"] a[href*="{file_name}"]')
            download_button.click()
            print('\n---------------Download successful for ', current_date)
            download_status = True
            break
        except Exception as e:
            print('again, wait for 5 seconds to download')
            time.sleep(random.choice([7,8,9]))
    
    if download_status==False:
        print(f'-ERROR--x-X-x-X-x-X-x-X-x-X-x-X-x-X-x-X-x-X-x-X-x-X-- download not completed for {current_date}')
        exit(0)

    driver.refresh()
    time.sleep(3)    
    current_date += timedelta(days=1)

driver.close()
driver.quit()
print('\n\n-------- All files dowonloaded till ', current_date)
