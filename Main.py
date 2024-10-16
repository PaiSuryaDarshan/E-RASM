# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

from docx import Document
import PBeta_HCSS
import P1
import P2
import P3
import P5
import time     # to calculate time elapsed

NAME = 'NEW_ATTEPT'
path = './template_directory/Blank Reaction Risk Assessment Form.docx'
# LIST_OF_CHEMICALS = ["ethanol", "Methanol", "Toluene", "Atrazine", "Oxalic acid", "Lycopene"]
LIST_OF_CHEMICALS = [
    "Cyclohexane",
    "Dichloromethane",
    "Dimethyl Sulfoxide",
    "Ethylene Glycol",
    "Methanol",
    "Ethanol",
    "Octanol",
    "Toluene"
    ]
# LIST_OF_CHEMICALS = ["Ethanol"]

    
document = Document(path)
haz_table = document.tables[0]

# Start time
start_time = time.time()

for chemical_number_index, chemical in enumerate(LIST_OF_CHEMICALS):
    # Standardizing text
    CHEMICAL = chemical.capitalize()
    
    # P1 - Download SDS file and obtain chemical name
    url             = P1.GRAB_SDS_URL(CHEMICAL)
    file_path       = P1.URL_to_PDF(url, CHEMICAL)
    CHEMICAL_NAME   = P1.obtain_name(file_path, CHEMICAL)

    # P2 - SDS Parsing
    sec_1, sec_2, sec_3, sec_9 = P2.auto_isolate_section(file_path=file_path)

    ## VALUE retrieval
    VALUE_cas_no = P2.get_cas_no(sec_1)
    VALUE_formula, VALUE_weight = P2.get_molecular_info(sec_3)
    VALUE_state, VALUE_density = P2.get_state(sec_9)
    VALUE_hazards = P2.get_hazards(sec_2)

    # Pβ - HCSS V2.2
    haz_flags, ROE_list = PBeta_HCSS.process_hazards(VALUE_hazards)
    
    # P3 - Flag and code interpreter
    index_values_TRUE, ROE_values = P3.catch_hazards(haz_flags)
    final_interpretation_haz_only = P3.interpret_hazards(index_values_TRUE, ROE_values, ROE_list)
    
    # P4 - Document preparation done manually
    # Hazard table has 25 rows on it by default, excess rows will be deleted at the end of loop.

    # P5 - Document entry
    FINAL_ENTRY = P5.prepare_final_list(final_interpretation_haz_only, CHEMICAL_NAME, VALUE_weight, VALUE_density)

    # print(f"CAS-No : {VALUE_cas_no}")
    # print(f"Formula: {VALUE_formula}")
    # print(f"Weight : {VALUE_weight}")
    # print(f"State  : {VALUE_state}")
    # print(f"Density: {VALUE_density}")
    # print(f"Hazards: {VALUE_hazards}")
    # print(f"Haz_tags:{final_interpretation_haz_only}")
    # print(f"Haz_tags:{len(final_interpretation_haz_only)} items")
    # print()
    # print(f"-------------------------------------------------------------------------------------------------------")
    # print(f"FINAL ENTRY TO APPEND TO TABLE")
    # print(f"{FINAL_ENTRY}")

    P5.make_table_entry(chemical_number_index, FINAL_ENTRY, haz_table)
    document.save(f'./Final Docs/{NAME}.docx')

    # P5 - Document clean up
    P5.del_excess_rows(NAME)









# -----------------------------------------------------------------------------------------------
# Log information 
# -----------------------------------------------------------------------------------------------

print("""
-----------------------------------------------------------------------------------------------
                                     Log information 
-----------------------------------------------------------------------------------------------
""")
# End time
end_time = time.time()
time_elapsed = round(end_time-start_time, 2)
# Number of chemicals
no_of_chemicals = len(LIST_OF_CHEMICALS)
# Rate 
rate = round(time_elapsed/no_of_chemicals, 2)
# Log statement
print(f"Number of chemicals                 : {no_of_chemicals}")
print(f"Time elapsed                        : {time_elapsed} seconds")
print(f"Estimated Rate of download/upload   : {rate} seconds/chemical")