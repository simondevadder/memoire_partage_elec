# file to draw graph from gurobi results

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def func_1():
    file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/first_simu/resultats_simulations_merged.csv"

    df = pd.read_csv(file)
    # print(df)
    
    n_households = df["n_households"].to_numpy()
    objective = df["objective"].to_numpy()
    kWc = df["kWc"].to_numpy()
    wh_battery = df["wh_battery"].to_numpy()
    puissance_totale = df["puissance_totale"].to_numpy()
    puissance_produite = df["puissance_produite"].to_numpy()
    tot_conso = df["tot_conso"].to_numpy()

    # print("n_households:", n_households)
    # print("objective:", objective)
    # print("kWc:", kWc)
    # print("wh_battery:", wh_battery)
    # print("puissance_totale:", puissance_totale)
    # print("puissance_produite:", puissance_produite)
    # print("tot_conso:", tot_conso)
    
    # print("len p totale:", len(puissance_totale))
    # print("len p produite:", len(puissance_produite))
    # print("len tot conso:", len(tot_conso))
    self_suffi = puissance_totale / tot_conso * 100
    self_conso = puissance_totale / puissance_produite * 100

    # print("self_suffi:", self_suffi)
    # print("self_conso:", self_conso)
    
    tot_conso = tot_conso / 1000000  # Convert to MWh if needed
    puissance_totale = puissance_totale / 1000000  # Convert to MWh if needed
    puissance_produite = puissance_produite / 1000000  # Convert to MWh if needed
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(tot_conso, self_suffi, label='Self Sufficiency (%)', color='blue', marker='o')
    ax1.plot(tot_conso, self_conso, label='Self Consumption (%)', color='orange', marker='x')
    ax1.set_xlabel('Total Consumption (MWh/year)')
    ax1.set_ylabel('Percentage (%)')
    ax1.legend()
    plt.show()
    
    fig, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(tot_conso, kWc, label='kWp', color='green', marker='o')
    ax2.set_xlabel('Total Consumption (MWh/year)')
    ax2.set_ylabel('Installed Power (kWp)')
    ax2.set_title('Optimal Installed Power')
    plt.show()

    wh_battery = wh_battery / 1000  # Convert to kWh if needed
    fig, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(tot_conso, wh_battery, label='Battery Capacity (kWh)', color='red', marker='o')
    ax3.set_xlabel('Total Consumption (MWh/year)')
    ax3.set_ylabel('Battery Capacity (kWh)')
    ax3.set_title('Optimal Battery Capacity')
    plt.show()
    
    fig, ax4 = plt.subplots(figsize=(10, 6))
    ax4.plot(tot_conso, objective, label='Total gain(eur/year)', color='purple', marker='o')
    ax4.set_xlabel('Total Consumption (MWh/year)')
    ax4.set_ylabel('Total gain (eur/year)')
    ax4.set_title('Total Gain of the community')
    plt.show()
    
    fig, ax5 = plt.subplots(figsize=(10, 6))
    ax5.plot(tot_conso, objective/tot_conso, label='Total gain per MWh (eur/MWh)', color='brown', marker='o')
    ax5.set_xlabel('Total Consumption (MWh/year)')
    ax5.set_ylabel('Total gain per MWh (eur/MWh)')
    plt.show()
func_1()

def func_2():
    file_1 = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/first_simu/resultats_simulations.csv"
    file_2 = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/first_simu/resultats_simulations_bis.csv"

    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)
    
    # On garde dans df1 uniquement les lignes dont n_households n'est pas dans df2
    df1_clean = df1[~df1['n_households'].isin(df2['n_households'])]

    # On concatène les lignes corrigées de df2
    df_merged = pd.concat([df1_clean, df2], ignore_index=True)

    # (Optionnel) On trie par n_households si tu veux
    df_merged = df_merged.sort_values('n_households').reset_index(drop=True)
    
    print(df_merged)

    df_merged.to_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/first_simu/resultats_simulations_merged.csv", index=False)

#func_2()
