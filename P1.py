# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

import sys_checks
from playwright.sync_api import sync_playwright
import requests

CHEMICAL = "propanol".capitalize()

# Function that obtains SDS PDF download link
def GRAB_SDS_URL(CHEMICAL):
    WEBSITE = "https://www.sigmaaldrich.com"
    SEARCH_BUTTON_ID = "header-search-submit-search-wrapper"
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        page.goto(WEBSITE)

        # Find chemical
        page.get_by_role("textbox", name="Type in Product").fill(CHEMICAL)
        page.get_by_test_id(SEARCH_BUTTON_ID).click()

        # Using page.locator('element[object-property='value']') to find precise match. 
        # Using .nth(0) to select the first button - Index = '0'
        page.locator('button[aria-describedby="sds"]').nth(0).click()

        # Grabbing link for English version
        href_tag = page.get_by_test_id("sds-link-EN").get_attribute('href')

        # Constructing final download link by concatenating the website URL and the href tag
        final_download_link = WEBSITE + href_tag
        page.close()

    return final_download_link

# Function to Download SDS to a specific directory
def URL_to_PDF(url):
    with open(f"./storage_directory/{CHEMICAL}.pdf", "wb") as f:
        f.write(requests.get(url, stream=True, headers='Mozilla 5.5 Firefox'))
        f.close()

url = GRAB_SDS_URL(CHEMICAL)
URL_to_PDF(url)