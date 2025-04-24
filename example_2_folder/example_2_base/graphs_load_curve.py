#Master thesis Simon De Vadder graph file

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def load_curve(): 
    
    conso_jour = np.zeros(24*4)
    day_count = 0
    df = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2_folder//example_2_night//consumption_1.csv", header=None, index_col=None, sep=",")
    df_2 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2_folder//example_2_base//wh.csv", header=None, index_col=None, sep=",")
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
        #conso_jour[i - ind_begin] -= df_2.iloc[i,0]
    conso_jour /= day_count
    plt.plot(conso_jour, label="Consumption", color="blue")
    plt.ylim((0,1500))
    plt.show()
load_curve()
            
            
    
