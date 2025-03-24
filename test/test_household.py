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
    "PEB" : "D",
    "heating_type" : "only-electric",
}

def test_load_temperature():
    params["T_ext_threshold"] = 12
    household = Household(params)
    print("power : ", household.annual_heating_value_m2)
    household.load_temperature_data()
    for i in range(365):
        household.electric_heating()
        household.day +=1
    first_year = np.zeros(192)
    for i in range(192):
        first_year[i] = household.load_heating[i][0]
    plt.plot(first_year)
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
    
    plt.plot(household.consumption[0:672])
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
        
    
test_cooking_this_day()

def test_electric_water_heater():
    params['wh_capacity'] = 'medium'
    params['wh_type'] = 'thermodynamic'
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