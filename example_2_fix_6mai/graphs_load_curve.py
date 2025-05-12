#Master thesis Simon De Vadder graph file

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def load_curve(): 
    
    conso_jour = np.zeros(24*4)
    day_count = 0
    df = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//consumption_2.csv", header=None, index_col=None, sep=",")
    df_2 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//wh.csv", header=None, index_col=None, sep=",")
    for i in range(24): 
        conso = df[i]
        ind_begin = 0
        for j in range(35040):
            if j - ind_begin>= 96 : 
                ind_begin = j 
                day_count += 1
            conso_jour[j-ind_begin] += conso[j]
    
    ind_begin = 0
    for i in range(35040):
        if i - ind_begin>= 96 : 
            ind_begin = i 
        conso_jour[i - ind_begin] -= df_2.iloc[i,0]
    conso_jour /= day_count
    plt.plot(conso_jour, label="Consumption", color="blue")
    plt.ylim((0,1500))
    plt.show()
#load_curve()
    

def daily_heating_curve():
    conso_tot = np.zeros((365, 24))
    file = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2_fix_6mai//heating_electric_m2_0.csv", header=None, index_col=None, sep=",")
    for i in range(365):
        ind_begin = i*96
        ind_end = (i+1)*96
        for j in range(24):
            conso_tot[i,j] += np.sum(file.iloc[ind_begin:ind_end,j])/4
             
    mean_conso = np.zeros(365)
    for i in range(365):
        mean_conso[i] = np.mean(conso_tot[i,:])
        
    
    for i in range(24):
        plt.plot(conso_tot[:,i], '#b0c4de')
    plt.plot(mean_conso,'#4169e1', label="Mean value")
    plt.ylabel("Heating consumption (Wh /m2.day)")
    plt.xlabel("Day of the year")
    plt.title("Heating consumption")
    plt.show()

daily_heating_curve()
        
            
    
