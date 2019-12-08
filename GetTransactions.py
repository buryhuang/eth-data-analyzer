from __future__ import print_function # Python 2/3 compatibility
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import boto3
import json
import decimal
import uuid
import re
import urllib.parse
import msvcrt as m
import re

def wait():
    m.getch()

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def find_by_xpath(locator, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, locator))
    )
    return element

def scroll_down_to_bottom():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Main
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('https://etherscan.io/tx/0x452d3bc7caddd5ce1e26e48152edb5ee0bf0fe31b8f94662bcf31bfdc2fee378')

html = driver.page_source

# <textarea readonly="" spellcheck="false" class="form-control bg-light text-secondary text-monospace p-3" rows="8" id="inputdata">Function: enterMarkets(address[] cTokens) ***

# MethodID: 0xc2998238
# [0]:  0000000000000000000000000000000000000000000000000000000000000020
# [1]:  0000000000000000000000000000000000000000000000000000000000000008
# [2]:  0000000000000000000000006c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e
# [3]:  0000000000000000000000005d3a536e4d6dbd6114cc1ead35777bab948e3643
# [4]:  0000000000000000000000004ddc2d193948926d02f9b1fe9e1daa0718270ed5
# [5]:  000000000000000000000000158079ee67fce2f58472a96584a73c7ab9ac95c1
# [6]:  000000000000000000000000f5dce57282a584d2746faf1593d3121fcac444dc
# [7]:  00000000000000000000000039aa39c021dfbae8fac545936693ac917d5e7563
# [8]:  000000000000000000000000c11b1268c1a384e55c48c2391d8d480264a3a7f4
# [9]:  000000000000000000000000b3319f5d18bc0d84dd1b4825dcde5d5f7266d407</textarea>

m = re.search('<textarea.*?id="inputdata">(.*?)</textarea>', html, re.DOTALL)
if m is not None:
    print(m.group(0))

# print('Waiting for user login. When done, press any key to continue...')
# wait()

# scroll_down_to_bottom()

driver.quit()

