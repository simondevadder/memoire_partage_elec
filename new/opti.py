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
    load_profile = np.loadtxt(load_profile_file, delimiter=',')
    production_profile = np.loadtxt(production_profile_file, delimiter=',')
    n_households = load_profile.shape[0]  # à vérifier si pas 1
    dt = 0.25
    n_timestep = load_profile.shape[1]
    m.time = RangeSet(0,n_timestep-1)  # 35040 timesteps for one year with 15 minutes intervals
    m.households = RangeSet(0, n_households - 1)  # 1 household

    #########################
    #VARIABLES
    #########################
    
    m.pv_area = Var(within=NonNegativeReals)
    m.wh_battery = Var(within=NonNegativeReals)
    m.w_battery = Var(within=NonNegativeReals)
    m.p = Var(m.households, m.time, within=NonNegativeReals)
    m.p_bat = Var( m.time)
    m.p_inj = Var(m.time, within=NonNegativeReals)
    m.soc = Var(m.time, within=NonNegativeReals)
    m.p_pv = Var(m.time, within=NonNegativeReals)
    
    
    #########################
    #PARAMETERS
    #########################
    m.p_bat_max = Param(initialize=1000)  # Maximum power of the battery in W, to change as a ffunction to the capacity
    
    
    
    #########################
    #OBJECTIVE
    #########################
    
    def objective_rule(m):
        return 0
    m.objective = Objective(rule=objective_rule, sense=maximize)
    
    #########################
    #CONSTRAINTS
    #########################
    
    def power_to_household(m, t, h):
        return m.p[h, t] <= load_profile[h, t]
    m.power_to_household = Constraint(m.households, m.time, rule=power_to_household)
    
    def power_from_pv(m, t):
        return m.p_pv[t] == production_profile[t] * m.pv_area
    m.power_from_pv = Constraint(m.time, rule=power_from_pv)
    
    def power_to_battery_pos(m, t):
        return m.p_bat[t] <= m.p_bat_max
    m.power_to_battery_pos = Constraint(m.time, rule=power_to_battery_pos)
    
    def power_to_battery_neg(m, t):
        return m.p_bat[t] >= -m.p_bat_max
    m.power_to_battery_neg = Constraint(m.time, rule=power_to_battery_neg)
    
    def power_equality(m,t):
        return  m.p_inj[t] + m.p_bat[t] + sum(m.p[h, t] for h in m.households) == m.p_pv[t]
    m.power_equality = Constraint(m.time, rule=power_equality)