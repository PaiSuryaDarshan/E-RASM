# Un-Licensed. Free to use, copy, modify and merge.
# Please maintain attribution to the original author and the license.

import PBeta_HCSS

# First Step: Interpret True 
def catch_hazards(list_of_hazard_flags: list) -> list:
    
    index_values_TRUE = []
    raw_interpretation = []

    for index, flag in enumerate(list_of_hazard_flags):
            
        raw_interpretation.append(0)
        if flag == 1:
            index_values_TRUE.append(index)

    return index_values_TRUE, raw_interpretation

# Second Step: Interpret ROE and return final interpretation of hazards
def interpret_hazards(index_values_TRUE: list, raw_interpretation: list, list_of_ROE: list) -> list:
    # where code is converted to english 
    # Values of ROW produced by HCSS V2 are interpretted here
    for index in (index_values_TRUE):
        # SIMPLE
        if list_of_ROE[index] == 0:       
            raw_interpretation[index] = "\n" + "X"
        elif list_of_ROE[index] == 101:       
            raw_interpretation[index] = "\n" + str(1)
        elif list_of_ROE[index] == 102:       
            raw_interpretation[index] = "\n" + str(2)
        elif list_of_ROE[index] == 103:       
            raw_interpretation[index] = "\n" + str(3)
        # COMPLEX
        elif list_of_ROE[index] == 203:       
            raw_interpretation[index] = str(1) + "\n" + str(2)
        elif list_of_ROE[index] == 204:       
            raw_interpretation[index] = str(1) + "\n" + str(3)
        elif list_of_ROE[index] == 205:       
            raw_interpretation[index] = str(2) + "\n" + str(3)
        # ALL COMBINED
        elif list_of_ROE[index] == 306:       
            raw_interpretation[index] = str(1) + "\n" + str(2) + "\n" + str(3)
        # Uniterable (Err)
        else:
            raw_interpretation[index] = str(raw_interpretation[index])
            
        
    # Making final interpreatation
    final_interpretation = []

    for i in raw_interpretation:
        if i == 0:
            final_interpretation.append('')
        else:
            final_interpretation.append(i)

    return final_interpretation








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
        'h319  causes serious skin and eye irritation.' # (5, 102)
        ]

    hazards_list_2 = [
        'h225  highly flammable liquid and vapor.', # (8, 0)
        'h301 + h311 + h331  toxic if swallowed, in contact with skin or if inhaled.', # (3, 306)
        'h370  causes damage to organs (eyes, central nervous system).' #! (Null)
        ]

    hazards_list_3 = [
        'h225  highly flammable liquid and vapor.', # (8, 0)
        'h304  may be fatal if swallowed and enters airways.', 
        'h315  causes skin/Eye irritation.', # (5, 102)
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

    flag_list, ROE_list = PBeta_HCSS.process_hazards(hazards_list_2)

    index_values_TRUE, ROE_values = catch_hazards(flag_list)
    final_interpretation = interpret_hazards(index_values_TRUE, ROE_values, ROE_list)

    print(final_interpretation)

    counter = 0
    for i in flag_list:
        if i == True:
            # print(f"hazard found at {counter} with route {ROE_list[counter]}.")
            pass
        counter += 1 

if __name__ == "__main__":
    prior_information()
    test()
    pass