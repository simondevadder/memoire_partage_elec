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
    'output_directory': 'Output_test',
}

def test_cooking_this_day():
    household = Household(params)
    for i in range(365):
        household.cooking_this_day()
        household.day +=1 
    
    #plt.plot(household.consumption[0:192])
    #plt.show()
    
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
        
    
test_cooking_this_day()
