# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

import P1
from pypdf import PdfReader

# First Step: Identify and split different sections 
# store them in their respective variables
def isolate_section(
        file_path: str,
        section_number: int, 
        section_start_locator: str, 
        section_end_locator: str, 
        section_alt_end_locator: str) -> str:
    
    # Enabling Reader
    reader  = PdfReader(file_path)
    TEXT    = ''

    # Extracting text from each page in the PDF file
    for page in reader.pages:
        TEXT += (page.extract_text()).lower()

    # Finding Section with required information
    if section_end_locator in TEXT:
        pass
    else:
        section_end_locator = section_alt_end_locator

    section_start_index = (TEXT.find(section_start_locator) + len(section_start_locator))
    section_end_index   = (len(TEXT[:section_start_index]) + TEXT[section_start_index:].find(section_end_locator))

    section_of_interest_raw = TEXT[section_start_index:section_end_index]

    section_of_interest = (f"\n=================================================\nSection {section_number}\n=================================================\n"+ 
                            section_of_interest_raw+ 
                            "================================================= \n")

    return section_of_interest

def auto_isolate_section(file_path: str) -> tuple:
    # to be updated
    sec_1 = ''
    sec_2 = ''
    sec_3 = ''
    sec_9 = ''
    # section_1 locators
    section_1_start_locator   = "1.1 "
    section_1_end_locator     = "1.2 "
    section_1_alt_end_locator = "section 2"
    # section_2 locators
    section_2_start_locator   = "2.2 "
    section_2_end_locator     = "precautionary statement"
    section_2_alt_end_locator = "section 3"
    # section_3 locators
    section_3_start_locator   = "3.1 "
    section_3_end_locator     = "index -no."
    section_3_alt_end_locator = "section 4"
    # section_9 locators
    section_9_start_locator   = "9.1 "
    section_9_end_locator     = "9.2 "
    section_9_alt_end_locator = "section 10"

    sec_1 = isolate_section(file_path, 1, section_1_start_locator, section_1_end_locator, section_1_alt_end_locator)
    sec_2 = isolate_section(file_path, 2, section_2_start_locator, section_2_end_locator, section_2_alt_end_locator)
    sec_3 = isolate_section(file_path, 3, section_3_start_locator, section_3_end_locator, section_3_alt_end_locator)
    sec_9 = isolate_section(file_path, 9, section_9_start_locator, section_9_end_locator, section_9_alt_end_locator)

    return sec_1, sec_2, sec_3, sec_9

# Test variables
#T_file_path     = './storage_directory/Ethanol.pdf'
#T_CHEMICAL_NAME = 'Ethanol'
#s1, s2, s3, s9 = auto_isolate_section(file_path=T_file_path)
#print(s1)





















# Second Step: Identify and isolate required information from each section 
# store in their respective variables

# 1. Product Identifiers    (SEC-1) 
# CAS-NO



# 2. Substance Information  (SEC-3) 
# Molecular formula, Molecular weight



# 3. Phys & Chem properties (SEC-9) 
# verify physical state != liquid, if false, grab density



# 4. Hazard statements      (SEC-2) 
# Split Hazard codes and Hazard statements


