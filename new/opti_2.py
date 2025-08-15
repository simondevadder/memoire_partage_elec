### gurobi optimisation file for electricity sharing in a building


from pyomo.environ import *
import json
import sys
import numpy as np
from pyomo.opt import SolverFactory
import pandas as pd
import pandas as pd


def first( load_profile_file=None, production_profile_file=None, capex_battery=0.3, injection_price=0.04, n_households=None, max_area=None, min_area=None):
    gurobi = SolverFactory('gurobi')
    m = ConcreteModel()
    
    # load_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/24_households_1_years.csv"
    # production_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/production_profile.csv"
    load_profile = pd.read_csv(load_profile_file, header=None )
    load_profile = load_profile.to_numpy()  # Convert to numpy array for easier manipulation
    df = pd.read_csv(production_profile_file, header=None, dtype=str)

    # Séparer chaque string en 3 colonnes
    production_profile = df[0].str.split(expand=True).astype(float).to_numpy()
    production_profile = np.repeat(production_profile, 4, axis=0)
    #print("production_profile shape:", np.sum(production_profile[:,:]))

    # production_profile aura la forme (8760, 3) avec des floats

  # Affiche les 3 valeurs de la première ligne sous forme de floats
    # print("production_profile[0, 0]:", production_profile[0, 0])
    if n_households is None:
        n_households = load_profile.shape[1]  # à vérifier si pas 1
    #n_households = 3  # Number of households, to change if needed
    dt = 0.25
    n_timestep = load_profile.shape[0]
    #n_timestep = 96
    m.time = RangeSet(0,n_timestep-1)  # 35040 timesteps for one year with 15 minutes intervals
    m.households = RangeSet(0, n_households - 1)  # 1 household
    #print("Number of households:", n_households)
    #print("Number of timesteps:", n_timestep)
    #print("load_profile shape:", load_profile)
    #print("load_profile tot sum:", np.sum(load_profile[:,:])*dt)
    tot_conso = np.sum(load_profile[:,0:n_households])*dt

    #########################
    #VARIABLES
    #########################
    if max_area is None:
        max_area = 10000
    if min_area is None:
        min_area = 2500
    
        
    max_kwc = max_area * 0.182  # Maximum kWc based on the area, 1 kWc = 5.5 m²
    area_init = (max_area+min_area) * 0.5  # Initial area set to 50% of the maximum area
    kwc_init = area_init * 0.182  # Initial kWc based on the initial area
    
    min_kwc = min_area * 0.182  # Minimum kWc based on the minimum area
    
    m.pv_area = Var(within=NonNegativeReals, bounds=(min_area, max_area), initialize=area_init)  # Area of the PV panels in m²
    m.wh_battery = Var(within=NonNegativeReals, bounds=(0,200000), initialize=80000)
    m.p_bat_max = Var(within=NonNegativeReals, initialize=40000)
    m.p = Var(m.households, m.time, within=NonNegativeReals, initialize=0)  # Power to each household in W
    m.p_bat_pos = Var(m.time, within=NonNegativeReals, initialize=0)
    m.p_bat_neg = Var(m.time, within=NonNegativeReals, initialize=0)  # Power to the battery in W
    #m.p_inj = Var(m.time, within=NonNegativeReals, initialize=0)
    m.p_ev = Var(m.time, within=NonNegativeReals, initialize=0)  # Power to EV, not used in this model
    m.soc = Var(m.time, within=NonNegativeReals, initialize=5000)  # State of charge of the battery in Wh, not used in this model
    #m.p_pv = Var(m.time, within=NonNegativeReals, initialize=0)  # Power from PV in W, not used in this model
    m.kWc = Var(within=NonNegativeReals, bounds=(min_kwc, max_kwc), initialize=kwc_init)  # Installed power in kWc, based on the area
    m.cv_coeff = Var(within=NonNegativeReals, bounds=(0.58, 1.953), initialize=1)  # Coefficient for the piecewise function, bounds can be adjusted
    m.price_per_kwc = Var(within=NonNegativeReals, bounds=(0, 4000), initialize=1500)  # Price per kWc, bounds can be adjusted
    m.p_ev_max = Var(within=NonNegativeReals, initialize=74000)  # Maximum power of the battery in W, to change as a ffunction to the capacity

    #########################
    #PARAMETERS
    #########################
    
    m.eff_bat = Param(initialize=0.9)  # Efficiency of the battery
    #m.p_bat_max = Param( initialize=10000)  # Maximum power of the battery in W, to change as a ffunction to the capacity
    m.annual_rate = Param(initialize=0.03)  # Annual rate for the PV costs
    m.lifetime = Param(initialize=25)  # Lifetime of the PV system in years
    m.lifetime_battery = Param(initialize=10)  # Lifetime of the battery in years
    year = 0
    breakpoints = [1.82, 36, 100, 250, 10000] # for cv_coeff
    
    breakpoints_price = [0, 10, 50, 100, 100000]  # adapte la borne supérieure si besoin

    # Les coefficients (x, y) pour chaque intervalle
    # Pour chaque palier : price_per_kwc = x * kWc + y
    price_x = [-240, -3.75, -3, -0.66]
    price_y = [3700, 1337.5, 1300, 1066.6]
    
    # print("Min production_profile:", np.min(production_profile[:, year]))
    # print("Max production_profile:", np.max(production_profile[:, year]))
    # print("Any negative?", np.any(production_profile[:, year] < 0))
    # print("production_profile[35009, year] =", production_profile[35009, year])
    production_profile = np.maximum(production_profile, 0)
    
    def pv_prod_rule(m, t):
        return production_profile[t, year] * m.pv_area
    m.pv_prod = Expression(m.time, rule=pv_prod_rule)
    
    def p_expr_rule(m, h, t):
        total_load = sum(load_profile[t, hh] for hh in range(n_households))
        pv_prod = m.pv_prod[t] + m.p_bat_neg[t]
        if total_load == 0:
            return 0
        else:
            return load_profile[t, h] * pv_prod / total_load     
    m.p_expr = Expression(m.households, m.time, rule=p_expr_rule)


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
        price_injection = injection_price  # price for injection, not used in this model
        price_ev = -1
        #####################
        #Revenue
        #####################
        total_bill_reduction = sum(
        m.p[h,t] * (price_night if time_is_night(t) else price_day) * dt * 0.001
        for t in m.time for h in m.households
        )
        p_inj = sum(m.pv_prod[t] - (
            sum(m.p[h, t] for h in m.households) + m.p_bat_pos[t] + m.p_ev[t] - m.p_bat_neg[t]
        ) for t in m.time)
        total_from_injection = p_inj * price_injection * dt * 0.001 
        total_from_ev = sum(m.p_ev[t] * price_ev * dt * 0.001 for t in m.time)
            
        #print("total_bill_reduction:", total_bill_reduction)
        #print("total_from_injection:", total_from_injection)
        #print("total_from_ev:", total_from_ev)
            
        #################
        # CV
        ##################

        cv_revenue = sum(m.pv_prod[t] for t in m.time) * m.cv_coeff * 65 * dt * 10 /(25 * 1000000)        #print("cv_revenue:", cv_revenue)
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
        battery_costs = m.wh_battery * capex_battery  # assuming 300 €/kWh for the battery
        battery_costs = battery_costs * (m.annual_rate / (1 - (1 + m.annual_rate) ** -m.lifetime_battery))  # 10 years lifetime for the battery
        
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
    
    def p_bat_max_rule(m):
        return m.p_bat_max <= m.wh_battery * 0.5
    m.p_bat_max_rule = Constraint(rule=p_bat_max_rule)
    
    def p_rule_1(m, h, t):
        return m.p[h, t] <= m.p_expr[h, t]
    m.p_rule_1 = Constraint(m.households, m.time, rule=p_rule_1)
    
    def p_rule_2(m, h, t):
        return m.p[h, t] <= load_profile[t, h]
    m.p_rule_2 = Constraint(m.households, m.time, rule=p_rule_2)
    
    def kwc_def_rule(m):   ## for cv_coeff
       return m.kWc == m.pv_area * 0.182
   
    # def cv_unique_rule(m):
    #     return m.cv_coeff == 2 # Coefficient for the piecewise function, can be adjusted
    # m.cv_unique = Constraint(rule=cv_unique_rule)
    
    # def price_unique_rule(m):
    #     return m.price_per_kwc == 1500
    # m.price_unique = Constraint(rule=price_unique_rule)
    
    m.kwc_def = Constraint(rule=kwc_def_rule)
    def cv_piecewise_rule(m, x):
        if x < 36:
            return 1.953
        elif x < 100:
            return 1.016
        elif x < 250:
            return 0.642
        else:
            return 0.58
        #return 0
    m.piecewise_cv = Piecewise(
    m.cv_coeff, m.kWc,
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
        elif x <120:
            return -0.66 * x + 1066.6
        else:
            return 987.4

    m.piecewise_price = Piecewise(
        m.price_per_kwc, m.kWc,
        pw_pts=breakpoints_price,
        f_rule=price_piecewise_rule,
        pw_constr_type='EQ',
        pw_repn='SOS2'
    )
    

    # def power_from_pv(m, t):
    #     return m.p_pv[t] == production_profile[t, year] * m.pv_area
    # m.power_from_pv = Constraint(m.time, rule=power_from_pv)
    
    def power_to_battery_pos(m, t):
        return m.p_bat_pos[t] <= m.p_bat_max
    m.power_to_battery_pos = Constraint(m.time, rule=power_to_battery_pos)
    
    def power_to_battery_neg(m, t):
        return m.p_bat_neg[t] <= m.p_bat_max
    m.power_to_battery_neg = Constraint(m.time, rule=power_to_battery_neg)
    
    # def power_bat_limit(m):
    #     return m.p_bat_max <= m.wh_battery * 0.5
    # m.power_bat_limit = Constraint(rule=power_bat_limit)
    def total_consumption_limit(m, t):
        return sum(m.p[h,t] for h in m.households) + m.p_bat_pos[t] + m.p_ev[t] <= production_profile[t, year] * m.pv_area + m.p_bat_neg[t]
    m.total_consumption_limit = Constraint(m.time, rule=total_consumption_limit)

    # def power_equality(m, t):
    #     return m.p_inj[t] == production_profile[t, year] * m.pv_area - (
    #         sum(m.p[h, t] for h in m.households) + m.p_bat_pos[t] + m.p_ev[t] - m.p_bat_neg[t]
    #     )
    # m.power_equality = Constraint(m.time, rule=power_equality)

    def soc_set(m, t):
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
    
    
    def p_ev_limit(m, t):
        return m.p_ev[t] <= m.p_ev_max
    m.p_ev_limit = Constraint(m.time, rule=p_ev_limit)
    
        # Avant le modèle Pyomo, calcule la demande totale pour chaque t
    total_load = {t: sum(load_profile[t, h] for h in range(n_households)) for t in range(n_timestep)}

    # def repartition_rule1(m, h, t):
    #     if total_load[t] == 0:
    #         return m.p[h, t] == 0
    #     return m.p[h, t] <= load_profile[t, h] * production_profile[t, year] * m.pv_area / total_load[t]
    # m.repartition1 = Constraint(m.households, m.time, rule=repartition_rule1)

    # def repartition_rule2(m, h, t):
    #     return m.p[h, t] <= load_profile[t, h]
    # m.repartition2 = Constraint(m.households, m.time, rule=repartition_rule2)

    gurobi.solve(m)
    import logging
    logging.basicConfig(level=logging.INFO)
    from pyomo.util.infeasible import log_infeasible_constraints
    log_infeasible_constraints(m)
    
    puissance_totale = sum(value(m.p[h,t]) for h in m.households for t in m.time)*0.25
    
    p_inj = sum(production_profile[t, year] * value(m.pv_area) - (
                sum(value(m.p[h, t]) for h in m.households) + value(m.p_bat_pos[t]) + value(m.p_ev[t]) - value(m.p_bat_neg[t])
            ) for t in m.time)
    puissance_produite = sum(production_profile[t, year] * value(m.pv_area)*0.25 for t in m.time)
    # print("Puissance totale distribuée aux ménages :", puissance_totale, "Wh")
    # print("puissance injectée :", p_inj * 0.025, "Wh")
    # print("puissance produite par les PV (p_pv) :", sum(production_profile[t, year] * value(m.pv_area)*0.25 for t in m.time))


    #  # Affichage des résultats principaux
    # print("Objectif (revenu total) :", value(m.objective))
    # print("Surface PV (pv_area) :", value(m.pv_area))

    # print("production_profile[65, year] :", production_profile[65, year])
    
    # print("Capacité batterie (wh_battery) :", value(m.wh_battery))
    # print("Puissance batterie max (p_bat_max) :", value(m.p_bat_max))
    # print("cv_coeff :", value(m.cv_coeff))
    # print("price par kwc", value(m.price_per_kwc))  # Affichage du prix par kWc
    pv_costs = value(m.kWc) * value(m.price_per_kwc)  # Calcul du coût total du PV
    pv_costs_annualized = pv_costs * (m.annual_rate / (1 - (1 + m.annual_rate) ** -m.lifetime))  # 25 years lifetime
    # print("pv costs", pv_costs_annualized)

    cv_revenue = sum(production_profile[t, year] * value(m.pv_area) for t in m.time) * value(m.cv_coeff) * 65 * dt * 10 /(25 * 1000000)
    # print("cv_revenue:", cv_revenue)
    price_day = 0.38
    price_night = 0.29
    price_injection = 0.04  # price for injection, not used in this model
    total_bill_reduction = sum(
        value(m.p_expr[h, t]) * (price_night if time_is_night(t) else price_day) * dt * 0.001
        for t in m.time for h in m.households
        )
    # print("total_bill_reduction:", total_bill_reduction)
    
    total_cost_without = sum(load_profile[t, h] * (price_night if time_is_night(t) else price_day) * dt * 0.001
                             for t in m.time for h in m.households)

    total_from_injection = p_inj * price_injection * dt * 0.001   
    # print("total_from_injection:", total_from_injection)
    # print("ev_max:", value(m.p_ev_max))
    print("n households:", n_households)
    return n_households, value(m.objective), value(m.kWc), value(m.wh_battery), puissance_totale, puissance_produite, tot_conso, value(m.p_bat_max), total_cost_without
    


def main_simu():

    results = []
    production_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/production_profile.csv"  # adapte le chemin si besoin

    for n in range(30,49):  # adapte la liste à tes cas
        #load_profile_file = f"C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/{n}_households_0_years.csv"
        load_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/combined_household_power_consumption_48_2.csv"
        try:
            res = first(load_profile_file, production_profile_file, capex_battery=0.3, n_households=n)
            results.append(res)
        except Exception as e:
            print(f"Erreur pour {n} ménages : {e}")
            continue

    # Adapter les noms de colonnes à ce que retourne first
    columns = [
        "n_households", "objective", "kWc", "wh_battery",
        "puissance_totale", "puissance_produite", "tot_conso", "p_bat_max", "total_cost_without "
    ]
    df = pd.DataFrame(results, columns=columns)

    # Pour voir le résultat
    print(df)
    df.to_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/resultats_simulations_unconst_capex_03_otherdata_2.csv", index=False)
    
#main_simu()

def twenty_households():
    production_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/production_profile.csv"  # adapte le chemin si besoin
    load_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/20_households_0_years.csv"
    max_area = np.linspace(50, 1250, 20)  # Exemple de valeurs pour max_area
    min_area = np.linspace(20, 750, 20)  # Exemple de valeurs pour min_area
    results = []
    for i in range(len(max_area)):
        try:
            res = first(load_profile_file, production_profile_file, n_households=20, max_area=max_area[i], min_area=min_area[i])
            results.append((max_area[i], min_area[i]) + res)
        except Exception as e:
            print(f"Erreur pour max_area={max_area[i]}, min_area={min_area[i]} : {e}")
            continue
    print(results)
    columns = [
        "max_area", "min_area", "n_households", "objective", "kWc", "wh_battery",
        "puissance_totale", "puissance_produite", "tot_conso", "p_bat_max", "total_cost_without"
    ]
    df = pd.DataFrame(results, columns=columns)
    print(df)
    df.to_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/resultats_twenty_households_correct_2.csv", index=False)
#twenty_households()


def capex_batt():
    capexes = np.array([0.1])
    injection_prices = np.linspace(0.06,0.1,5)
    
    production_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/production_profile.csv"  # adapte le chemin si besoin
    load_profile_file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/load_profile_simu/20_households_0_years.csv"
    results = []
    for capex in capexes:
        for injection_price in injection_prices:
            try:
                res = first(load_profile_file, production_profile_file, capex_battery=capex, injection_price=injection_price)
                results.append((capex, injection_price) + res)
                print(f"Résultat pour capex {capex} et injection price {injection_price} : {res}")
            except Exception as e:
                print(f"Erreur pour capex {capex} et injection price {injection_price} : {e}")
                continue
            
    # capexes_2 = np.linspace(0.1,0.3,4)
    # injection_prices_2 = np.array([0.05])
    
    # for capex in capexes_2:
    #     for injection_price in injection_prices_2:
    #         try:
    #             res = first(load_profile_file, production_profile_file, capex_battery=capex, injection_price=injection_price)
    #             results.append((capex, injection_price) + res)
    #             print(f"Résultat pour capex {capex} et injection price {injection_price} : {res}")
    #         except Exception as e:
    #             print(f"Erreur pour capex {capex} et injection price {injection_price} : {e}")
    #             continue
    columns = [
        "capex_battery", "injection_price", "n_households", "objective", "kWc", "wh_battery",
        "puissance_totale", "puissance_produite", "tot_conso", "p_bat_max", "total_cost_without"
    ]
    df = pd.DataFrame(results, columns=columns)
    print(df)
    df.to_csv("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/new/resultats_capex_battery_correct_4.csv", index=False)
    

#capex_batt()