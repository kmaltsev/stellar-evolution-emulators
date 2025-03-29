import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys

####################################################################################################
############################################### Paths ##############################################
####################################################################################################

# paths
data_path = 'data/MIST' # original non-rotating solar-metallicity MIST stellar models
webint_path = data_path # additional tracks generated  using the MIST Web Interpolator
test_path =  data_path # hold-out stellar tracks for testing the accuracy of HNNI

import eep_read1
from processing_and_plot_routines import *

####################################################################################################
############################################ ZAMS masses & test data ###############################
####################################################################################################

## mass dictionaries converting names of file (containing evolutionary tracks) into ZAMS mass values 
name_mass_dict = pd.read_excel('data/name-massMIST.xlsx', engine='openpyxl')
name_mass_dict2 = pd.read_excel('data/name-massWebInt.xlsx', engine='openpyxl')

# definition of the ZAMS mass range (width of parameter space)
entire_mass_range, dict1 = mass_name_dict(name_mass_dict)
webint_masses, dict2 = mass_name_dict(name_mass_dict2)
initial_masses = entire_mass_range[20:] # with this, M_ZAMS within range (0.7, 300) in solar mass units
all_masses = np.sort(initial_masses + webint_masses)

# loading test data stellar evolution tracks
name_mass_dict3 = pd.read_excel('data/name-massTest.xlsx', engine='openpyxl')
initial_massesEEP, dict3 = mass_name_dict(name_mass_dict3)
initial_massesEEP = initial_massesEEP[1:]

######################################################################################################################
####################################################### MIST catalog specific ########################################
######################################################################################################################

# selection of evolutionary phases (numericals correspond to the MIST labels, see readme file)
phases_list = [0, 2, 3, 9] 
CHeB_augmentation = False

# stellar evolution variables needed here
basic_columns = ['log_L', 'log_Teff', 'star_age', 'phase', 'log_center_Rho', 'center_he4', "log_center_T", 'log_g']


####################################################################################################
############################################# HNNI #################################################
####################################################################################################

# linear interpolation scheme
def linear_int(x1, x2, y1, y2, x):
    return y1 + (y2-y1)/(x2-x1)*(x-x1)

# nearest min-max neighbors
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


# method to merge two dictionaries
def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def neighbor_points(values, test):
    diff = values - test
    if len(values[diff >=0] > 0):
        upper = find_nearest(values[diff >= 0 ],test)
    else:
        upper = np.amax(values)
    if len(values[diff <=0] > 0):
        lower = find_nearest(values[diff <= 0 ],test)
    else:
        lower = np.amin(values)
    return lower, upper

def HNNI_general(catalog, test_mass, test_s, target):
    all_masses = sorted(catalog.keys())
    
    # upper and lower ZAMS mass grid points
    m_min, m_max = neighbor_points(np.array(all_masses), test_mass)
    
    # s values at mmin and mmax
    if not m_min == m_max:
        smin_values, smax_values = catalog[m_min]["s"], catalog[m_max]["s"]
    
        # target variable values at mmin and mmax
        target_min_values, target_max_values = catalog[m_min][target], catalog[m_max][target]
    
        # closest (from above and from below) s values to given test_s, at mmin and mmax
        smin1_value, smin2_value = neighbor_points(np.array(smin_values), test_s)
        smax1_value, smax2_value = neighbor_points(np.array(smax_values), test_s)
    
        # get their indices (in mmin and mmax tracks at given test s)
        index1_min = np.where(np.array(smin_values)==smin1_value) 
        index1_max = np.where(np.array(smin_values)==smin2_value) 
        index2_min = np.where(np.array(smax_values)==smax1_value)
        index2_max = np.where(np.array(smax_values)==smax2_value)        

        # interpolation along s axis
        if not smin1_value == smin2_value:
            target_s_min = linear_int(smin1_value, smin2_value, np.array(target_min_values)[index1_min], np.array(target_min_values)[index1_max], test_s)
        elif smin1_value == smin2_value:
            target_s_min = target_min_values[int(np.array(index1_min))]
            
        if not smax1_value == smax2_value:
            target_s_max = linear_int(smax1_value, smax2_value, np.array(target_max_values)[index2_min], np.array(target_max_values)[index2_max], test_s)
        
        elif smax1_value == smax2_value:
            target_s_max = target_max_values[int(np.array(index2_min))]
        
        # interpolation along log ZAMS mass axis
        target_s = linear_int(np.log10(m_min), np.log10(m_max), target_s_min, target_s_max, np.log10(test_mass))
         
    
    elif m_min == m_max:
        s_values = catalog[m_min]["s"]
        target_values = catalog[m_min][target]
        smin_value, smax_value = neighbor_points(np.array(s_values), test_s)
        index_min = np.where(np.array(s_values)==smin_value)
        index_max = np.where(np.array(s_values)==smax_value)
        if not index_min == index_max:
            target_s = linear_int(smin_value, smax_value, np.array(target_values)[index_min], np.array(target_values)[index_max], test_s)
        elif index_min == index_max:
            target_s = target_values[int(np.array(index_min))] 
    return float(target_s)










