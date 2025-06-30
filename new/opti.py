### gurobi optimisation file for electricity sharing in a building


from pyomo.environ import *
import json
import sys
import numpy as np
from pyomo.opt import SolverFactory
import pandas as pd


def first():
    gurobi = SolverFactory('gurobi')
    m = ConcreteModel()
    
    load_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/24_households_1_years.csv"
    production_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/production_profile.csv"
    load_profile = pd.read_csv(load_profile_file, header=None )
    load_profile = load_profile.to_numpy()  # Convert to numpy array for easier manipulation
    df = pd.read_csv(production_profile_file, header=None, dtype=str)

    # Séparer chaque string en 3 colonnes
    production_profile = df[0].str.split(expand=True).astype(float).to_numpy()
    production_profile = np.repeat(production_profile, 4, axis=0)
    #print("production_profile shape:", np.sum(production_profile[:,:]))

    # production_profile aura la forme (8760, 3) avec des floats

  # Affiche les 3 valeurs de la première ligne sous forme de floats
    n_households = load_profile.shape[1]  # à vérifier si pas 1
    dt = 0.25
    n_timestep = load_profile.shape[0]
    m.time = RangeSet(0,n_timestep-1)  # 35040 timesteps for one year with 15 minutes intervals
    m.households = RangeSet(0, n_households - 1)  # 1 household
    #print("Number of households:", n_households)
    #print("Number of timesteps:", n_timestep)
    #print("load_profile shape:", load_profile)


    #########################
    #VARIABLES
    #########################

    m.pv_area = Var(within=NonNegativeReals, bounds=(40, 2000), initialize=700)
    m.wh_battery = Var(within=NonNegativeReals, initialize=10000)
    #m.p_bat_max = Var(within=NonNegativeReals, initialize=2000)
    m.p = Var(m.households, m.time, within=NonNegativeReals, initialize=0)  # Power to each household in W
    m.p_bat_pos = Var(m.time, within=NonNegativeReals, initialize=0)
    m.p_bat_neg = Var(m.time, within=NonNegativeReals, initialize=0)  # Power to the battery in W
    m.p_inj = Var(m.time, within=NonNegativeReals, initialize=0)
    m.p_ev = Var(m.time, within=NonNegativeReals, initialize=0)  # Power to EV, not used in this model
    m.soc = Var(m.time, within=NonNegativeReals, initialize=0)  # State of charge of the battery in Wh, not used in this model
    m.p_pv = Var(m.time, within=NonNegativeReals, initialize=0)  # Power from PV in W, not used in this model
    m.kWc = Var(within=NonNegativeReals, initialize=127.4)
    m.cv_coeff = Var(within=NonNegativeReals, bounds=(0.0, 2.1), initialize=1)  # Coefficient for the piecewise function, bounds can be adjusted
    m.price_per_kwc = Var(within=NonNegativeReals, bounds=(0, 4000), initialize=1000)  # Price per kWc, bounds can be adjusted
    m.p_ev_max = Var(within=NonNegativeReals, initialize=74000)  # Maximum power of the battery in W, to change as a ffunction to the capacity

    #########################
    #PARAMETERS
    #########################
    
    m.eff_bat = Param(initialize=0.9)  # Efficiency of the battery
    m.p_bat_max = Param( initialize=1000)  # Maximum power of the battery in W, to change as a ffunction to the capacity
    m.annual_rate = Param(initialize=0.03)  # Annual rate for the PV costs
    m.lifetime = Param(initialize=25)  # Lifetime of the PV system in years
    year = 0
    breakpoints = [0, 5, 36, 100, 250, 10000] # for cv_coeff
    
    breakpoints_price = [0, 10, 50, 100, 10000]  # adapte la borne supérieure si besoin

    # Les coefficients (x, y) pour chaque intervalle
    # Pour chaque palier : price_per_kwc = x * kWc + y
    price_x = [-240, -3.75, -3, -0.66]
    price_y = [3700, 1337.5, 1300, 1066.6]
    
    
    
    #########################
    #OBJECTIVE
    #########################
    
    def time_is_night(t):
        #night is from 22 to 7 during the week and all weekend
        t_week = t%672 # 672 timesteps per week (7 days * 24 hours * 4 timesteps per hour)
        if t_week > 480 : 
            return True  # saturday or sunday
        else:
            t_day = t % 96
            if t_day < 28 or t_day >= 88:
                return True  # night time during the week
        return False


    def objective_rule(m):
        total_bill_reduction = 0
        total_from_injection = 0
        total_from_ev = 0
        price_day = 0.38
        price_night = 0.29
        price_injection = 0.04  # price for injection, not used in this model
        price_ev = 0.2
        #####################
        #Revenue
        #####################
        total_bill_reduction = sum(
        m.p[h, t] * (price_night if time_is_night(t) else price_day) * dt * 0.001
        for t in m.time for h in m.households
        )
        total_from_injection = sum(m.p_inj[t] * price_injection * dt * 0.001 for t in m.time)
        total_from_ev = sum(m.p_ev[t] * price_ev * dt * 0.001 for t in m.time)
            
        #print("total_bill_reduction:", total_bill_reduction)
        #print("total_from_injection:", total_from_injection)
        #print("total_from_ev:", total_from_ev)
            
        #################
        # CV
        ##################
        
        cv_revenue = sum(m.p_pv[t] for t in m.time) * m.cv_coeff * 65 * dt * 10 /(25 * 1000000)        #print("cv_revenue:", cv_revenue)
        #print("cv_revenue:", cv_revenue)
        ###############
        # PV Costs
        ###############
       
        pv_costs = m.kWc * m.price_per_kwc        #print("prix par kwc:", price_per_kwc)  
        #print("kWc:", kWc)
            
        #Annualized costs 
        pv_costs_annualized = pv_costs * (m.annual_rate / (1 - (1 + m.annual_rate) ** -m.lifetime))  # 25 years lifetime
        #print("pv_costs_annualized:", pv_costs_annualized)
        
        ###############
        #Battery Costs
        ###############
        battery_costs = m.wh_battery * 0.03  # assuming 300 €/kWh for the battery
        
        ###############
        #ev_costs
        ###############
        ev_costs = m.p_ev_max * 0.01  # to change
        
        total_revenue = total_bill_reduction + total_from_injection + total_from_ev + cv_revenue - pv_costs_annualized - battery_costs - ev_costs
        #print("total_revenue:", total_revenue)
        return total_revenue

       
    m.objective = Objective(rule=objective_rule, sense=maximize)
    
    #########################
    #CONSTRAINTS
    #########################
    
    def kwc_def_rule(m):   ## for cv_coeff
       return m.kWc == m.pv_area * 0.182
    m.kwc_def = Constraint(rule=kwc_def_rule)
    def cv_piecewise_rule(m, x):
        if x < 5:
            return 2.055
        elif x < 36:
            return 1.953
        elif x < 100:
            return 1.016
        elif x < 250:
            return 0.642
        else:
            return 0.58
        #return 0
    m.piecewise_cv = Piecewise(
    m.kWc, m.cv_coeff,
    pw_pts=breakpoints,
    f_rule=cv_piecewise_rule,
    pw_constr_type='EQ',
    pw_repn='SOS2'
    )
    
    def price_piecewise_rule(m,x):
        if x < 10:
            return -240 * x + 3700
        elif x < 50:
            return -3.75 * x + 1337.5
        elif x < 100:
            return -3 * x + 1300
        else:
            return -0.66 * x + 1066.6

    m.piecewise_price = Piecewise(
        m.kWc, m.price_per_kwc,
        pw_pts=breakpoints_price,
        f_rule=price_piecewise_rule,
        pw_constr_type='EQ',
        pw_repn='SOS2'
    )
    
    def power_to_household(m, h, t):
        return m.p[h, t] <= load_profile[t, h]
    m.power_to_household = Constraint(m.households, m.time, rule=power_to_household)
    
    def power_from_pv(m, t):
        return m.p_pv[t] == production_profile[t, year] * m.pv_area
    m.power_from_pv = Constraint(m.time, rule=power_from_pv)
    
    def power_to_battery_pos(m, t):
        return m.p_bat_pos[t] <= m.p_bat_max
    m.power_to_battery_pos = Constraint(m.time, rule=power_to_battery_pos)
    
    def power_to_battery_neg(m, t):
        return m.p_bat_neg[t] <= m.p_bat_max
    m.power_to_battery_neg = Constraint(m.time, rule=power_to_battery_neg)
    
    # def power_bat_limit(m):
    #     return m.p_bat_max <= m.wh_battery * 0.5
    # m.power_bat_limit = Constraint(rule=power_bat_limit)
    
    def power_equality(m,t):
        return  m.p_inj[t] + m.p_bat_pos[t] - m.p_bat_neg[t] + sum(m.p[h, t] for h in m.households) + m.p_ev[t] == m.p_pv[t]
    m.power_equality = Constraint(m.time, rule=power_equality)
    
    def soc_set(m,t):
        if t == 0:
            return m.soc[t] == 0.5 *m.wh_battery  # Initial state of charge at 50% of the battery capacity
        else:
            return m.soc[t] == m.soc[t-1] + dt * m.p_bat_pos[t-1] * m.eff_bat - dt * m.p_bat_neg[t-1] / m.eff_bat
    m.soc_set = Constraint(m.time, rule=soc_set)
    
    def soc_lower_limit(m, t):
        return m.soc[t] >= 0.2 * m.wh_battery  # Minimum state of charge at 20% of the battery capacity
    m.soc_lower_limit = Constraint(m.time, rule=soc_lower_limit)
    
    def soc_upper_limit(m, t):
        return m.soc[t] <= 0.9 * m.wh_battery  # Maximum state of charge at 90% of the battery capacity
    m.soc_upper_limit = Constraint(m.time, rule=soc_upper_limit)
    
    def pv_area_limit(m):
        return m.pv_area <= 1000
    #m.pv_area_limit = Constraint(rule=pv_area_limit)
    
    def wh_battery_limit(m):
        return m.wh_battery <= 100000
    #m.wh_battery_limit = Constraint(rule=wh_battery_limit)
    
    def p_ev_limit(m, t):
        return m.p_ev[t] <= m.p_ev_max
    m.p_ev_limit = Constraint(m.time, rule=p_ev_limit)
    
    
    gurobi.solve(m)
    puissance_totale = sum(value(m.p[h, t]) for h in m.households for t in m.time)*0.25
    print("Puissance totale distribuée aux ménages :", puissance_totale, "Wh")
    print("puissance injectée :", sum(value(m.p_inj[t]) for t in m.time)*.025, "Wh")
    print("puissance produite par le PV (p_pv) :", sum(value(m.p_pv[t])*0.25 for t in m.time))


     # Affichage des résultats principaux
    print("Objectif (revenu total) :", value(m.objective))
    print("Surface PV (pv_area) :", value(m.pv_area))
    print("Capacité batterie (wh_battery) :", value(m.wh_battery))
    print("Puissance batterie max (p_bat_max) :", value(m.p_bat_max))
    print("cv_coeff :", value(m.cv_coeff))
    print("price", value(m.price_per_kwc))  # Affichage du prix par kWc
    pv_costs = value(m.kWc) * value(m.price_per_kwc)  # Calcul du coût total du PV
    pv_costs_annualized = pv_costs * (m.annual_rate / (1 - (1 + m.annual_rate) ** -m.lifetime))  # 25 years lifetime
    print("pv costs", pv_costs_annualized)

    cv_revenue = sum(value(m.p_pv[t]) for t in m.time) * value(m.cv_coeff) * 65 * dt * 10 /(25 * 1000000)
    print("cv_revenue:", cv_revenue)
    price_day = 0.38
    price_night = 0.29
    price_injection = 0.04  # price for injection, not used in this model
    total_bill_reduction = sum(
        value(m.p[h, t]) * (price_night if time_is_night(t) else price_day) * dt * 0.001
        for t in m.time for h in m.households
        )
    print("total_bill_reduction:", total_bill_reduction)
    total_from_injection = sum(value(m.p_inj[t]) * price_injection * dt * 0.001 for t in m.time)
    print("total_from_injection:", total_from_injection)
    print("ev_max:", value(m.p_ev_max))
    

first()
