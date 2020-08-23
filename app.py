from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys
from PIL import Image
from io import BytesIO
from datetime import datetime

url = 'http://apps.benilde.edu.ph/sis/'
fox_driver_path = "./geckodriver.exe"

fox_options = Options()
fox_options.add_argument('--headless')
webdriver = webdriver.Firefox(
    executable_path=fox_driver_path, options=fox_options
)


def get_grades(u, p):
    webdriver.get(url)
    print('page loaded')
    id_number = webdriver.find_element_by_xpath(
        "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/form/table/tbody/tr[3]/td/input")
    id_number.send_keys(u)
    password = webdriver.find_element_by_xpath(
        "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/form/table/tbody/tr[4]/td/input")
    password.send_keys(p)
    enter = webdriver.find_element_by_xpath(
        '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/form/table/tbody/tr[5]/td/input[1]').send_keys(Keys.RETURN)
    time.sleep(1)
    print('logged in')
    webdriver.find_element_by_xpath(
        '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[3]/td/a').send_keys(Keys.RETURN)
    time.sleep(1)
    print('extracting grades')
    webdriver.get('http://sis.benilde.edu.ph/sisv2/CurrentEnrollmentRecord')
    time.sleep(1)

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    grades = webdriver.find_element_by_xpath(
        '//*[@id="content"]')

    location = grades.location
    size = grades.size
    file_name = '%s_grades.png' % (dt_string)
    file_path = './grades/%s' % (file_name)
    webdriver.save_screenshot(file_path)
    x = location['x']
    y = location['y']
    width = location['x']+size['width']
    height = location['y']+size['height']
    im = Image.open(file_path)
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(file_path)
    print('grades saved as %s' % file_path)
    # webdriver.close()


while True:
    get_grades('ID_NUMBER', 'PASSWORD')
    time.sleep(10)
