"""
Master Thesis :  simulation of an energy community
Master Student: Simon De Vadder
 This file is used to test the functions in the file 'energy_community.py'
"""

import numpy as np
import pandas as pd
from datetime import date
import sys
import os
from matplotlib import pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from energy_community import EnergyCommunity
from household import Household

params = {
    'input_directory': 'brussels',
    'output_directory': 'test_directory_brussels',
    "PEB" : "A",
    "heating_type" : "only-electric",
}

def test_load_temperature():
    params["T_ext_threshold"] = 12
    params["appartment_area"] = 100
    params["heating_efficiency"] = 2.3
    
    household = Household(params)
    #print(household.temperature_array[1][0])
    thershold_day = np.ones(365*24)*12
    thershold_night = np.ones(365*24)*7
    days = np.linspace(0, 365, 365*24)
    plt.plot(days, household.temperature_array[:,0], label="Température extérieure (2017)")
    plt.plot(days, thershold_day, label="Température limite jour")
    plt.plot(days, thershold_night, label="Température limite nuit")
    plt.xlabel("Jours")
    plt.ylabel("Température (°C)")
    plt.legend()
    plt.show()
    print("power : ", household.annual_heating_value_m2)
    household.load_temperature_data()
    for i in range(365):
        household.electric_heating()
        household.day +=1
    first_year = np.zeros(192)
    for i in range(192):
        first_year[i] = household.load_heating[192+i][0]
    hours = np.linspace(0, 48, 48*4)
    #sns.lineplot(x=hours, y=first_year)
   # plt.show()
    
    heating = np.zeros(365)
    for i in range(365):
        heating[i] = np.sum(household.load_heating[i*96:(i+1)*96, 0])/4000
    day = np.linspace(0, 365, 365)
    sns.lineplot(x=day, y=heating)
    plt.xlabel("Jours")
    plt.ylabel("Energie (kWh)")
    plt.show()
    
    time_on = np.zeros(365*24*4)
    for i in range(35040):
        if household.load_heating[i][0] > 0:
            time_on[i] = 1
    on_per_day = np.zeros(365)
    for i in range(365):
        on_per_day[i] = np.sum(time_on[i*96:(i+1)*96])
    plt.plot(on_per_day)
    plt.show()
    on = np.sum(household.load_heating, axis=0)/(4000 * household.flat_area)
    is_on = np.zeros(3)
    for i in range(len(household.load_heating[0])):
        for j in range(len(household.load_heating)):
            if household.load_heating[j][i] > 0:
                is_on[i] += 1
       
    
    print(on)
    print(is_on)
    
#test_load_temperature()
    
def test_cooking_this_day():
    params["cooking activity"]  = "medium"
    household = Household(params)
    print(household.total_conso_cooking)
    for i in range(365):
        household.cooking_this_day()
        household.day +=1 
    time = np.linspace(0, 48, 48*4)
    sns.lineplot(x=time, y=household.consumption[0:192])
    plt.xlabel("Hours")
    plt.ylabel("power (W)")
    plt.show()
    
    per_15min = np.zeros(96)
    for i in range(365):
        per_15min += household.consumption[96*i:96*(i+1)]
    per_15min = per_15min/365
    hours = np.linspace(0, 24, 24*4)
    sns.lineplot(x=hours, y=per_15min)
    plt.xlabel("hours")
    plt.ylabel("Mean power (W)")
    plt.show()
    
    total = 0
    for i in range(len(household.consumption)):
        total += household.consumption[i]/4
    print(total/1000)
        
    
#test_cooking_this_day()

def test_electric_water_heater():
    params['wh_usage'] = 'medium'
    params['wh_type'] = 'Joules'
    params['wh_night'] = False
    household = Household(params)
    for i in range(365):
        household.electric_water_heater()
        household.day +=1
    
    plt.plot(household.consumption[0:192])
    plt.show()
    
    per_15min = np.zeros(96)
    for i in range(365):
        per_15min += household.consumption[96*i:96*(i+1)]
    per_15min = per_15min/365
    plt.plot(per_15min)
    plt.show()
    
    total = 0
    for i in range(len(household.consumption)):
        total += household.consumption[i]/4
    print(total/1000)
#test_electric_water_heater()
  
def test_wh_2():
    n_low = 20
    n_medium = 20
    n_high = 20
    n_thermo = 20
    
    conso_low = np.zeros(n_low)
    conso_medium = np.zeros(n_medium)
    conso_high = np.zeros(n_high)
    conso_thermo = np.zeros(n_thermo)
    
    for i in range(n_low):
        params['wh_usage'] = 'low'
        params['wh_type'] = 'Joules'
        household = Household(params)
        for j in range(365):
            household.electric_water_heater()
            household.day +=1
        conso_low[i] = np.sum(household.consumption)/4000
        
    for i in range(n_medium):
        params['wh_usage'] = 'medium'
        params['wh_type'] = 'Joules'
        household = Household(params)
        for j in range(365):
            household.electric_water_heater()
            household.day +=1
        conso_medium[i] = np.sum(household.consumption)/4000
        
    for i in range(n_high):
        params['wh_usage'] = 'high'
        params['wh_type'] = 'Joules'
        household = Household(params)
        for j in range(365):
            household.electric_water_heater()
            household.day +=1
        conso_high[i] = np.sum(household.consumption)/4000
    
    for i in range(n_thermo):
        params['wh_type'] = 'thermodynamic'
        household = Household(params)
        for j in range(365):
            household.electric_water_heater()
            household.day +=1
        conso_thermo[i] = np.sum(household.consumption)/4000
        
    # Noms des tableaux pour la légende
    labels = ['Low', 'Medium', 'High', 'Thermodynamic']

    # Combiner les données pour trier
    data = np.concatenate([conso_low, conso_medium, conso_high, conso_thermo])
    colors = ['skyblue'] * len(conso_low) + ['yellow'] * len(conso_medium) + ['red'] * len(conso_high) + ['green'] * len(conso_thermo)

    # Trier par ordre décroissant
    sorted_indices = np.argsort(data)[::-1]
    sorted_data = data[sorted_indices]
    sorted_colors = np.array(colors)[sorted_indices]

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    sns.barplot(x=np.arange(len(sorted_data)), y=sorted_data, palette=sorted_colors)

    # Ajouter les légendes et ajuster le graphique
    #plt.title('Bar Plot des valeurs triées', fontsize=16)
    #plt.xlabel('', fontsize=14)
    plt.ylabel('Annual consumption [kWh]', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.xticks([])  # Supprimer les ticks et étiquettes sur l'axe des x
    plt.legend(handles=[
        plt.Line2D([0], [0], color='skyblue', lw=4, label='Low'),
        plt.Line2D([0], [0], color='yellow', lw=4, label='Medium'),
        plt.Line2D([0], [0], color='red', lw=4, label='High'),
        plt.Line2D([0], [0], color='green', lw=4, label='Thermodynamic'),
    ], loc='upper right')

    # Afficher le graphique
    plt.tight_layout()
    plt.show()

test_wh_2()
        
def test_cold_source():
    params['number_cold_sources'] = 2
    household = Household(params)
    for i in range(365):
        household.cold_sources()
        household.day +=1
    
    plt.plot(household.consumption)
    plt.show()
    
    per_15min = np.zeros(96)
    for i in range(365):
        per_15min += household.consumption[96*i:96*(i+1)]
    per_15min = per_15min/365
    plt.plot(per_15min)
    plt.show()
    
    total = 0
    for i in range(len(household.consumption)):
        total += household.consumption[i]/4
    print(total/1000)      

#test_cold_source()

def test_washing_utilities():
    params['have_washing_machine'] = False
    params['washing_frequency']= 'low'
    params['washing_itelligence']=False
    params['have_dishwasher'] = True
    params['dishwasher_frequency']= 'high'
    params['dishwasher_intelligence']=False
    params['have_dryer']= False
    params['dryer_usage']= 'high'
    params['dryer_intelligence']=False
    params['dryer_type']= 'condensation'
    
    household = Household(params)
    for i in range(52):
        household.washing_utilities()
        household.day +=7
    
    plt.plot(household.consumption[0:672])
    plt.show()
    
    total = 0
    for i in range(len(household.consumption)):
        total += household.consumption[i]/4
    print(total/1000)
#test_washing_utilities()

    
def test_total_conso():
    params['wh_capacity'] = 'medium'
    params['wh_type'] = 'Joules'
    params['wh_night'] = True
    params['number_cold_sources'] = 2
    params['have_washing_machine'] = True
    params['washing_frequency']= 'medium'
    params['washing_itelligence']=False
    params['have_dishwasher'] = True
    params['dishwasher_frequency']= 'high'
    params['dishwasher_intelligence']=False
    params['have_dryer']= True
    params['dryer_usage']= 'low'
    params['dryer_intelligence']=False
    params['dryer_type']= 'condensation'
    household = Household(params)
    household.launch_year()
    args = {
        "day" : 15,
        "month" :  6,
        "week" : 15,
        "from_day" : 257,
        "to_day" : 263,
    }
    #household.plot_consumption(args, plot_day=True, plot_week=True, plot_to_from=True, plot_whole_year=True)
    
    plt.plot(household.total_consumption[0:672])
    plt.show()
#test_total_conso()