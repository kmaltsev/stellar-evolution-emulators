#!/usr/bin/env python

import numpy as np
from tensorflow import keras 
#from tensorflow.keras.models import load_model
import tensorflow 
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

# color map for discriminating stellar evolution tracks in the HR and Kiel diagram
def color_map_color(value, cmap_name='Wistia', vmin=0, vmax=1):
    # norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(norm(abs(value)))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color

# predicting stellar observables with the ffNN model
def HR_and_Kiel_track(M_ZAMS, s_sampling, ffNN):
    L_vals, Teff_vals, g_vals = [], [], []
    for s in s_sampling:
        logL_logTeff_logg_s = ffNN.predict(np.array([s, np.log10(M_ZAMS)]).reshape(1,-1))
        L_vals.append(logL_logTeff_logg_s[:,0]), Teff_vals.append(logL_logTeff_logg_s[:,1]), g_vals.append(logL_logTeff_logg_s[:,2])
    return L_vals, Teff_vals, g_vals

# plotting routines for the HR and Kiel diagram
def plot_HR(L_vals, Teff_vals, M_ZAMS):
    plt.figure()
    plt.scatter(Teff_vals, L_vals, s = 2.5)
    plt.xlabel(r"$\log T_\mathrm{eff} / K$", fontsize = 14)
    plt.ylabel(r"$\log L / L_\odot$", fontsize = 14)
    plt.gca().invert_xaxis()
    plt.title(r"$M_\mathrm{ZAMS}/M_\odot=$"+str(M_ZAMS), fontsize = 14.5)
    plt.show()     
def plot_Kiel(g_vals, Teff_vals, M_ZAMS):
    plt.figure()
    plt.scatter(Teff_vals, g_vals, s = 2.5)
    plt.xlabel(r"$\log T_\mathrm{eff} / \mathrm{K}$", fontsize = 14)
    plt.ylabel(r"$\log g / \mathrm{[cm \cdot s^{-2}]}$", fontsize = 14)
    plt.gca().invert_xaxis()
    plt.title(r"$M_\mathrm{ZAMS}/M_\odot=$"+str(M_ZAMS), fontsize = 14.5)
    plt.show() 

# scaled age variable
def t_calc(logt_zams, logt_tacheb, log_t):
    t_tilde = (log_t - logt_zams)/(logt_tacheb - logt_zams)
    return t_tilde

# prediction of the stellar observables at any age and ZAMS mass using the two-step interpolation scheme
def observables_fixed_tau_MZAMS(test_age, log_M_ZAMS, gpr_modelTA, gpr_modelTE, knn_model, ffNN):
    
    # stellar ages at ZAMS and at the end of CHeB
    logt_zams = gpr_modelTA.predict(log_M_ZAMS.reshape(1,-1))
    logt_tacheb = gpr_modelTE.predict(log_M_ZAMS.reshape(1,-1))    
    
    # scaled age variable
    t_scaled = t_calc(logt_zams, logt_tacheb, np.log10( test_age ))   
            
    # knn prediction of the timescale-adapted evolutionary coordinate 
    s_pred = knn_model.predict(np.array([t_scaled, log_M_ZAMS], dtype = 'float64').reshape(1,-1))
            
    # ffnn prediction of observables
    output_nn = ffNN.predict(np.array([float(s_pred), log_M_ZAMS]).reshape(1,-1))
    
    return output_nn

# routine for calculating isochrones in the HR diagram
def isochrone_computation(log_Mini, iso_values, gpr_modelTA, gpr_modelTE, knn_model, ffNN):
    
    # Prediction of (log-scaled) stellar age at ZAMS & at TACHeB, for the given ZAMS masses
    log_zams_mini = gpr_modelTA.predict(log_Mini.reshape(-1,1))
    log_tacheb_mini = gpr_modelTE.predict(log_Mini.reshape(-1,1))
    
    # data tables to fill    
    iso_dict = {}
    all_data_lists = []

    # for each isochrone value, ...
    for t in iso_values:

        iso_vals = pd.DataFrame(columns = ["logL", "logT", "logg"])
        T_vals, L_vals, g_vals = [], [], [] 
    
        # ...., calculate for each sampled ZAMS mass ...
        for i in range(0, len(log_Mini)):
            log_M_val = log_Mini[i]
        
            # 1) ... the ages at ZAMS & at TACHeB 
            log_zams, log_tacheb = log_zams_mini[i], log_tacheb_mini[i]
        
            # 2) ... the time past the star's ZAMS age
            test_age = 10.**log_zams+t 
       
            # 3) ... the observables at that test age, if the test age is within the age range
            if test_age < 10.**log_tacheb: 
        
                # scaled age variable calculation
                t_scaled = t_calc(log_zams, log_tacheb, np.log10( test_age ))
            
                # knn prediction of the timescale-adapted evolutionary coordinate 
                s_pred = knn_model.predict(np.array([t_scaled, log_M_val]).reshape(1,-1))
            
                # ffnn prediction of observables
                output_nn = ffNN.predict(np.array([float(s_pred), log_M_val]).reshape(1,-1))
            
                # store logL, logTeff & logg predictions in lists
                L_vals.append(output_nn[0,0]), T_vals.append(output_nn[0,1]), g_vals.append(output_nn[0,2])
                
                # store data frame containing all pertinent variables
                all_data_lists.append([output_nn[0,0], output_nn[0,1], output_nn[0,2], log_M_val, np.log10(t), np.log10(test_age), t_scaled])
    
        # extracting logL, logTeff and logg values over all ZAMS masses (single isochrone)
        iso_vals.logL, iso_vals.logT, iso_vals.logg = L_vals, T_vals, g_vals
        # ... and storing them in dict
        iso_dict[t] = iso_vals
    # integral data frame with the observables, zams masses and ages
    all_columns_df = pd.DataFrame(all_data_lists, columns = ["logL", "logTeff", "logg", "logMini", "isochrone", "test_age", "t_scaled"])
    
    return iso_dict, all_columns_df