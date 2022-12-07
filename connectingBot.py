import os
import time

from dotenv import load_dotenv
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from list_urls import list_of_urls_anderson

load_dotenv()



linkedin_login = os.getenv('LINKEDIN_LOGIN')
linkedin_pass = os.getenv('LINKEDIN_PASSWORD')




driver_service = Service(executable_path='/home/hello/Downloads/chromedriver.exe')
driver = webdriver.Chrome(service=driver_service)

driver.get('https://www.linkedin.com')
time.sleep(3)

# ********** LOG IN *************

username = driver.find_element("xpath", "//input[@name='session_key']")
password = driver.find_element("xpath", "//input[@name='session_password']")

username.send_keys(linkedin_login)
password.send_keys(linkedin_pass)
time.sleep(2)

driver.find_element("xpath", "//button[@type='submit']").click()

"""
add contacts
"""
for url in list_of_urls_anderson:
    driver.get(url)
    time.sleep(3)
    all_buttons = driver.find_elements(By.TAG_NAME, 'button')
    connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

    for btn in all_buttons:
        if btn.text == "Connect":
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
            name = driver.find_element(By.XPATH, "//strong")
            full_name = name.text
            send = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
            driver.execute_script("arguments[0].click();", send)
            time.sleep(2)
            logger.info(f'We successfully added a new invite to connect with {full_name}')
            close = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            driver.execute_script("arguments[0].click();", close)
            time.sleep(2)
        else:
            continue
