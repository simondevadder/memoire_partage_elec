#Master thesis Simon De Vadder graph file

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def load_curve(): 
    
    conso_jour = np.zeros(24*4)
    cooking_jour = np.zeros(24*4)
    cold_jour = np.zeros(24*4)
    washing_jour = np.zeros(24*4)
    heating_jour = np.zeros(24*4)
    other_jour = np.zeros(24*4)
    wh_jour = np.zeros(24*4)
    day_count = 0
    df = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//consumption_2.csv", header=None, index_col=None, sep=",")
    df_2 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//wh.csv", header=None, index_col=None, sep=",")
    df_3 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//cooking.csv", header=None, index_col=None, sep=",")
    df_4 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//cold.csv", header=None, index_col=None, sep=",")
    df_5 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//washing.csv", header=None, index_col=None, sep=",")
    df_6 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//heating_electric_m2_0.csv", header=None, index_col=None, sep=",")
    df_7 = pd.read_csv("C://Users//simva//OneDrive//Documents//1 Master 2//Mémoire//code//memoire_partage_elec//example_2//other.csv", header=None, index_col=None, sep=",")
    
    for i in range(24): 
        conso = df[i]
        ind_begin = 0
        for j in range(35040):
            if j - ind_begin>= 96 : 
                ind_begin = j 
                day_count += 1
            conso_jour[j-ind_begin] += conso[j]
            heating_jour[j-ind_begin] += df_6.iloc[j,i]

            
    
    ind_begin = 0
    for i in range(35040):
        if i - ind_begin>= 96 : 
            ind_begin = i 
        conso_jour[i - ind_begin] -= df_2.iloc[i,0]
    conso_jour /= day_count
    
    ind_begin = 0
    day_count = 0
    for j in range(35040):
        if j - ind_begin>= 96 : 
            ind_begin = j 
            day_count += 1
        cooking_jour[j-ind_begin] += df_3.iloc[j,0]
        cold_jour[j-ind_begin] += df_4.iloc[j,0]
        washing_jour[j-ind_begin] += df_5.iloc[j,0]
        other_jour[j-ind_begin] += df_7.iloc[j,0]
        wh_jour[j-ind_begin] += df_2.iloc[j,0]
    cooking_jour /= 24* day_count
    cold_jour /= 24* day_count
    washing_jour /= 24* day_count
    heating_jour /= 24* day_count
    other_jour /= 24* day_count
    wh_jour /= 24* day_count
    
    hour_indices = np.arange(0, 96, 4)
    hour_labels = [f"{h}:00" for h in range(24)] 
    plt.plot(conso_jour, label="Consumption", color="blue")
    plt.xticks(hour_indices, hour_labels, rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Power (W)")
    plt.title("Consumption load curve (without water heaters)")
    plt.ylim((0,800))
    plt.show()
    
    plt.plot(cooking_jour, label="Cooking")
    plt.xticks(hour_indices, hour_labels, rotation=45)

    plt.xlabel("Time (15 min)")
    plt.ylabel("Power (W)")
    plt.title("Cooking load curve")
    plt.show()
    
    plt.plot(cold_jour, label="Cold load")
    plt.xticks(hour_indices, hour_labels, rotation=45)

    plt.xlabel("Time (15 min)")
    plt.ylabel("Power (W)")
    plt.title("Cold load curve")
    plt.show()
    
    plt.plot(washing_jour, label="Washing load")
    plt.xticks(hour_indices, hour_labels, rotation=45)

    plt.xlabel("Time")
    plt.ylabel("Power (W)")
    plt.title("Washing load curve")
    plt.show()
    
    plt.plot(heating_jour, label="Heating load")
    plt.xticks(hour_indices, hour_labels, rotation=45)

    plt.xlabel("Time ")
    plt.ylabel("Power (W/m2)")
    plt.ylim((0, 3))
    plt.title("Heating load curve")
    plt.show()
    
    plt.plot(other_jour, label="Other load")
    plt.xticks(hour_indices, hour_labels, rotation=45)

    plt.xlabel("Time ")
    plt.ylabel("Power (W)")
    plt.title("Other load curve")
    plt.show()
    
    plt.plot(wh_jour, label="Water heater load")
    plt.xticks(hour_indices, hour_labels, rotation=45)

    plt.xlabel("Time ")
    plt.ylabel("Power (W)")
    plt.title("Water heater load curve")
    plt.show()
    
load_curve()
            
            
    
