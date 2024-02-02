from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from selenium.common.exceptions import WebDriverException, NoSuchDriverException

import time
import requests
import os
import re
import base64
from flask import Flask

extensionId = 'ilehaonighjijnmpnagapkhpcdbhclfg'
CRX_URL = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=98.0.4758.102&acceptformat=crx2,crx3&x=id%3D~~~~%26uc&nacl_arch=x86-64"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

try:
    USER = os.environ['GRASS_USER']
    PASSW = os.environ['GRASS_PASS']
except:
    USER = ''
    PASSW = ''

# are they set?
if USER == '' or PASSW == '':
    print('Please set GRASS_USER and GRASS_PASS env variables')
    exit()

#https://gist.github.com/ckuethe/fb6d972ecfc590c2f9b8
def download_extension(extension_id):
    url = CRX_URL.replace("~~~~", extension_id)
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, stream=True, headers=headers)
    with open("grass.crx", "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


print('Downloading extension...')
download_extension(extensionId)
print('Downloaded! Installing extension and driver manager...')

options = webdriver.ChromeOptions()
#options.binary_location = '/usr/bin/chromium-browser'
options.add_argument("--headless=new")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--no-sandbox')

options.add_extension('grass.crx')

print('Installed! Starting...')
try:
    driver = webdriver.Chrome(options=options)
except (WebDriverException, NoSuchDriverException) as e:
    print('Could not start with Manager! Trying to default to manual path...')
    try:
        driver_path = "/usr/bin/chromedriver"
        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except (WebDriverException, NoSuchDriverException) as e:
        print('Could not start with manual path! Exiting...')
        exit()

#driver.get('chrome-extension://'+extensionId+'/index.html')
print('Started! Logging in...')

driver.get('https://app.getgrass.io/')

sleep = 0
while True:
    try:
        driver.find_element('xpath', '//*[@name="user"]')
        driver.find_element('xpath', '//*[@name="password"]')
        driver.find_element('xpath', '//*[@type="submit"]')
        break
    except:
        time.sleep(1)
        print('Loading login form...')
        sleep += 1
        if sleep > 30:
            print('Could not load login form! Exiting...')
            driver.quit()
            exit()

#find name="user"
user = driver.find_element('xpath', '//*[@name="user"]')
passw = driver.find_element('xpath', '//*[@name="password"]')
submit = driver.find_element('xpath', '//*[@type="submit"]')

#get user from env
user.send_keys(USER)
passw.send_keys(PASSW)
submit.click()

sleep = 0
while True:
    try:
        e = driver.find_element('xpath', '//*[contains(text(), "Dashboard")]')
        break
    except:
        time.sleep(1)
        print('Logging in...')
        sleep += 1
        if sleep > 30:
            print('Could not login! Double Check your username and password! Exiting...')
            driver.quit()
            exit()

print('Logged in! Waiting for connection...')
driver.get('chrome-extension://'+extensionId+'/index.html')
sleep = 0
while True:
    try:
        driver.find_element('xpath', '//*[contains(text(), "Network quality")]')
        break
    except:
        time.sleep(1)
        print('Loading connection...')
        sleep += 1
        if sleep > 30:
            print('Could not load connection! Exiting...')
            driver.quit()
            exit()

print('Connected! Starting API...')
#flask api
app = Flask(__name__)
@app.route('/')
def get():
    network_quality = driver.find_element('xpath', '//*[contains(text(), "Network quality")]').text
    network_quality = re.findall(r'\d+', network_quality)[0]
    lifetime_earnings = driver.find_element('xpath', '//*[contains(text(), "Lifetime earnings")]')
    lifetime_earnings = lifetime_earnings.find_element('xpath','following-sibling::div')
    lifetime_earnings = lifetime_earnings.find_element('xpath','child::p').text
    return {'network_quality': network_quality, 'lifetime_earnings': lifetime_earnings}

app.run(host='0.0.0.0',port=80, debug=False)
driver.quit()
