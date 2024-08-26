import os
import sys_checks
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect
import time

CHEMICAL = {"TEST.pdf"}

final_download_link = 'https://www.sigmaaldrich.com/IN/en/sds/mm/6.18663?userType=anonymous'

def test_file_download(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        
        page.goto(url)
        time.sleep(15)
        with page.expect_download() as download_info:
            page.get_by_role('button').click()
        download = download_info.value

        print(download.path())

        page.close()

    return

test_file_download(final_download_link)