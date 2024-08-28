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
            
        


    # Making final interpretation
    final_interpretation = []

    for i in raw_interpretation:
        if i == 0:
            final_interpretation.append('')
        else:
            final_interpretation.append(i)

    # Test "final interpretation"
    # final_interpretation = [
    #     "carcinogen", "teratogen", "mutagen", "toxic", 
    #     "harmful", "irritant", "explosive", "pyrophoric", 
    #     "flammable", "oxidising", "corrosive", "lachrymator"
    # ]

    # C_T_M Table Entry 1
    carcinogen = final_interpretation.pop(0)            # pops carcinogen (0th index on original list)
    teratogen  = final_interpretation.pop(0)            # pops teratogen  (1th index on original list)
    mutagen    = final_interpretation.pop(0)            # pops mutagen    (3th index on original list)
    c_t_m        = (carcinogen + teratogen + mutagen).strip()
    final_interpretation.insert(0 , c_t_m)

    # H_I Table Entry 3
    harmful    = final_interpretation.pop(2)            # pops harmful  (4th index on original list)
    irritant   = final_interpretation.pop(2)            # pops irritant (5th index on original list)
    h_i        = (harmful+irritant).strip()
    final_interpretation.insert(2 , h_i)

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

Re-arranged labels
    0: carcinogen, teratogen, mutagen
    1: toxic
    2: harmful, irritant
    3: explosive
    4: pyrophoric
    5: flammable
    6: oxidising
    7: corrosive
    8: lachrymator
        
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
        'h225  highly flammable liquid and vapor.', 
        'h319  causes serious skin and eye irritation.'
        ]

    hazards_list_2 = [
        'h225  highly flammable liquid and vapor.', 
        'h301 + h311 + h331  toxic if swallowed, in contact with skin or if inhaled.',
        'h370  causes damage to organs (eyes, central nervous system).'
        ]

    hazards_list_3 = [
        'h225  highly flammable liquid and vapor.', 
        'h304  may be fatal if swallowed and enters airways.', 
        'h315  causes skin/Eye irritation.', 
        'h336  may cause drowsiness or dizziness.', 
        'h361d  suspected of damaging the unborn child.', 
        'h373  may cause damage to organs (central nervous system) through prolonged or repeated exposure if inhaled.', 
        'h412  harmful to aquatic life with long lasting effects.'
        ]
    
    hazards_list_4 = [
        'h317  may cause an allergic skin reaction.', 
        'h373  may cause damage to organs through prolonged or repeated exposure.', 
        'h410  very toxic to aquatic life with long lasting effects.' 
        ]
    
    hazards_list_5 = [
        'h225  highly flammable liquid and vapor.', 
        'h304  may be fatal if swallowed and enters airways.', 
        'h315  causes skin/Eye irritation.',
        'h315  causes swallow harmfulness.',
        'h336  may cause drowsiness or dizziness.', 
        'h361d  suspected of damaging the unborn child.', 
        'h373  may cause damage to organs (central nervous system) through prolonged or repeated exposure if inhaled.', 
        'h412  harmful to aquatic life with long lasting effects.'
        ]

    flag_list, ROE_list = PBeta_HCSS.process_hazards(hazards_list_5)

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