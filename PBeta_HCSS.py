# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

# Function to print variable name
#TODO:

# Flag function based on provided substring
def haz_flag(string: str, keywords: str, flag_variable: bool, ROE_value=0):
    # Locate the keyword in the string
    for keyword in keywords:
        if keyword in string:
            flag_variable = True
        else:
            pass

    # If the keyword is found, check for ROE
    # ROE Locators
    inhalation_locators = [101, "inhal"]
    skin_locators       = [102, "skin"]
    eyes_locators       = [102, "eye"]
    swallow_locators    = [103, "swall"]

    ROE_list = [
        inhalation_locators, 
        skin_locators, 
        eyes_locators, 
        swallow_locators
    ]

    if flag_variable == True:
        for route_list in ROE_list:
            for route in route_list[1:]:
                if route in string:
                    ROE_value += route_list[0]
                else:
                    pass
    return flag_variable, ROE_value

# Function to process and flag hazards
def process_hazards(hazards_list: str) -> list[bool]:

    # list of existing hazards
    interpreted_flags  = []
    # list of Routes Of Exposure (ROE)
    interpreted_ROE    = []

    # flags are initially set to False 
    #1
    carcinogen  = False
    teratogen   = False
    mutagen     = False
    #2
    toxic       = False
    #3
    harmful     = False
    irritant    = False
    #4
    explosive   = False
    #5
    pyrophoric  = False
    #6
    flammable   = False
    #7
    oxidising   = False
    #8
    corrosive   = False
    #9
    lachrymator = False

    # All possible locators are identified
    carcinogen_locators = ["carcinogen"]
    teratogen_locators = ["teratogen"]
    mutagen_locators = ["mutagen"]
    toxic_locators = ["tox"]
    harmful_locators = ["harm"]
    irritant_locators = ["irri"]
    explosive_locators = ["explo"]
    pyrophoric_locators = ["fire"]
    flammable_locators = ["flamm"]
    oxidising_locators = ["oxidi"]
    corrosive_locators = ["corr"]
    lachrymator_locators = ["lachrymator"]

    # flag list
    interpreted_flags  = [
    carcinogen, teratogen, mutagen, toxic, 
    harmful, irritant, explosive, pyrophoric, 
    flammable, oxidising, corrosive, lachrymator
    ]

    # locator list
    locators = [
        carcinogen_locators, 
        teratogen_locators, 
        mutagen_locators,
        toxic_locators,
        harmful_locators,
        irritant_locators,
        explosive_locators,
        pyrophoric_locators,
        flammable_locators,
        oxidising_locators,
        corrosive_locators,
        lachrymator_locators
    ]

    for index, flag in enumerate(interpreted_flags):
        # iterates each item in list looking for keywords
        for hazard in hazards_list:
            flag, ROE_value = haz_flag(hazard, locators[index], flag)
            if flag:
                print(index, ROE_value)
            else:
                pass

    return interpreted_flags, interpreted_ROE



# TEST

hazards_list = [
    'h225  highly flammable liquid and vapor.', # 0
    'h304  may be fatal if swallowed and enters airways.', # 103
    'h315  causes skin irritation.', # 102
    'h336  may cause drowsiness or dizziness.', # FALSE
    'h361d  suspected of damaging the unborn child.', # FALSE
    'h373  may cause damage to organs (central nervous system) through prolonged or repeated exposure if inhaled.', # FALSE
    'h412  harmful to aquatic life with long lasting effects.' # FALSE
    ]

flag_list, ROE_list = process_hazards(hazards_list)

print(len(ROE_list))