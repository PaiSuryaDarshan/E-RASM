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
        print(f"using alt locator for section {section_number}")
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

# Function to automate start index
def start_index_marker(text: str, locator_substring: str) -> int:
    start_index = (text.find(locator_substring) + len(locator_substring))
    return start_index

# Function to automate start index
def end_index_marker(text: str, start_index: str, locator_substring: str) -> int:
    end_index = text[start_index:].find(locator_substring) + len(text[:start_index])
    return end_index

# Second Step: Identify and isolate required information from each section 
# store in their respective variables

# 1. Product Identifiers    (SEC-1) 
# CAS-NO
def get_cas_no(section_1_text: str) -> str:

    # SPECIFIC LOCATORS
    L_CAS_NO = "cas-no. : "
    # Generic locators
    l_space = " "

    text = section_1_text
    start_index = start_index_marker(text, L_CAS_NO)
    end_index   = end_index_marker(text, start_index, l_space)
    cas_no      = text[start_index:end_index]
    return cas_no

# 2. Substance Information  (SEC-3) 
# Molecular formula, Molecular weight
def get_molecular_info(section_3_text: str) -> tuple:

    # SPECIFIC LOCATORS
    L_MOL_FORMULA = "formula  : "
    L_MOL_WEIGHT = "weight  : "
    # Generic locators
    l_space = " "

    text = section_3_text

    # Molecular formula
    start_index = start_index_marker(text, L_MOL_FORMULA)
    end_index   = end_index_marker(text, start_index, l_space)
    mol_formula = text[start_index:end_index]
    # Molecular weight
    start_index = start_index_marker(text, L_MOL_WEIGHT)
    end_index   = end_index_marker(text, start_index, l_space)
    mol_weight  = text[start_index:end_index]

    if ',' in mol_weight:
        mol_weight = mol_weight.replace(',', '.')
    else:
        pass

    return mol_formula, mol_weight

# 3. Phys & Chem properties (SEC-9) 
# verify physical state != liquid, if false, grab density
def get_state(section_9_text: str) -> tuple:

    # SPECIFIC LOCATORS
    L_phys_state  = "physical state  "
    L_density     = "density  "
    # Generic locators
    l_space = " "

    text = section_9_text

    # state
    start_index = start_index_marker(text, L_phys_state)
    end_index   = end_index_marker(text, start_index, l_space)
    phys_state  = text[start_index:end_index]

    if phys_state == "liquid":
        # Get density
        start_index = start_index_marker(text, L_density)
        end_index   = end_index_marker(text, start_index, l_space)
        density     = text[start_index:end_index]

        if ',' in density:
            density = density.replace(',', '.')
        else:
            pass
    else:
        density = "N/A"

    return phys_state, density

# 4. Hazard statements      (SEC-2) 
# Split Hazard codes and Hazard statements

def get_hazards(section_2_text: str) -> tuple:

    haz_list_raw        = []
    hazard_list = []
    haz_codes       = []
    haz_statements  = []

    # SPECIFIC LOCATORS
    L_haz_lines = "hazard statement"
    L_haz_codes = "h"

    # Generic locators
    l_space = " "

    section_start_index = start_index_marker(section_2_text, L_haz_lines)
    text = section_2_text[section_start_index:]
    
    start_index = text.find(L_haz_codes)-1
    haz_text    = text[start_index:]

    # state
    # start_index = start_index_marker(text, L_haz_codes)-1
    # end_index   = start_index + 4
    # haz_lines  = text[start_index:end_index]

    haz_list_raw = haz_text.split('\n')

    for index, hazard in enumerate(haz_list_raw):
        if hazard.strip() == "" or hazard.strip()[0] == "=":
            continue
        elif hazard.strip()[0] != "h" and hazard.strip()[1].isdigit() == False and index == 0 :
            break
        elif hazard.strip()[0] != "h" and index != 0:
            hazard = (haz_list_raw[index - 1] + hazard).strip()
            hazard_list[-1] = hazard
        else:
            hazard_list.append(hazard.strip())

    return hazard_list



# Test variables
T_file_path     = './storage_directory/Atrazine.pdf'
T_CHEMICAL_NAME = 'Ethanol'
s1, s2, s3, s9 = auto_isolate_section(file_path=T_file_path)
print(get_hazards(s2))