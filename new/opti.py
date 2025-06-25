### gurobi optimisation file for electricity sharing in a building


from pyomo.environ import *
import json
import sys
import numpy as np
from pyomo.opt import SolverFactory


def first():
    gurobi = SolverFactory('gurobi')
    m = ConcreteModel()
    
    load_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/1_households_1_years.csv"
    production_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/production_profile.csv"
    n_households = 1
    dt = 0.25
    n_timestep = 35040
    m.time = RangeSet(0,35040-1)  # 35040 timesteps for one year with 15 minutes intervals
    m.households = RangeSet(0, n_households - 1)  # 1 household

    #########################
    #VARIABLES
    #########################
    
    m.pv_area = Var(within=NonNegativeReals)
    m.wh_battery = Var(within=NonNegativeReals)
    m.w_battery = Var(within=NonNegativeReals)
    m.p = Var(m.households, m.time, within=NonNegativeReals)
    m.p_bat = Var( m.time)
    m.soc = Var(m.time, within=NonNegativeReals)
    
    
    #########################
    #PARAMETERS
    #########################
    
    
    
    #########################
    #OBJECTIVE
    #########################
    
    def objective_rule(m):
        return 0
    m.objective = Objective(rule=objective_rule, sense=maximize)
    
    #########################
    #CONSTRAINTS
    #########################
    
    