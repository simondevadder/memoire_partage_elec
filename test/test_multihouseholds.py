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
from multihouseholds import MultiHouseholds


def test_define_wh_begin_fixed():
    params = {
        'n_households': 100,
        'input_dir': 'brussels',
        'output_dir': 'test_multi',
        'wh_intelligence_param' : [True] * 100,
        
    }
    test_multi = MultiHouseholds(params)
    wh_on = np.zeros(24)
    for i in range(100):
        ind = test_multi.households.array[i].wh_hours_begin 
        wh_on[ind] += 1
        wh_on[ind+1] += 1
    
    plt.plot(wh_on, label="Wh on")
    plt.show()
    
test_define_wh_begin_fixed

def test_define_wh_begin_perfect_knowledge():
    pass
# test_define_wh_begin_perfect_knowledge