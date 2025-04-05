#### master thesis, Simon De Vadder, electricity sharing in multi-units buildings
## test file for mutlihouseholds.py

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
from multihousehold import MultiHousehold


def test_define_wh_begin_fixed():
    params = {
        'n_households': 5,
        'input_directory': 'brussels',
        'output_directory': 'test_multi',
        'wh_intelligence_param' : [True] * 5,
        'PEB_params' : ["A"] * 5
        
    }
    test_multi = MultiHousehold(params,None)
    wh_on = np.zeros(24)
    for i in range(5):
        ind = int(test_multi.households_array[i].wh_hours_begin)
        wh_on[ind] += 1
        wh_on[ind+1] += 1
    
    plt.plot(wh_on, label="Wh on")
    plt.show()
    
#test_define_wh_begin_fixed()

def test_define_wh_begin_perfect_knowledge():
    params = {
        'n_households': 100,
        'input_directory': 'brussels',
        'output_directory': 'test_multi',
        'wh_intelligence_param' : [True] * 100,
        'PEB_params' : ["A"] * 100,
        'wh_hours_mode' : "perfect_knowledge" 
    }
    params_ener = {
        'n_years':3,
        'directory_data': 'brussels',
        'weather_file_name':'brussels_50.8444_4.35609_msg-iodc_60_',
        'directory_output': 'pv_out',
        'begin_year':2017,
        'end_year':2019,
        'n_households': 3,
        'key': 'fix1round',
        'PV_inclination': [20],
        'PV_orientation': [180],
        'PV_module_size':[1.99, 0.991, 0.075],
        'PV_area': [1],
        'PV_efficiency': 0.15,
        'sharing_price': 0.1,
        'grid_price': 0.2,
        'grid_injection_price': 0.05,
        'n_elevators': 1,
        'elevator_consumption': 20,
        'n_floor': 5,
        'common_area': 10,
        'electric_heating': False,   
    }
    enercom = EnergyCommunity(params_ener)
    enercom.func_compute_total_production()
    test_multi = MultiHousehold(params,enercom)
    
    to_print_2017 = test_multi.wh_hours_begin_all[:,:,0]
    prod_2017 = enercom.total_production[:,0]
    
    day = 111
    prod_to_print = prod_2017[day*24:day*24+24]
    wh_on = np.zeros(24)
    for i in range(100):
        ind = int(to_print_2017[i, day])
        wh_on[ind] += 1
        wh_on[ind+1] += 1
        
    plt.plot(prod_to_print, label="Production")
    plt.plot(wh_on, label="Wh on")
    plt.legend()
    plt.show()
    
    
test_define_wh_begin_perfect_knowledge()