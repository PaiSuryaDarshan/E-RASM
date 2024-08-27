import P1

list_of_chemicals = ["ethanol"]

for chemical in list_of_chemicals:
    # Standardizing text
    CHEMICAL = chemical.capitalize()
    
    # P1 - Download SDS file and obtain chemical name
    url             = P1.GRAB_SDS_URL(CHEMICAL)
    file_path       = P1.URL_to_PDF(url, CHEMICAL)
    CHEMICAL_NAME   = P1.obtain_name(file_path, CHEMICAL)

    # P2 - SDS Parsing
    