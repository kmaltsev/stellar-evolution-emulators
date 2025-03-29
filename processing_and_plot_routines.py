import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import eep_read1

def mass_name_dict(name_mass_dict):
    dict1 = {}
    for i in range(0, len(name_mass_dict)):
        dict1[name_mass_dict.loc[i, 'mass0']] = name_mass_dict.loc[i, 'Unnamed: 0']
    return list(dict1.keys()), dict1 

phase_dict = {}
phase_dict[-1] = 'PMS'
phase_dict[0] = 'MS'
phase_dict[2] = 'RGB'
phase_dict[3] = 'CHeB'
phase_dict[4] = 'EAGB'
phase_dict[5] = 'TPAGB'
phase_dict[6] = 'postAGB'
phase_dict[9] = 'WR'

colors2 = ['blue', 'orange', 'purple', 'grey', 'brown', 'pink', 'red', 'yellow']

def mist_dataframe(eeps, basic_columns):
    basic_df = pd.DataFrame(columns = basic_columns)
    for i in range(0, len(basic_columns)):
        basic_column = basic_columns[i]
        basic_df[basic_column] = eeps[basic_column]
    return basic_df

def phases_cutWR(basic_df, phases_list, M0):    

    # selection of evolutionary sequences from ZAMS up to TACHeB, incl. WR phase
    for i in range(0, len(basic_df)):
        if basic_df.loc[i,'phase'] not in phases_list:
            basic_df = basic_df.drop(index=i)
    basic_df.reset_index(drop=True, inplace= True)
    if (M0 <= 110) and (M0 >= 60):
        for i in range(0, len(basic_df)):
            if (basic_df.loc[i, 'phase'] == 9) and (basic_df.loc[i, 'center_he4'] <= 1e-4):
                basic_df = basic_df.drop(index=i)
        basic_df.reset_index(drop=True, inplace= True)
    elif (M0 >=115):
        for i in range(0, len(basic_df)):
            if (basic_df.loc[i, 'center_he4'] <= 1e-4):
                basic_df = basic_df.drop(index=i)
        basic_df.reset_index(drop=True, inplace= True)
    return basic_df

# method to calculate the timescale-adapted evolutionary coordinate s
def Axes3_proxy(L, T, nuc):
    delta_c = 0
    path_length_list = [delta_c]    
    for i in range(0, len(L)-1):
        lumi, lumj = L[i], L[i+1]
        tempi, tempj = T[i], T[i+1]
        nuci, nucj = nuc[i], nuc[i+1]
        delta_l = abs(lumj-lumi)
        delta_T = abs(tempj-tempi)
        delta_nuc = abs(nuci-nucj)
        delta_c = delta_c + np.sqrt(delta_l**2+delta_T**2+delta_nuc**2)
        path_length_list.append(delta_c)  
    return path_length_list

def MIST_data_reader(initial_masses, dict1, new_path, phases_list, basic_columns):

    multiple_masses_df = dict()

    # file names
    for i in range(0, len(initial_masses)):
        # find file name for given initial mass input
        initial_mass = initial_masses[i]
        filename = dict1[initial_mass]    
    
        # load eep track
        eep = eep_read1.EEP(new_path+'/'+ filename + '.track.eep')
        #print(eep)
    
        # store the chosen data columns
        basic_df = mist_dataframe(eep.eeps, basic_columns)
        #print(basic_df)
        
        # cut out pre-main sequence, agb and post-agb phases
        basic_df = phases_cutWR(basic_df, phases_list, initial_mass)
        #print(basic_df)
        
        # calculate s
        path_length_list = Axes3_proxy(basic_df['log_L'], basic_df['log_Teff'], basic_df['log_center_Rho'])
        basic_df['s_tilde'] = path_length_list
        basic_df['s'] = path_length_list/path_length_list[-1] 

        # store in df
        multiple_masses_df[initial_mass] = basic_df
        #print(multiple_masses_df)
    return multiple_masses_df











