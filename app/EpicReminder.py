# Script: EpicReminder.py
# Developer: Ron Egli
# Version: 1.0.1
# Purpose: Pulls Epic's site on a regular interval, checks for changes, if changes to free games are detected it sends a remminder via Discord

import requests
import json
import hashlib
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv('.env')

#Build Chrome Options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

DISCORDWEBHOOK = str(os.getenv('DISCORDWEBHOOK'))
if DISCORDWEBHOOK == "":
    print("Invalid Webhook Provided")
    sys.exit()

SLEEPTIME = 30

def compareHash(newhash):
    try:
        with open(".lastHash", 'r') as hashfile:
            oldhash = hashfile.readline()
    except FileNotFoundError as e:
        with open(".lastHash", 'w') as hashfile:
            oldhash = ""
            hashfile.write("")

    # Debug
    print("New: " + newhash)
    print("Old: " + oldhash)

    if oldhash == newhash:
        return False
    else:
        return True

def saveHash(newhash):
    with open(".lastHash", 'w') as hashfile:
        hashfile.write(newhash)

def pullLatest():
    # Build the browser
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    # Fetch the page
    driver.get("https://www.epicgames.com/store/en-US/")
    # Find the free games div
    gamesdiv = driver.find_element_by_class_name('css-decuci')
    # Debug
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
        saveHash(newhash)

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
    pullLatest()
    print("Sleeping for: " + str(SLEEPTIME) + " Seconds")
    time.sleep(SLEEPTIME)
    main()

main()