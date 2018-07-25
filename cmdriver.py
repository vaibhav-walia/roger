from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os
import time
import datetime

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# unzip and put in the same directory as this file
chrome_driver = os.getcwd()+'/chromedriver';
# go to transit website
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.get("https://truetime.portauthority.org/bustime/eta/eta.jsp")
findStop_button = driver.find_element_by_css_selector("[id=findStop]")
findStop_button.click()

# capture the screen, name the file using current time
filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
driver.get_screenshot_as_file(filename+'.png')