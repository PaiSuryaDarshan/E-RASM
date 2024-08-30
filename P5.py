# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

from docx import Document

CHEMICAL_NAME   = ""
MOL_WEIGHT      = ""
DENSITY         = ""
QUANTITY        = ""
MMOL            = ""
EQUIVALENT      = ""
# HAZARDS       = "" (x 9)
OTHERS_TO_SPECIFY = ""

# First Step: 
# Preparing list that covers the full length of the table (Final Touches)

def prepare_final_list(
    interpreted_haz_list: list, 
    CHEMICAL_NAME = "", 
    MOL_WEIGHT = "", 
    DENSITY = "", 
    QUANTITY = "", 
    MMOL = "", 
    EQUIVALENT = "", 
    OTHERS_TO_SPECIFY = ""
    ) -> list:

    final_entry = []

    final_entry.append(CHEMICAL_NAME)
    final_entry.append(MOL_WEIGHT)

    # remove decimal point, (if present)
    DENSITY_STRIPED = DENSITY.replace('.', '')
    if DENSITY_STRIPED.isnumeric():
        final_entry.append(DENSITY)
    else:
        final_entry.append("")
    
    final_entry.append(QUANTITY)
    final_entry.append(MMOL)
    final_entry.append(EQUIVALENT)

    for haz_tag in interpreted_haz_list:
        final_entry.append(haz_tag)
    
    final_entry.append(OTHERS_TO_SPECIFY)

    return final_entry

# Second Step: 
# Entering value into document the document

# document = Document('./template_directory/T_RiskAssessment_Blank.docx')

# print(document.tables[0])

# document.save('./Test/test_draft.docx')