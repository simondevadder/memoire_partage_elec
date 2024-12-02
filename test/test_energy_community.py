"""

Master Thesis :  simulation of an energy community
Master Student: Simon De Vadder
 This file is used to test the functions in the file 'energy_community.py'
"""

import numpy as np

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from energy_community import EnergyCommunity


def test_init():
    params = {'n_households': 3, 'key': 'fix1round'}
    community= EnergyCommunity(params)
    community.consumption = np.array([5, 2, 1])
    community.production = 10
    
    
    

#test_init()
    
def test_repartition():
    
    
    keys = ["fix1round", "fixmultiround", "prorata", "hybrid"]
    for key in keys :
        params = {'n_households': 3, 'key': key}
        community = EnergyCommunity(params)
        community.consumption = np.array([5, 2, 7])
    
        community.production = 10
        repartition, taken_to_grid, injected_to_grid = community.func_repartition(community.consumption, community.production)
        print(key, repartition, taken_to_grid, injected_to_grid, community.consumption)

test_repartition()    

