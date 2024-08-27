# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

from playwright.sync_api import sync_playwright
import requests
import time
from pypdf import PdfReader

# Function that obtains SDS PDF download link
def GRAB_SDS_URL(CHEMICAL: str) -> str:
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
def URL_to_PDF(url: str, CHEMICAL: str) -> str:

    headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'}
    file_path = f"./storage_directory/{CHEMICAL}.pdf"

    response = requests.get(url, stream =True, headers = headers)

    # Check if the chemical SDS was retrieved successfully
    if response.status_code == 200:
        pass
    else:
        print(f"RESPONSE ERROR - BLACKLISTED - [{CHEMICAL}]")
        print(response)
        print(response.status_code)

    content = response.content

    with open(file_path, "wb") as file:
        file.write(content)
        file.close()
    
    return file_path

# Function to check if the SDS PDF is readable 
# (also returns official/standard name)
def obtain_name(file_path: str, CHEMICAL: str) -> str:

    # Cooldown time for computer to completely execute the file download
    time.sleep(1)

    # Creating variables
    CHEMICAL_NAME = ''
    text    = ''

    # Enabling Reader
    reader  = PdfReader(file_path)

    # Extracting text from each page in the PDF file
    for page in reader.pages:
        text += (page.extract_text()).lower()
    
    # Finding the chemical name within the text using common flags
    section_locator = "1.1 product identifier"
    start_locator = "product name  :"
    end_locator   = ":"

    ## Finding Section with required information
    section_index = (text.find(section_locator) + len(section_locator))
    section_of_interest = text[section_index:]

    ## Finding string of information in section
    name_start_index = (section_of_interest.find(start_locator) + len(start_locator))
    name_end_index = section_of_interest[name_start_index:].find(end_locator)

    ## Assigning variable
    CHEMICAL_NAME_raw = section_of_interest[name_start_index : name_end_index]
    CHEMICAL_NAME = CHEMICAL_NAME_raw.split()[0].capitalize()

    # Confirm NAME (Manual Input required)
    confirmation_flag = input(
        f"""
        ================================================================
        Is Name of chemical: {CHEMICAL_NAME}?
        Press ENTER to confirm (or) 
        Type 'alt' to use query name as chemical name (or)
        Type an alternate name.
        ================================================================
        """)

    if confirmation_flag.strip() == '':
        print(f"Name: {CHEMICAL_NAME}")
    elif confirmation_flag.strip().lower() == 'alt':
        # use query name as CHEMICAL_NAME
        CHEMICAL_NAME = CHEMICAL
        print(f"Query name used: {CHEMICAL_NAME}" + ".")
    else:
        # suggested alternate name
        CHEMICAL_NAME = confirmation_flag.capitalize().strip() + '(r)'
        print(f"Name modified: {CHEMICAL_NAME}")

    return CHEMICAL_NAME