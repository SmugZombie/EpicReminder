# Script: EpicReminder.py
# Developer: Ron Egli
# Version: 1.0.4
# Purpose: Pulls Epic's site on a regular interval, checks for changes, if changes to free games are detected it sends a remminder via Discord

import requests
import json
import hashlib
import sys
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv('.env')
hash = ""

#Build Chrome Options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

DISCORDWEBHOOK = str(os.getenv('DISCORDWEBHOOK'))
if DISCORDWEBHOOK == "":
    print("Invalid Webhook Provided")
    sys.exit()

try:
    SLEEPTIME = int(os.getenv('SLEEPTIME'))
except:
    SLEEPTIME = 7200

def getCurrentHash():
    global hash
    url = "https://playground.alreadydev.com/epic/"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data = payload)

    hash = response.text

def setCurrentHash(newHash):
    global hash
    url = "https://playground.alreadydev.com/epic/?hash=" + newHash

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data = payload)

    hash = response.text

def compareHash(newhash):
    getCurrentHash()

    oldhash = hash

    # Debug
    print("New: " + newhash)
    print("Old: " + oldhash)

    if oldhash == "pause":
        return False
    if oldhash == newhash:
        return False
    else:
        setCurrentHash(newhash)
        return True

def saveHash(newhash):
    with open(".lastHash", 'w') as hashfile:
        hashfile.write(newhash)

def pullLatest():
    now = str(datetime.datetime.now())
    # Build the browser
    #driver = webdriver.Chrome('./chromedriver', options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # Fetch the page
    driver.get("https://www.epicgames.com/store/en-US/")
    # Find the free games div
    gamesdiv = driver.find_element_by_class_name(str(os.getenv('MONITOR')))
    # gamesdiv = driver.find_element_by_xpath("//div[@component='DiscoverContainerHighlighted']"); 
    # Debug
    print(now)
    print("-----------Debug----------------")
    print(gamesdiv.text)
    print("-----------Debug----------------")
    if len(gamesdiv.text) <= 40:
        print("String not long enough, Breaking")
        driver.close()
        return
    # Replace the results / format for prettiness
    gamesdiv = gamesdiv.text.replace("VIEW MORE","").replace("FREE NOW","").replace("COMING SOON","\nCOMING SOON").replace("\nFree"," - Free").replace("\n\n", "\n").replace("\n\n", "\n").replace("Free Games","--- FREE EPIC GAMES ---")
    # Hash it, to double check
    newhash = hashlib.md5(gamesdiv.encode("utf-8")).hexdigest()
    # Add a link
    gamesdiv = gamesdiv + "\nhttps://www.epicgames.com/store/en-US/"
    # Debug
    print("-----------Debug--Cleaned------")
    print(gamesdiv)
    print("-----------Debug----------------")
    # Close the browser
    driver.close()
    # If the hash doesn't match, proceed
    if compareHash(newhash) is True:
        # Send the latest to Discord
        sendToDiscord(gamesdiv)
        # Save the hash so we don't send it again
        # saveHash(newhash)
    else:
        print(now + " Skipping")

def sendToDiscord(gamesdiv):
    data = {}
    data['content'] = gamesdiv

    url = DISCORDWEBHOOK

    payload = json.dumps(data)
    headers = { 'Content-Type': 'application/json' }
    response = requests.request("POST", url, headers=headers, data = payload)
    # Debug
    print(response.text.encode('utf8'))

def main():
    print("main")
    pullLatest()
    print("Sleeping for: " + str(SLEEPTIME) + " Seconds")
    time.sleep(SLEEPTIME)
    #sys.exit(1)
    main()

print("Running Script")
main()
