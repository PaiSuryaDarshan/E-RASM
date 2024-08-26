# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

import sys_checks
from playwright.sync_api import sync_playwright

WEBSITE = "https://www.sigmaaldrich.com/"
CHEMICAL = "methyl alcohol".capitalize()

# First Step: Accessing WEBSITE

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page    = browser.new_page()
    page.goto(WEBSITE)
    page.get_by_role("textbox", name="Type in Product").fill(CHEMICAL)
    page.get_by_test_id("header-search-submit-search-wrapper").click()

# Second Step: Checking the search results

    page.get_by_role("button", name="sds").click()
    page.kis