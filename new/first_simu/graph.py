# file to draw graph from gurobi results

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def func_1():
    file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/unconst_correct_data/resultats_simulations_unconst_capex_03_merged.csv"
    file_2 = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/unconst_correct_otherdata/resultats_simulations_unconst_capex_03_otherdata_merged.csv"
    df = pd.read_csv(file)
    df_2 = pd.read_csv(file_2)
    # print(df)
    
    n_households = df["n_households"].to_numpy()
    objective = df["objective"].to_numpy()
    kWc = df["kWc"].to_numpy()
    wh_battery = df["wh_battery"].to_numpy()
    puissance_totale = df["puissance_totale"].to_numpy()
    puissance_produite = df["puissance_produite"].to_numpy()
    tot_conso = df["tot_conso"].to_numpy()
    tot_cost_without = df["total_cost_without "].to_numpy()
    tot_cost_with = tot_cost_without - objective
    
    n_households_2 = df_2["n_households"].to_numpy()
    objective_2 = df_2["objective"].to_numpy()
    kWc_2 = df_2["kWc"].to_numpy()
    # random_factors = np.random.uniform(0.9, 0.95, size=len(df_2))
    # df_2['wh_battery'] = df_2['wh_battery'] * random_factors
    wh_battery_2 = df_2["wh_battery"].to_numpy()
    puissance_totale_2 = df_2["puissance_totale"].to_numpy()
    puissance_produite_2 = df_2["puissance_produite"].to_numpy()
    tot_conso_2 = df_2["tot_conso"].to_numpy()
    tot_cost_without_2 = df_2["total_cost_without "].to_numpy()
    tot_cost_with_2 = tot_cost_without_2 - objective_2
    


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
    
    self_suffi_2 = puissance_totale_2 / tot_conso_2 * 100
    self_conso_2 = puissance_totale_2 / puissance_produite_2 * 100

    # print("self_suffi:", self_suffi)
    # print("self_conso:", self_conso)
    
    tot_conso = tot_conso / 1000000  # Convert to MWh if needed
    puissance_totale = puissance_totale / 1000000  # Convert to MWh if needed
    puissance_produite = puissance_produite / 1000000  # Convert to MWh if needed
    
    tot_conso_2 = tot_conso_2 / 1000000  # Convert to MWh if needed
    puissance_totale_2 = puissance_totale_2 / 1000000  #
    puissance_produite_2 = puissance_produite_2 / 1000000  # Convert to MWh if needed
    
    lcoe_with = tot_cost_with / tot_conso  # LCOE with battery en eur/MWh
    lcoe_without = tot_cost_without / tot_conso  # LCOE without battery  en eur/MWh
    
    lcoe_with_2 = tot_cost_with_2 / tot_conso_2  # LCOE with battery en eur/MWh
    lcoe_without_2 = tot_cost_without_2 / tot_conso_2
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(tot_conso, self_suffi, label='Self-Sufficiency for data set 1 (%)', color='green', marker='o')
    ax1.plot(tot_conso, self_conso, label='Self-Consumption for data set 1 (%)', color='red', marker='o')
    ax1.plot(tot_conso_2, self_suffi_2, label='Self-Sufficiency for data set 2 (%)', color='blue', marker='x')
    ax1.plot(tot_conso_2, self_conso_2, label='Self-Consumption for data set 2 (%)', color='orange', marker='x')
    ax1.set_xlabel('Total Consumption (MWh/year)')
    ax1.set_ylabel('Percentage (%)')
    ax1.set_ylim(0, 100)
    ax1.set_title('Self-Sufficiency and Self-Consumption')
    ax1.legend()
    plt.show()
    
    fig, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(tot_conso, kWc/tot_conso, label='kWp/MWh', color='green', marker='o')
    ax2.set_xlabel('Total Consumption (MWh/year)')
    ax2.set_ylabel('Optimal Installed Power per MWh (kWp/MWh)')
    ax2.set_ylim(0, 7)
    #ax2.set_title('Optimal Installed Power')
    plt.show()

    wh_battery = wh_battery / 1000  # Convert to kWh if needed
    wh_battery_2 = wh_battery_2 / 1000  # Convert to kWh if needed
    fig, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(tot_conso, wh_battery/tot_conso, label='Battery Capacity (kWh)', color='red', marker='o')
    ax3.set_xlabel('Total Consumption (MWh/year)')
    ax3.set_ylabel('Optimal Battery Capacity per MWh (kWh/MWh)')
    ax3.set_ylim(0, 7)
    #ax3.set_title('Optimal Battery Capacity')
    plt.show()
    
    # print("orange", wh_battery_2/tot_conso_2)
    fig, ax7 = plt.subplots(figsize=(10, 6))
    ax7.plot(tot_conso, kWc/tot_conso, label='Optimal Installed Power for data set 1 (kWp/MWh)', color='green', marker='o')
    ax7.plot(tot_conso, wh_battery/tot_conso, label='Optimal Battery Capacity for data set 1 (kWh/MWh)', color='red', marker='o')
    ax7.plot(tot_conso_2, kWc_2/tot_conso_2, label='Optimal Installed Power for data set 2 (kWp/MWh)', color='blue', marker='x')
    ax7.plot(tot_conso_2, wh_battery_2/tot_conso_2, label='Optimal Battery Capacity for data set 2 (kWh/MWh)', color='orange', marker='x')
    ax7.set_xlabel('Total Consumption (MWh/year)')
    ax7.set_ylabel('kWp/MWh or kWh/MWh')
    ax7.set_ylim(0, 4)
    ax7.set_title('Optimal Installed Power and Battery Capacity')
    ax7.legend()
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
    ax5.set_title('Total Gain per MWh of the community')
    plt.show()
    
    fig, ax6 = plt.subplots(figsize=(10, 6))
    ax6.plot(tot_conso, lcoe_with, label='Electricity cost with PV and electricity sharing for data set 1 (eur/MWh)', color='blue', marker='o')
    ax6.plot(tot_conso, lcoe_without, label='Base electricity cost for data set 1 (eur/MWh)', color='red', marker='o')
    ax6.plot(tot_conso_2, lcoe_with_2, label='Electricity cost with PV and electricity sharing for data set 2 (eur/MWh)', color='green', marker='x')
    ax6.plot(tot_conso_2, lcoe_without_2, label='Base electricity cost for data set 2 (eur/MWh)', color='orange', marker='x')
    ax6.set_xlabel('Total Consumption (MWh/year)')
    ax6.set_ylabel('Electricity cost (eur/MWh)')
    ax6.set_ylim(0, 400)
    ax6.legend()
    ax6.set_title('Electricity Cost Comparison')
    plt.show()
#func_1()

def func_2():
    file_1 = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/unconst_correct_otherdata/resultats_simulations_unconst_capex_03_otherdata.csv"
    file_2 = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/unconst_correct_otherdata/resultats_simulations_unconst_capex_03_otherdata_2.csv"

    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)
    
    # On garde dans df1 uniquement les lignes dont n_households n'est pas dans df2
    df1_clean = df1[~df1['n_households'].isin(df2['n_households'])]

    # On concatène les lignes corrigées de df2
    df_merged = pd.concat([df1_clean, df2], ignore_index=True)

    # (Optionnel) On trie par n_households si tu veux
    df_merged = df_merged.sort_values('n_households').reset_index(drop=True)
    
    print(df_merged)

    df_merged.to_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/unconst_correct_otherdata/resultats_simulations_unconst_capex_03_otherdata_merged.csv", index=False)

#func_2()

def twenty_households_pv_area():
    file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/twenty_households_pv_correct/resultats_twenty_households_correct_2.csv"
    df = pd.read_csv(file)
    # print(df)
    
    max_area = df["max_area"].to_numpy()
    n_households = df["n_households"].to_numpy()
    objective = df["objective"].to_numpy()
    kWc = df["kWc"].to_numpy()
    wh_battery = df["wh_battery"].to_numpy()
    puissance_totale = df["puissance_totale"].to_numpy()
    puissance_produite = df["puissance_produite"].to_numpy()
    tot_conso = df["tot_conso"].to_numpy()
    tot_cost_without = df["total_cost_without"].to_numpy()
    tot_cost_with = tot_cost_without - objective
    self_suffi = puissance_totale / tot_conso * 100
    self_conso = puissance_totale / puissance_produite * 100
    
    # print("self_suffi:", self_suffi)
    # print("self_conso:", self_conso)
    
    tot_conso = tot_conso / 1000000  # Convert to MWh if needed
    puissance_totale = puissance_totale / 1000000  # Convert to MWh if needed
    puissance_produite = puissance_produite / 1000000  # Convert to MWh if needed
    
   
    lcoe_with = tot_cost_with / tot_conso  # LCOE with battery en eur/MWh
    lcoe_without = tot_cost_without / tot_conso  # LCOE without battery  en eur/MWh
    wh_battery = wh_battery / 1000  # Convert to kWh if needed
    
    max_kwc = max_area * 0.182
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(max_kwc, self_suffi, label='Self-Sufficiency (%)', color='blue', marker='o')
    ax1.plot(max_kwc, self_conso, label='Self-Consumption (%)', color='red', marker='o')
    ax1.set_xlabel('Maximum PV peak power (kWp)')
    ax1.set_ylabel('Percentage (%)')
    ax1.legend()
    ax1.set_title('Self-Sufficiency and Self-Consumption')
    plt.show()
    
    fig, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(max_kwc, wh_battery/tot_conso, label='kWh/MWh', color='red', marker='o')
    ax2.set_xlabel('Maximum PV peak power (kWp)')
    ax2.set_ylabel('Optimal Battery Capacity per MWh (kWh/MWh)')
    ax2.set_ylim(0, 1)
    ax2.set_title('Optimal Battery Capacity')
    plt.show()
    
    fig, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(max_kwc, lcoe_with, label='Electricity cost with PV and electricity sharing (eur/MWh)', color='orange', marker='o')
    ax3.plot(max_kwc, lcoe_without, label='Base electricity cost (eur/MWh)', color='blue', marker='o')
    ax3.set_xlabel('Maximum PV peak power (kWp)')
    ax3.set_ylabel('Electricity cost (eur/MWh)')
    ax3.set_title('Electricity cost comparison')
    ax3.set_ylim(0, 400)
    plt.show()
    
#twenty_households_pv_area()

def twenty_households_heat_map_bat_capex():
    df = pd.read_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/capex_range_correct/resultats_capex_battery_merged_3.csv")
    df["wh_battery"] = 1000*df["wh_battery"] /  df["tot_conso"]  # Convert to kWh and multiply by total consumption

    df["kWc"] = df["kWc"] *1000000 / df["tot_conso"]  # Convert to kWp/MWh
    df["capex_battery"] = (df["capex_battery"] * 1000).round(1)  # Convert to euros
    # Pivot pour obtenir une matrice (tableau 2D) pour la heatmap
    heatmap_data = df.pivot(index="injection_price", columns="capex_battery", values="wh_battery")

    # Trie les axes pour un affichage correct
    heatmap_data = heatmap_data.sort_index().sort_index(axis=1)
    
    heatmap_data = heatmap_data.iloc[::-1]
    
    heat_map_data_kwc = df.pivot(index="injection_price", columns="capex_battery", values="kWc")
    heat_map_data_kwc = heat_map_data_kwc.sort_index().sort_index(axis=1)
    heat_map_data_kwc = heat_map_data_kwc.iloc[::-1]

    df["lcoe_with"] = (df["total_cost_without"] - df["objective"]) / df["tot_conso"]  # LCOE with battery en eur/MWh
    df["lcoe_with"] = df["lcoe_with"] * 1000000  # Convert to MWh if needed
    heatmap_data_lcoe = df.pivot(index="injection_price", columns="capex_battery", values="lcoe_with")
    heatmap_data_lcoe = heatmap_data_lcoe.sort_index().sort_index(axis=1)
    heatmap_data_lcoe = heatmap_data_lcoe.iloc[::-1]
    heatmap_data_lcoe_filtered = heatmap_data_lcoe[heatmap_data_lcoe.index <= 0.05]


    # Affiche la heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd")
    plt.xlabel("Battery Capex (euros/kWh)")
    plt.ylabel("Injection price (euros/kWh)")
    plt.yticks(rotation=0) 
    plt.title("Battery capacity (kWh/MWh)")
    plt.show()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(heat_map_data_kwc, annot=True, fmt=".1f", cmap="YlOrRd")
    plt.xlabel("Battery Capex (euros/kWh)")
    plt.ylabel("Injection price (euros/kWh)")
    plt.yticks(rotation=0) 
    plt.title("Optimal Installed Power (kWp/MWh)")
    plt.show()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data_lcoe_filtered, annot=True, fmt=".1f", cmap="YlOrRd")
    plt.xlabel("Battery Capex (euros/kWh)")
    plt.ylabel("Injection price (euros/kWh)")
    plt.yticks(rotation=0) 
    plt.title("Electricity cost (eur/MWh)")
    plt.show()
    
    
twenty_households_heat_map_bat_capex()

def merging_capex():
    # Charge les deux fichiers
    df1 = pd.read_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/capex_range_correct/resultats_capex_battery_merged_2.csv")
    df2 = pd.read_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/capex_range_correct/resultats_capex_battery_correct_4.csv")

    # Fusionne sur capex_battery et injection_price, en gardant les lignes de df1 qui ne sont PAS dans df2
    mask = ~df1.set_index(['capex_battery', 'injection_price']).index.isin(
        df2.set_index(['capex_battery', 'injection_price']).index
    )
    df1_clean = df1[mask]

    # Concatène les lignes corrigées de df2 (qui remplacent celles de df1)
    df_merged = pd.concat([df1_clean, df2], ignore_index=True)

    # Trie si besoin
    df_merged = df_merged.sort_values(['capex_battery', 'injection_price']).reset_index(drop=True)

    # Sauvegarde le résultat
    df_merged.to_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/capex_range_correct/resultats_capex_battery_merged_3.csv", index=False)

#merging_capex()

def plot_load_profiles():
    file_data = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/48_households_0_years.csv"
    file_other_data = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/combined_household_power_consumption_48_2.csv"

    df = pd.read_csv(file_data)
    df_other = pd.read_csv(file_other_data)

    # Moyenne sur tous les foyers (colonnes)
    profile_1 = df.mean(axis=1).to_numpy()
    profile_2 = df_other.mean(axis=1).to_numpy()

    n_steps_per_day = 24 * 4  # 15 min time step
    n_days = len(profile_1) // n_steps_per_day

    # Reshape et calcule la moyenne pour chaque time step sur l'année
    daily_matrix_1 = profile_1[:n_days * n_steps_per_day].reshape(n_days, n_steps_per_day)
    daily_matrix_2 = profile_2[:n_days * n_steps_per_day].reshape(n_days, n_steps_per_day)

    mean_profile_1 = daily_matrix_1.mean(axis=0)
    mean_profile_2 = daily_matrix_2.mean(axis=0)

    hours = np.arange(0, 24, 0.25)  # 0h à 23h45

    plt.figure(figsize=(14, 6))
    plt.plot(hours, mean_profile_1, label='Fichier 1 - Moyenne tous foyers')
    plt.plot(hours, mean_profile_2, label='Fichier 2 - Moyenne tous foyers')
    plt.xlabel('Hour of day')
    plt.ylabel('Mean Power (Wh)')
    plt.title('Mean Daily Load Profile (All Households)')
    plt.legend()
    plt.xticks(np.arange(0, 25, 2))
    plt.grid(True)
    plt.show()

    
#plot_load_profiles()