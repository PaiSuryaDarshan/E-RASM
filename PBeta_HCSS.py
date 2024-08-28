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
        # Define ROE variable (stores ROE code)
        ROE_value = 0
        interpreted_ROE.append(ROE_value)
        interpreted_flags[index] = 0

        # iterates each item in list looking for keywords
        for hazard in hazards_list:

            flag, ROE_value = haz_flag(hazard, locators[index], flag)
            if flag:
                # print(index, ROE_value)
                # Record interpretation
                interpreted_flags[index] = 1
                interpreted_ROE[index] += ROE_value
            else:
                pass
        
            # reset flags to default (False) before next iteration / cycle
            flag = False



    return interpreted_flags, interpreted_ROE


# ----------------------------------------------------------------
# TEST FUNCTIONS
# ----------------------------------------------------------------

def prior_information():
    print(("""
Index labels
    0: carcinogen
    1: teratogen
    2: mutagen
    3: toxic
    4: harmful
    5: irritant
    6: explosive
    7: pyrophoric
    8: flammable
    9: oxidising
    10:corrosive
    11:lachrymator
        
ROE_values (possible interpretations):
    Simple value:
        101: Inhalation
        102: Skin/Eye
        103: Swallow
    Complex value: (Arises out of a combination of routes)
        203: Inhalation + Skin/Eye
        204: Inhalation + Swallow
        205: Skin/Eye   + Swallow
    Total value:
        306: All possible routes (Inhalation, Skin/Eye, Swallow)
""").upper())

def test():
    # Sample values with expected results (INDEX, ROE_value)
    hazards_list_1 = [
        'h225  highly flammable liquid and vapor.', # (8, 0)
        'h319  causes serious eye irritation.' # (5, 102)
        ]

    hazards_list_2 = [
        'h225  highly flammable liquid and vapor.', # (8, 0)
        'h301 + h311 + h331  toxic if swallowed, in contact with skin or if inhaled.', # (3, 306)
        'h370  causes damage to organs (eyes, central nervous system).' #! (Null)
        ]

    hazards_list_3 = [
        'h225  highly flammable liquid and vapor.', # (8, 0)
        'h304  may be fatal if swallowed and enters airways.', 
        'h315  causes skin irritation.', # (5, 102)
        'h336  may cause drowsiness or dizziness.',  #! (Null)
        'h361d  suspected of damaging the unborn child.',  #! (Null)
        'h373  may cause damage to organs (central nervous system) through prolonged or repeated exposure if inhaled.',  #! (Null)
        'h412  harmful to aquatic life with long lasting effects.'# (4, 0)
        ]
    
    hazards_list_4 = [
        'h317  may cause an allergic skin reaction.',  #! (Null)
        'h373  may cause damage to organs through prolonged or repeated exposure.',  #! (Null)
        'h410  very toxic to aquatic life with long lasting effects.' # (3, 0)
        ]

    flag_list, ROE_list = process_hazards(hazards_list_1)

    print(flag_list)
    print(ROE_list)
    print()

    counter = 0
    for i in flag_list:
        if i == True:
            print(f"hazard found at {counter} with route {ROE_list[counter]}.")
        counter += 1 

if __name__ == "__main__":
    prior_information()
    # test()
    pass