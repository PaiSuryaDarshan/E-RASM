import P1
import P2
import time     # to calculate time elapsed


list_of_chemicals = ["ethanol", "Methanol", "Toluene"]

# Start time
start_time = time.time()

for chemical in list_of_chemicals:
    # Standardizing text
    CHEMICAL = chemical.capitalize()
    
    # P1 - Download SDS file and obtain chemical name
    url             = P1.GRAB_SDS_URL(CHEMICAL)
    file_path       = P1.URL_to_PDF(url, CHEMICAL)
    CHEMICAL_NAME   = P1.obtain_name(file_path, CHEMICAL)

    # P2 - SDS Parsing
    sec_1, sec_2, sec_3, sec_9 = P2.auto_isolate_section(file_path=file_path)
    print(sec_1)













# -----------------------------------------------------------------------------------------------
# Log information 
# -----------------------------------------------------------------------------------------------

# End time
end_time = time.time()
time_elapsed = round(end_time-start_time, 2)
# Number of chemicals
no_of_chemicals = len(list_of_chemicals)
#rate 
rate = round(time_elapsed/no_of_chemicals, 2)
# Log statement
print(f"Number of chemicals: {no_of_chemicals}")
print(f"Time elapsed: {time_elapsed} seconds")
print(f"Estimated Rate of download: {rate} seconds/chemical")