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
import re
import csv

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

def fetch_transaction(driver, tx_hash, outfile):
    driver.get('https://etherscan.io/tx/%s' % tx_hash)

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

    m = re.search('<textarea.*?id="inputdata">.*?Function: (.*?)(\(.*?\)).*?MethodID: (.*?)(\[.*?)</textarea>', html, re.DOTALL)
    if m is not None:
        functionName = m.group(1).rstrip()
        arguments =  m.group(2).rstrip()
        methodId = m.group(3).rstrip()
        parameters_raw = m.group(4) + '\n'
        parameters = re.findall('\[\d+\]: (.*?)\n', parameters_raw, re.DOTALL)
        outfile.write("%s,%s,%s,%s\n" % (tx_hash, functionName, methodId, ','.join(parameters)))
    else:
        outfile.write("%s\n" % (tx_hash)) # Record it has been processed

def fetch_transactions(driver, tx_hash_list, out_filename):
    with open(out_filename, "a") as outfile:
        process_count = 1
        for tx in tx_hash_list:
            fetch_transaction(driver, tx, outfile)
            print("Finished [%d] %s\n" % (process_count, tx))
            process_count += 1

# Main

tx_list = []
existing_tx_map = {}
data_folder = "raw_data/compound"

input_filename = '%s/Comptroller-0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b.csv' % data_folder
output_filename = '%s/compound_function_calls.csv' % data_folder

# get list of already fetched tx
with open(output_filename, 'r') as output_csv_file:
    csv_reader = csv.reader(output_csv_file, delimiter=',')
    for row in csv_reader:
        tx_hash = row[0]
        existing_tx_map[tx_hash] = True

# process new records
line_limit = 20000
with open(input_filename) as input_csv_file:
    csv_reader = csv.reader(input_csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > line_limit:
            break
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'fetching \t{row[0]}')
            tx = row[0]
            # fetch_transaction(driver, tx)
            if tx not in existing_tx_map:
                tx_list.append(tx)
            line_count += 1
    print(f'Processed {line_count} lines. New records found {len(tx_list)}')

# Go Fetch
if len(tx_list) > 0:
    chromedriver = "./chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    # fetch_transaction(driver, '0x452d3bc7caddd5ce1e26e48152edb5ee0bf0fe31b8f94662bcf31bfdc2fee378')
    fetch_transactions(driver, tx_list, '%s/compound_function_calls.csv' % data_folder)

    driver.quit()

