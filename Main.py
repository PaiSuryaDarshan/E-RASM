import PBeta_HCSS
import P1
import P2
import P3
import time     # to calculate time elapsed


LIST_OF_CHEMICALS = ["ethanol", "Methanol", "Toluene", "Atrazine", "Oxalic acid", "Lycopene"]
# LIST_OF_CHEMICALS = ["ethanol", "Methanol", "Toluene", "Atrazine"]
# LIST_OF_CHEMICALS = ["Oxalic acid", "Lycopene"]

# Start time
start_time = time.time()

for chemical in LIST_OF_CHEMICALS:
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

    # P3
    haz_flags, ROE_list = PBeta_HCSS.process_hazards(VALUE_hazards)
    index_values_TRUE, ROE_values = P3.catch_hazards(haz_flags)
    final_interpretation_haz_only = P3.interpret_hazards(index_values_TRUE, ROE_values, ROE_list)
    
    print(f"CAS-No : {VALUE_cas_no}")
    print(f"Formula: {VALUE_formula}")
    print(f"Weight : {VALUE_weight}")
    print(f"State  : {VALUE_state}")
    print(f"Density: {VALUE_density}")
    print(f"Hazards: {VALUE_hazards}")
    print(f"Haz_tags:{final_interpretation_haz_only}")













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
#rate 
rate = round(time_elapsed/no_of_chemicals, 2)
# Log statement
print(f"Number of chemicals: {no_of_chemicals}")
print(f"Time elapsed: {time_elapsed} seconds")
print(f"Estimated Rate of download: {rate} seconds/chemical")