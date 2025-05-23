### Master thesis, Simon De Vaddern electricity sharing in multi units buildings
###  example file 2, containing examples with mutlihousehold class

import numpy as np
import pandas as pd
from datetime import date
import sys
import os
from matplotlib import pyplot as plt
import seaborn as sns
from energy_community import EnergyCommunity
from household import Household
from multihousehold import MultiHousehold


def example_1():
        """ This example shows how to run the model with an example building 
        The building analysed has the fllowing features : 
        PV : 2 sets : 
                - orientation = 80, inclinaison = 40, surface = 122.5
                - orientation = 260, inclinaison = 40, surface = 103

        flats : 1 duplex 4 rooms and 7 flats 2 rooms
                - duplex  : 250m^2, PEB E, gas heating, familly of 2 parents and 2 children
                                wh_type = elec
                                wh_capacity = high
                                heating_type = non-electric
                                number_cold_source = 2
                                have_washing_machine = True
                                washing_frequency = medium
                                have_dryer = True
                                dryer_usage = medium
                                dryer_type = condensation
                        have_dishwasher = True
                        dishwasher_frequency = high
                - flats : 7 flats 2 rooms, 95m^2, PEB E, gas heating
                                wh_type = elec
                                wh_capacity = medium
                                heating_type = non-electric
                                number_cold_source = 1
                                have_washing_machine = True, one False
                                washing_frequency = 4 low, 2 medium, 1 null
                                have_dryer = 1 True (one of the medium), 6 False
                                dryer_type = condensation, or None
                        have_dishwasher = 4 True, 3 False
                        dishwasher_frequency = 2 medium, 2 low
        """
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_out", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                        "n_households" : 8, "key" : "hybrid", "PV_inclination": [40], "PV_orientation" : [260], "PV_area" : [77], "PV_efficiency" : 0.16, "PV_module_size": [1.6, 0.99, 0.008],
                        "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 18000, "estimated_lifetime" : 25, "interest_rate" : 0.03 }


        input_directory = "pv_out"
        output_directory = "example_multi"
        n_households = 8
        cooking_params = ["high", "medium", "low", "low", "medium", "low", "high", "medium"]
        wh_capacity_params = ["high", "medium", "medium", "medium", "medium", "medium", "medium", "medium"]
        n_cold_source_params = [2, 1, 1, 1, 1, 1, 1, 1]
        wm_frequency_params = ["medium", "medium", "medium", "low", "low", "low", "low", "low"]
        have_dryer_params = [True, False, True, False, False, False, False, False]
        dryer_type_params = ["condensation", None, "condensation", None, None, None, None, None]
        dryer_frequency_params = ["high", None, "medium", None, None, None, None, None]
        have_dw_params = [True, True, True, True, False, False, True, False]
        dw_frequency_params = ["medium", "low", "medium", "medium", None, None, "low", None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29]
        wh_intelligence_params = True
        #wh_night = [False, False, False, False, False, False, False, False]
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_capacity_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
             #   "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
        }
        
        enercom = EnergyCommunity(pv_params)
        enercom.func_compute_total_production()
        multi = MultiHousehold(params, enercom)
        multi.run()
        multi.repartition_elec()
        multi.compute_metrics()
        multi.pricing()
        multi.save_results()

#example_1()

def example_2():
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [548], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03
                
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        #"EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv'
        

        input_directory = "pv_example_2"
        output_directory = "example_2_19mai"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [95] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        kWc = pv_params["PV_area"][0] * pv_params["PV_efficiency"] 
        if kWc <=10:
                x = -240
                y = 3700
                price_per_kwc = x * kWc + y
                pv_params["investment_cost"] = price_per_kwc * kWc
        elif kWc <=50:
                x = -3.75
                y = 1337.5
                price_per_kwc = x * kWc + y
                pv_params["investment_cost"] = price_per_kwc * kWc
        elif kWc <=100:
                x = -3
                y = 1300
                price_per_kwc = x * kWc + y
                pv_params["investment_cost"] = price_per_kwc * kWc  
        else : 
                x = -0.66
                y = 1066.6
                price_per_kwc = x * kWc + y
                pv_params["investment_cost"] = price_per_kwc * kWc
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        #enercom.save_production()
        multi = MultiHousehold(params, enercom)
        multi.run()
        multi.repartition_elec()
        multi.compute_metrics()
        multi.pricing()
        
        cv_coeff = 0
        if kWc < 5:
                cv_coeff = 2.055
        elif kWc < 36:
                cv_coeff = 1.953
        elif kWc < 100:
                cv_coeff = 1.016
        elif kWc < 250:
                cv_coeff = 0.642
        else : 
                cv_coeff = 0.58
        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
        print("Annualized revenue from cv : ", cv_revenue)
        cost = multi.annualized_investment_cost  #+ 0.05433*10000
        print("Annualized cost : ", cost)
        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
        print("Total gain : ", tot_gain)
        tot_gain += cv_revenue
        # print("Total gain with cv : ", tot_gain)
        # rev_from_ev = np.mean(multi.total_revenue_from_ev[:])
        # print("Total gain from ev : ", rev_from_ev)
        # print("ev_from_pv", multi.ev_total_from_pv)
        # print("ev_share", multi.ev_share_from_pv)
        # print("ev_conso", multi.ev_charger_tot_conso)

        multi.save_results()
        
#example_2()

def compute_roi():
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.22, "PV_module_size": [1.6, 0.99, 0.008],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 90000, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                 "EV_charger" : True, "EV_price" : 0.45}
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        
        

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["high", "medium", "low", "low", "medium", "low", "high", "medium", "high", "medium", "low", "low", "medium", "low", "high", "medium", "high", "medium", "high", "medium", "low", "low", "medium", "low" ]
        wh_capacity_params = ["high", "medium", "low", "medium", "low", "medium", "medium", "medium", "high", "medium", "medium", "low", "low", "medium", "medium", "medium", "high", "medium", "low", "medium", "low", "medium", "high", "medium"]
        n_cold_source_params = [2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2,1,1,1,1,2,1,2,1]
        wm_frequency_params = ["medium", "medium", "medium", "low", "low", "low", "low", "low", "medium", "high", "medium", "low", "low", "high", "low", "medium", "medium", "high", "medium", "low", "low", "low", "low", "high"]
        have_dryer_params = [True, False, True, False, False, False, False, False, True, False, True, False, False, False, False, False, True, False, True, False, False, False, True, False]
        dryer_type_params = ["condensation", None, "condensation", None, None, None, None, None, "evacuation", None, "heat-pump", None, None, None, None, None, "heat-pump", None, "evacuation", None, None, None, "condensation", None]
        dryer_frequency_params = ["high", None, "medium", None, None, None, None, None, "low", None, "medium", None, None, None, None, None, "medium", None, "low", None, None, None, "medium", None]
        have_dw_params = [True, True, True, True, False, False, True, False, True, True, True, True, True, False, False, False, False, False, True, True, True, True, False, False, True, False]
        dw_frequency_params = ["medium", "low", "medium", "medium", None, None, "low", None, "medium", "medium", "low", "high", "medium", "high", None, None, None, None, None, "medium", "low", "medium", "low", None, None, "low", None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,8,14,11,13,13,11,14,12,10,11,9,13,15,12,12,12,11,13,15,9,8,16,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        PEB_params = ["A","B", "A", "B", "A", "B", "A", "B", "A","B", "A", "B", "A", "B", "A", "B", "A","B", "A", "B", "A","B", "A","B"]
        heating_eff_params = [2.3]*n_households
        
        flat_area_params = [40,66,120,150,250,66,40,50,40,66,120,150,250,66,40,50,40,66,120,150,250,66,40,50]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [True]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_capacity_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
        }
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        #enercom.save_production()
        multi = MultiHousehold(params, enercom)
        multi.annual_return_lifetime()
        print("ROI : ", multi.roi)
        print("Annual return : ", multi.mean_annual_return)
        print("return array", multi.annual_return)
        print("investment cost" , enercom.investment_cost)
        print("Annual cost : ", multi.annual_cost)
        print("annual return rate", multi.annual_return_rate)
        #multi.run()
        #multi.repartition_elec()
        #multi.compute_metrics()
        #multi.pricing()
        #multi.save_results()
#compute_roi()
        
def compute_single_home():
         
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.22, "PV_module_size": [1.6, 0.99, 0.008],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0, "grid_injection_price" : 0.04, "investment_cost" : 90000, "estimated_lifetime" : 25, "interest_rate" : 0.03
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        

        input_directory = "pv_example_2"
        output_directory = "single_home"
        n_households = 1
        cooking_params = ["high"]
        wh_capacity_params = ["high"]
        n_cold_source_params = [2]
        wm_frequency_params = ["medium"]
        have_dryer_params = [True]
        dryer_type_params = ["condensation"]
        dryer_frequency_params = ["high"]
        have_dw_params = [True]
        dw_frequency_params = ["medium"]
        grid_price_day_params=[0.36]
        grid_price_night_params=[0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12]
        T_ext_th_night_params = [7]
        PEB_params = ["A"]
        heating_eff_params = [2.3]*n_households
        
        flat_area_params = [120]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_capacity_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
        }
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        #enercom.save_production()
        multi = MultiHousehold(params, enercom)
        multi.run()
        multi.repartition_elec()
        multi.compute_metrics()
        multi.pricing()
        multi.save_results()
        
        
#compute_single_home()    

def plot_graph_pv_bat():
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [40] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        
        
        autoconsommation = np.zeros((10, 10))
        autoproduction = np.zeros((10, 10))
        gain_net_tot = np.zeros((10, 10))
        cost_tot = np.zeros((10, 10))
        rev_tot = np.zeros((10, 10))
        power = np.zeros(10)
        bat = np.zeros(10)
        area = np.linspace(20, 600, 10)
        for i in range(10):
                for j in range(10):
                        pv_params["PV_area"] = [area[i]]
                        kWc = pv_params["PV_area"][0] * pv_params["PV_efficiency"] 
                        if kWc <=10:
                                x = -240
                                y = 3700
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        elif kWc <=50:
                                x = -3.75
                                y = 1337.5
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        elif kWc <=100:
                                x = -3
                                y = 1300
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc  
                        else : 
                                x = -0.66
                                y = 1066.6
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc   

                        pv_params["battery_capacity"] = 5000*j
                        enercom = EnergyCommunity(pv_params)
                        enercom.func_compute_total_production()
                        multi = MultiHousehold(params, enercom)
                        multi.run()
                        multi.repartition_elec()
                        multi.compute_metrics()
                        multi.pricing()
                        cost = multi.annualized_investment_cost  + 0.05433*5000*j
                        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                        
                        autoconsommation[i, j] = np.mean(multi.self_consumption[:])
                        autoproduction[i, j] = np.mean(multi.self_sufficiency[:,:])
                        #### CV revenue
                        power[i] = kWc
                        bat[j] = pv_params["battery_capacity"]
                        cv_coeff = 0
                        if kWc < 5:
                                cv_coeff = 2.055
                        elif kWc < 36:
                                cv_coeff = 1.953
                        elif kWc < 100:
                                cv_coeff = 1.016
                        elif kWc < 250:
                                cv_coeff = 0.642
                        else : 
                                cv_coeff = 0.58
                        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                        tot_gain += cv_revenue
                        gain_net = tot_gain - cost
                        gain_net_tot[i, j] = gain_net
                        cost_tot[i, j] = cost
                        rev_tot[i, j] = tot_gain
                        print("i", i)
                        print("j", j)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/bat.npy", bat)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/power.npy", power)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/autoconsommation.npy", autoconsommation)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/autoproduction.npy", autoproduction)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/gain_net_tot.npy", gain_net_tot)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/cost_tot.npy", cost_tot)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/pv_bat_folder/rev_tot.npy", rev_tot)
        
        bat = bat / 1000
        fig, ax = plt.subplots(figsize=(10, 6))
        c = ax.pcolormesh(bat, power, autoconsommation, cmap='viridis', shading='auto')
        fig.colorbar(c, ax=ax)
        ax.set_title('Self-consumption')
        ax.set_xlabel('Battery capacity (kWh)')
        ax.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        c2 = ax2.pcolormesh(bat, power, autoproduction, cmap='viridis', shading='auto')
        fig2.colorbar(c2, ax=ax2)
        ax2.set_title('Self-sufficiency')
        ax2.set_xlabel('Battery capacity (kWh)')
        ax2.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        c3 = ax3.pcolormesh(bat, power, gain_net_tot, cmap='viridis', shading='auto')
        fig3.colorbar(c3, ax=ax3)
        ax3.set_title('Net gain (euro)')
        ax3.set_xlabel('Battery capacity (kWh)')
        ax3.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        c4 = ax4.pcolormesh(bat, power, cost_tot, cmap='viridis', shading='auto')
        fig4.colorbar(c4, ax=ax4)
        ax4.set_title('Cost (euro)')
        ax4.set_xlabel('Battery capacity (kWh)')
        ax4.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        c5 = ax5.pcolormesh(bat, power, rev_tot, cmap='viridis', shading='auto')
        fig5.colorbar(c5, ax=ax5)
        ax5.set_title('Revenue (euro)')
        ax5.set_xlabel('Battery capacity (kWh)')
        ax5.set_ylabel('Pv peak power [kWp]')
        plt.show()
        
        
#plot_graph_pv_bat()

def example_2_with_ev():
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/Charging_Profiles_1ev.csv'
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [40] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        evs = [1,3,4,5,6,9,11,13,15,17,20]
        area = np.linspace(20,600,11)
        power = area * pv_params["PV_efficiency"]
        part_from_pv = np.zeros((11,11))
        autoconso = np.zeros((11,11))
        paid_by_ev = np.zeros((11,11))
        gain_net = np.zeros((11,11))
        for i in range(11): 
                print(i)
                pv_params["PV_area"]=[area[i]]
                kWc = power[i]
                for j in range(len(evs)) :
                        print(j)
                        ev = evs[j]
                        
                        pv_params["EV_file"] = f'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/Charging_Profiles_{ev}ev.csv'
                        params["output_directory"] = f"exemple_2_{ev}ev"
                        
                        if kWc <=10:
                                x = -240
                                y = 3700
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        elif kWc <=50:
                                x = -3.75
                                y = 1337.5
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        elif kWc <=100:
                                x = -3
                                y = 1300
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc  
                        else : 
                                x = -0.66
                                y = 1066.6
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        enercom = EnergyCommunity(pv_params)
                        #enercom.get_weather_data()
                        enercom.func_compute_total_production()
                        cv_coeff = 0
                        if kWc < 5:
                                cv_coeff = 2.055
                        elif kWc < 36:
                                cv_coeff = 1.953
                        elif kWc < 100:
                                cv_coeff = 1.016
                        elif kWc < 250:
                                cv_coeff = 0.642
                        else : 
                                cv_coeff = 0.58
                        #enercom.save_production()
                        multi = MultiHousehold(params, enercom)
                        multi.run()
                        multi.repartition_elec()
                        multi.compute_metrics()
                        
                        
                        multi.pricing()
                        autoconso[i,j] = np.mean(multi.self_consumption[:])
                        part_from_pv[i,j] = np.mean(multi.ev_share_from_pv[:])*100
                        paid_by_ev[i,j] = np.mean(multi.total_paid_by_ev[:])
                        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)

                        cost  = multi.annualized_investment_cost 
                        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                        tot_gain += cv_revenue
                        gain_net[i,j] = tot_gain - cost
                        #multi.save_results()
                        
        fig, ax = plt.subplots(figsize=(10, 6))
        c = ax.pcolormesh(evs, power, part_from_pv, cmap='viridis', shading='auto')
        fig.colorbar(c, ax=ax)
        ax.set_title('Share of EV electricity coming from PV (%)')
        ax.set_xlabel('Number of EV')
        ax.set_ylabel('Peak power of installation [kWc]')
        plt.show()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        c2 = ax2.pcolormesh(evs, power, autoconso, cmap='viridis', shading='auto')
        fig2.colorbar(c2, ax=ax2)
        ax2.set_title('Self-consumption (%)')
        ax2.set_xlabel('Number of EV')
        ax2.set_ylabel('Peak power of installation [kWc]')
        plt.show()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        c = ax.pcolormesh(evs, power, gain_net, cmap='viridis', shading='auto')
        fig.colorbar(c, ax=ax)
        ax.set_title('Net gain for the community (euro)')
        ax.set_xlabel('Number of EV')
        ax.set_ylabel('Peak power of installation [kWc]')
        plt.show()
        
        
#example_2_with_ev()
        
def gain_pv_power():
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        

        input_directory = "pv_example_2"
        output_directory = "example_2_news"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,8,14,11,13,13,11,13,12,10,11,9,13,14,12,12,12,11,13,14,9,8,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [40] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        area_array = np.linspace(20,600, 20)
        kWc_array = area_array * pv_params["PV_efficiency"] 
        interest_rate_array = np.array([0.0,0.01,0.02,0.03,0.04])
        gain_array = np.zeros((len(area_array), len(interest_rate_array)))
        cost_array = np.zeros((len(area_array), len(interest_rate_array)))
        rev_array = np.zeros((len(area_array), len(interest_rate_array)))
        autoconsommation = np.zeros((len(area_array), len(interest_rate_array)))
        autoproduction = np.zeros((len(area_array), len(interest_rate_array)))
        
        for i in range(len(area_array)):
                for j in range(len(interest_rate_array)):
                        print(i)
                        print(j)
                        pv_params["PV_area"] = [area_array[i]]
                        kWc = kWc_array[i]
                        if kWc <=10:
                                x = -240
                                y = 3700
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        elif kWc <=50:
                                x = -3.75
                                y = 1337.5
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc
                        elif kWc <=100:
                                x = -3
                                y = 1300
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc  
                        else : 
                                x = -0.66
                                y = 1066.6
                                price_per_kwc = x * kWc + y
                                pv_params["investment_cost"] = price_per_kwc * kWc   

                        pv_params["interest_rate"] = interest_rate_array[j]
                        enercom = EnergyCommunity(pv_params)
                        #enercom.get_weather_data()
                        enercom.func_compute_total_production()
                        #enercom.save_production()
                        multi = MultiHousehold(params, enercom)
                        multi.run()
                        multi.repartition_elec()
                        multi.compute_metrics()
                        multi.pricing()
                        cost  = multi.annualized_investment_cost 
                        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                        
                        autoconsommation[i, j] = np.mean(multi.self_consumption[:])
                        autoproduction[i, j] = np.mean(multi.self_sufficiency[:,:])
                        #### CV revenue
                        cv_coeff = 0
                        if kWc < 5:
                                cv_coeff = 2.055
                        elif kWc < 36:
                                cv_coeff = 1.953
                        elif kWc < 100:
                                cv_coeff = 1.016
                        elif kWc < 250:
                                cv_coeff = 0.642
                        else : 
                                cv_coeff = 0.58
                        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                        tot_gain += cv_revenue
                        gain_net = tot_gain - cost
                        gain_array[i, j] = gain_net
                        cost_array[i, j] = cost
                        rev_array[i, j] = tot_gain
                        print("i", i)
                        print("j", j)
                        
                        #multi.save_results()
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/gain_array.npy", gain_array)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/cost_array.npy", cost_array)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/rev_array.npy", rev_array)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/autoconsommation.npy", autoconsommation)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/autoproduction.npy", autoproduction)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/kWc_array.npy", kWc_array)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/area_array.npy", area_array)
        np.save("C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/example_2_new_folder/interest_rate_array.npy", interest_rate_array)
        
        
        for i in range(len(interest_rate_array)):
                plt.plot(kWc_array, gain_array[:,i], label = f"interest rate {interest_rate_array[i]}")
        plt.xlabel("kWc")
        plt.ylabel("Gain (euro)")
        plt.legend()
        plt.show()
        
        plt.plot(kWc_array, cost_array[:,0], label = f"interest rate {interest_rate_array[0]}")
        plt.ylabel("Cost (euro)")
        plt.legend()
        plt.show()
        
        
        plt.plot(kWc_array, rev_array[:,0], label = f"interest rate {interest_rate_array[0]}")
        plt.ylabel("Revenue (euro)")
        plt.legend()
        plt.show()
        
        
        
#gain_pv_power()
def ev_100kw():
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/Charging_Profiles_1ev.csv'
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [40] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        evs = [1,3,4,5,6,9,11,13,15,17,20]
        
        part_from_pv = np.zeros((11))
        autoconso = np.zeros((11))
        paid_by_ev = np.zeros((11))
        gain_net = np.zeros((11))
        
        pv_params["PV_area"]=[550]
        kWc = 550 * pv_params["PV_efficiency"]
        for j in range(len(evs)) :
                print(j)
                ev = evs[j]
                
                pv_params["EV_file"] = f'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/Charging_Profiles_{ev}ev.csv'
                params["output_directory"] = f"exemple_2_{ev}ev"
                
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                enercom = EnergyCommunity(pv_params)
                #enercom.get_weather_data()
                enercom.func_compute_total_production()
                cv_coeff = 0
                if kWc < 5:
                        cv_coeff = 2.055
                elif kWc < 36:
                        cv_coeff = 1.953
                elif kWc < 100:
                        cv_coeff = 1.016
                elif kWc < 250:
                        cv_coeff = 0.642
                else : 
                        cv_coeff = 0.58
                #enercom.save_production()
                multi = MultiHousehold(params, enercom)
                multi.run()
                multi.repartition_elec()
                multi.compute_metrics()
                
                
                multi.pricing()
                print(np.mean(multi.self_consumption[:]))
                autoconso[j] = np.mean(multi.self_consumption[:])*100
                part_from_pv[j] = np.mean(multi.ev_share_from_pv[:])*100
                paid_by_ev[j] = np.mean(multi.total_paid_by_ev[:])
                cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)

                cost  = multi.annualized_investment_cost 
                tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                tot_gain += cv_revenue
                gain_net[j] = tot_gain - cost
                #multi.save_results()
        
        print(autoconso)              
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(evs, part_from_pv)
        ax.set_title('Share of EV electricity coming from PV (%)')
        ax.set_xlabel('Number of EV')
        ax.set_ylabel('Share of EV electricity coming from PV [%]')
        plt.show()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(evs, autoconso)
        ax2.set_title('Self-consumption (%)')
        ax2.set_xlabel('Number of EV')
        ax2.set_ylabel('self-consumption [%]')
        plt.show()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(evs, gain_net)
        ax.set_title('Net gain for the community (euro)')
        ax.set_xlabel('Number of EV')
        ax.set_ylabel('Net gain')
        plt.show()               
        
                        
        
       
#ev_100kw()

def price_pv_bat():
        """Modification of the price range 
        Based on the price of 2012 (1404 euro/kWc) and 2020 (628 euro/kWc), the study computed the estimated capex of solar in 2030 and 2050, based ont that
        """
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000
                
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        #"EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv'

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [90] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        #enercom.save_production()
        multi = MultiHousehold(params, enercom)
        multi.run()
        #multi.repartition_elec()
        #multi.compute_metrics()
        #multi.pricing()
        
        enercom_array = []
        
        price_per_kwp = np.linspace(600,2500,10)  #628 is the lowest capex estimation found in the literature
        area_array = np.linspace(20,600, 10)
        #area_array = np.linspace(500,600, 10)
        kWc_array = area_array * pv_params["PV_efficiency"]
        bat_array = np.linspace(0,50000, 10)
        #bat_array = np.linspace(5000,10000, 10)
        gains = np.zeros((len(bat_array), len(area_array)))
        autoconsommation = np.zeros((len(bat_array), len(area_array)))
        autoproduction = np.zeros((len(bat_array), len(area_array)))
        
        annualized_costs_norm = np.zeros((len(bat_array), len(area_array)))
        ################Compute the production
        print("beginning of the production computation")
        for i in range(len(area_array)):
                print("i", i)
                pv_params["PV_area"] = [area_array[i]]
                kWc = kWc_array[i]
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                this_enercom = EnergyCommunity(pv_params)   
                this_enercom.func_compute_total_production()
                enercom_array.append(this_enercom)
                
        #compute the repartition as a fonction of the battery power
        print("beginning of the repartition computation")
        for i in range(len(bat_array)):
                for j in range(len(enercom_array)):
                        print("i", i)
                        print("j", j)
                        this_enercom = enercom_array[j]
                        kWc = this_enercom.PV_area[0] * this_enercom.PV_efficiency
                        this_enercom.battery_capacity = bat_array[i]
                        multi.enercom = this_enercom
                        multi.production = this_enercom.total_production
                        #print("sum production", np.sum(multi.production[:,0]))
                        multi.repartition_elec()
                        multi.compute_metrics()
                        multi.pricing()
                        cv_coeff = 0
                        if kWc < 5:
                                cv_coeff = 2.055
                        elif kWc < 36:
                                cv_coeff = 1.953
                        elif kWc < 100:
                                cv_coeff = 1.016
                        elif kWc < 250:
                                cv_coeff = 0.642
                        else : 
                                cv_coeff = 0.58
                        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                        tot_gain += cv_revenue
                        #cost = this_enercom.annualized_investment_cost + 0.05433 * bat_array[i]
                        cost = this_enercom.annualized_investment_cost + 0.03 * bat_array[i]  #300eur/kWh sur 10 ans
                        annualized_costs_norm[i,j] = cost
                        
                        autoconsommation[i, j] = np.mean(multi.self_consumption[:])
                        autoproduction[i, j] = np.mean(multi.self_sufficiency[:,:])
                        gains[i,j] = tot_gain
                        multi.clean_production()
                        
        
        print("gains :", gains)
        print("beginning of costs function")
        gains = gains.T
        autoconsommation = autoconsommation.T
        autoproduction = autoproduction.T
        annualized_costs_norm = annualized_costs_norm.T
        
        bat = bat_array / 1000
        power = kWc_array 
        gain_net_tot = gains - annualized_costs_norm
        
        fig, ax = plt.subplots(figsize=(10, 6))
        c = ax.pcolormesh(bat, power, autoconsommation, cmap='viridis', shading='auto')
        fig.colorbar(c, ax=ax)
        ax.set_title('Self-consumption')
        ax.set_xlabel('Battery capacity (kWh)')
        ax.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        c2 = ax2.pcolormesh(bat, power, autoproduction, cmap='viridis', shading='auto')
        fig2.colorbar(c2, ax=ax2)
        ax2.set_title('Self-sufficiency')
        ax2.set_xlabel('Battery capacity (kWh)')
        ax2.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        c3 = ax3.pcolormesh(bat, power, gain_net_tot, cmap='viridis', shading='auto')
        fig3.colorbar(c3, ax=ax3)
        ax3.set_title('Net gain (euro)')
        ax3.set_xlabel('Battery capacity (kWh)')
        ax3.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        c4 = ax4.pcolormesh(bat, power, annualized_costs_norm, cmap='viridis', shading='auto')
        fig4.colorbar(c4, ax=ax4)
        ax4.set_title('Cost (euro)')
        ax4.set_xlabel('Battery capacity (kWh)')
        ax4.set_ylabel('PV peak power [kWp]')
        plt.show()
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        c5 = ax5.pcolormesh(bat, power, gains, cmap='viridis', shading='auto')
        fig5.colorbar(c5, ax=ax5)
        ax5.set_title('Revenue (euro)')
        ax5.set_xlabel('Battery capacity (kWh)')
        ax5.set_ylabel('Pv peak power [kWp]')
        plt.show()
        interest_rate = 0.03
        life_time = 25
        max_indices_array = []
        max_value_array = []
        for k in range(len(price_per_kwp)):
                this_price = price_per_kwp[k]   
                price_matrix = np.zeros((len(bat_array), len(area_array)))
                for i in range(len(bat_array)):
                        for j in range(len(area_array)):
                                this_area = area_array[j]
                                this_bat = bat_array[i]
                                kWc = this_area * pv_params["PV_efficiency"]
                                tot_price = this_price * kWc 
                                annual_price =  tot_price * interest_rate / (1-(1/(1+interest_rate))**life_time)
                                #annual_price += 0.05433 * this_bat
                                annual_price += 0.03 * this_bat  #300eur/kWh sur 10 ans
                                price_matrix[i,j] = annual_price
                
                price_matrix = price_matrix.T
                net_gain_matrix = gains - price_matrix
                net_gain_matrix = net_gain_matrix.T
                print("net gain matrix", net_gain_matrix)
                a = np.argmax(net_gain_matrix)
                print("indices", a)
                print("i = ", a // 10)
                print("j = ", a % 10)
                max_indices = np.unravel_index(np.argmax(net_gain_matrix), net_gain_matrix.shape)
                max_indices_array.append(max_indices)
                max_value = net_gain_matrix[max_indices]
                max_value_array.append(max_value)
                
                
        print("pricing done, beginning graphs")
        print(net_gain_matrix)
        print(max_indices_array)
        optimal_battery = [bat_array[idx[0]]/1000 for idx in max_indices_array]
        optimal_kwc = [area_array[idx[1]] * 0.182 for idx in max_indices_array]  # 0.182 est l'efficacité PV

        # Création du scatter plot
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(optimal_battery, optimal_kwc, c=price_per_kwp, cmap='viridis', s=100, edgecolor='k')
        plt.xlim(0, 50)  # Limite de l'axe des x (capacité de batterie)
        plt.ylim(0, 100)  # Limite de l'axe des y (puissance crête des panneaux)

        # Ajouter une barre de couleur pour indiquer le prix
        cbar = plt.colorbar(scatter)
        cbar.set_label('Prix par kWp (€)', rotation=270, labelpad=15)

        # Ajouter des labels et un titre
        plt.title("Évolution des configurations optimales en fonction du prix")
        plt.xlabel("Capacité de batterie (kWh)")
        plt.ylabel("Puissance crête des panneaux (kWc)")
        plt.grid(True)

        # Afficher le graphique
        plt.show()

#price_pv_bat()
        
        
def ev_bat():
        """modification of the number of ev charger plugged in 
        """
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [548], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,"EV_charger" : True, "EV_price" : 0.3,
                'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv', "number_ev_charger": 1      
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        #"EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv'

        input_directory = "pv_example_2"
        output_directory = "example_2_ev_charger"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [95] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        #enercom.save_production()
        multi = MultiHousehold(params, enercom)
        multi.run()
        #multi.repartition_elec()
        #multi.compute_metrics()
        #multi.pricing()
        
        enercom_array = []
        
        #area_array = np.linspace(20,600, 10)
        #bat_array = np.linspace(0,50000, 10)
        ev_arr = np.array([0,1,2,3])
        bat_array = np.linspace(0,50000, 10)
        gains = np.zeros((len(bat_array), len(ev_arr)))
        autoconsommation = np.zeros((len(bat_array), len(ev_arr)))
        autoproduction = np.zeros((len(bat_array), len(ev_arr)))
        
        annualized_costs_norm = np.zeros((len(bat_array), len(ev_arr)))
        ################Compute the production
        print("beginning of the production computation")
        for i in range(len(ev_arr)):
                print("i", i)
                pv_params["number_ev_charger"] = ev_arr[i]
                if pv_params["number_ev_charger"] == 0:
                        pv_params["EV_charger"] = False
                else : 
                        pv_params["EV_charger"] = True
                kWc = pv_params["PV_area"][0] * pv_params["PV_efficiency"]
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                this_enercom = EnergyCommunity(pv_params)   
                this_enercom.func_compute_total_production()
                enercom_array.append(this_enercom)
                
        #compute the repartition as a fonction of the battery power
        print("beginning of the repartition computation")
        for i in range(len(bat_array)):
                for j in range(len(enercom_array)):
                        print("i", i)
                        print("j", j)
                        this_enercom = enercom_array[j]
                        kWc = this_enercom.PV_area[0] * this_enercom.PV_efficiency
                        this_enercom.battery_capacity = bat_array[i]
                        multi.enercom = this_enercom
                        multi.production = this_enercom.total_production
                        #print("sum production", np.sum(multi.production[:,0]))
                        multi.repartition_elec()
                        multi.compute_metrics()
                        multi.pricing()
                        cv_coeff = 0
                        if kWc < 5:
                                cv_coeff = 2.055
                        elif kWc < 36:
                                cv_coeff = 1.953
                        elif kWc < 100:
                                cv_coeff = 1.016
                        elif kWc < 250:
                                cv_coeff = 0.642
                        else : 
                                cv_coeff = 0.58
                        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                        tot_gain += cv_revenue
                        cost = this_enercom.annualized_investment_cost + 0.05433 * bat_array[i]
                        annualized_costs_norm[i,j] = cost
                        
                        autoconsommation[i, j] = np.mean(multi.self_consumption[:])
                        autoproduction[i, j] = np.mean(multi.self_sufficiency[:,:])
                        gains[i,j] = tot_gain
                        multi.clean_production()
                        
        
        print("gains :", gains)
        print("beginning of costs function")
        gains = gains.T
        autoconsommation = autoconsommation.T
        autoproduction = autoproduction.T
        annualized_costs_norm = annualized_costs_norm.T
        
        bat = bat_array / 1000
        gain_net_tot = gains - annualized_costs_norm
        
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, ev in enumerate(ev_arr):
                ax.plot(bat, autoconsommation[i, :], label=f"{ev} charging station(s)")
        ax.set_title('Self-consumption')
        ax.set_xlabel('Battery capacity (kWh)')
        ax.set_ylabel('Self-consumption')
        ax.legend()
        ax.grid(True)
        plt.show()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        for i, ev in enumerate(ev_arr):
                ax2.plot(bat, autoproduction[i, :], label=f"{ev} charging station(s)")
        ax2.set_title('Self-sufficiency')
        ax2.set_xlabel('Battery capacity (kWh)')
        ax2.set_ylabel('Number of charging station')
        ax2.legend()
        ax2.grid(True)
        plt.show()
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        for i, ev in enumerate(ev_arr):
                ax3.plot(bat, gain_net_tot[i, :], label=f"{ev} charging station(s)")

        ax3.set_title('Net gain (euro)')
        ax3.set_xlabel('Battery capacity (kWh)')
        ax3.set_ylabel('number of charging station')
        ax3.legend()
        ax3.grid(True)
        plt.show()
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        for i, ev in enumerate(ev_arr):
                ax4.plot(bat, annualized_costs_norm[i, :], label=f"{ev} charging station(s)")
                
        ax4.set_title('Cost (euro)')
        ax4.set_xlabel('Battery capacity (kWh)')
        ax4.set_ylabel('Number of charging station')
        ax4.legend()
        ax4.grid(True)
        plt.show()
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        for i, ev in enumerate(ev_arr):
                ax5.plot(bat,  gains[i, :], label=f"{ev} charging station(s)")

   
        ax5.set_title('Revenue (euro)')
        ax5.set_xlabel('Battery capacity (kWh)')
        ax5.set_ylabel('Number of charging station')
        ax5.legend()
        ax5.grid(True)
        plt.show()
        

#ev_bat()
         
def change_number_household():
        """Modification of the number of households in the community
        """
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000
                
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        #"EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv'

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [95] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        #enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        #enercom.func_compute_total_production()
        #enercom.save_production()
        #multi = MultiHousehold(params, enercom)
        #multi.run()
        #multi.repartition_elec()
        #multi.compute_metrics()
        #multi.pricing()
        
        enercom_array = []
        
        area_array = np.linspace(20,600, 10)
        #area_array = np.linspace(500,600, 10)
        kWc_array = area_array * pv_params["PV_efficiency"]
        bat_array = np.linspace(0,30000, 10)
        #bat_array = np.linspace(5000,10000, 10)
       
        ################Compute the production
        print("beginning of the production computation")
        for i in range(len(area_array)):
                print("i", i)
                pv_params["PV_area"] = [area_array[i]]
                kWc = kWc_array[i]
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                this_enercom = EnergyCommunity(pv_params)   
                this_enercom.func_compute_total_production()
                enercom_array.append(this_enercom)
                
        #compute the repartition as a fonction of the battery power
        print("beginning of the repartition computation")
        optimal_points = {}
        optimal_gains = {}
        total_consumption = {}
        
        for k in range(1, 25):
                gains = np.zeros((len(bat_array), len(area_array)))
                autoconsommation = np.zeros((len(bat_array), len(area_array)))
                autoproduction = np.zeros((len(bat_array), len(area_array))) 
                annualized_costs_norm = np.zeros((len(bat_array), len(area_array)))
                net_gain_matrix = np.zeros((len(bat_array), len(area_array)))
                consumption = np.zeros((len(bat_array), len(area_array)))
                params["n_households"] = k
                multi = MultiHousehold(params, enercom_array[0])
                multi.run()
                for i in range(len(bat_array)):
                        for j in range(len(enercom_array)):
                                print("i", i)
                                print("j", j)
                                this_enercom = enercom_array[j]
                                kWc = this_enercom.PV_area[0] * this_enercom.PV_efficiency
                                this_enercom.battery_capacity = bat_array[i]
                                multi.enercom = this_enercom
                                multi.production = this_enercom.total_production
                                #print("sum production", np.sum(multi.production[:,0]))
                                multi.repartition_elec()
                                multi.compute_metrics()
                                multi.pricing()
                                cv_coeff = 0
                                if kWc < 5:
                                        cv_coeff = 2.055
                                elif kWc < 36:
                                        cv_coeff = 1.953
                                elif kWc < 100:
                                        cv_coeff = 1.016
                                elif kWc < 250:
                                        cv_coeff = 0.642
                                else : 
                                        cv_coeff = 0.58
                                cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                                tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                                tot_gain += cv_revenue
                                #cost = this_enercom.annualized_investment_cost + 0.05433 * bat_array[i]
                                cost = this_enercom.annualized_investment_cost + 0.03 * bat_array[i]  #300eur/kWh sur 10 ans
                                annualized_costs_norm[i,j] = cost
                                
                                autoconsommation[i, j] = np.mean(multi.self_consumption[:])
                                autoproduction[i, j] = np.mean(multi.self_sufficiency[:,:])
                                gains[i,j] = tot_gain
                                net_gain_matrix[i,j] = tot_gain - cost
                                consumption[i,j] = np.sum(multi.consumption_year[:,:])/3 #sum over 3 years
                                multi.clean_production()
                
                max_indices = np.unravel_index(np.argmax(net_gain_matrix), net_gain_matrix.shape)
                optimal_points[k] = max_indices
                optimal_gains[k] = net_gain_matrix[max_indices]
                total_consumption[k] = consumption[max_indices]
                print("number of households", k)
                print("optimal points", optimal_points)
                print("optimal gains", optimal_gains)
                print("total consumption", total_consumption)
                
        kwc_plot = np.zeros(24)
        bat_plot = np.zeros(24)
        for k in range(1, 25):
                i = optimal_points[k][0] # 
                j = optimal_points[k][1]
                this_bat = bat_array[i]
                this_area = area_array[j]
                kWc = this_area * pv_params["PV_efficiency"]
                this_gain = optimal_gains[k]
                this_consumption = total_consumption[k]
                kwc_plot[k-1] = kWc
                bat_plot[k-1] = this_bat
                print("number of households", k)
                print("optimal battery capacity", this_bat)
                #print("optimal area", this_area)
                print("optimal kWc", kWc)
                print("optimal gain", this_gain)
                print("total consumption", this_consumption)
                
                
        
        plt.plot(kwc_plot)
        plt.show()
        plt.plot(bat_plot)
        plt.show()
        
change_number_household()


def example_with_other_data():
               
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [548], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03
                }
        #"EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv', 'number_ev_charger' : 3
        file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/data/individual+household+electric+power+consumption/household_power_consumption_24.npy"
        consumption_household = np.load(file)
        consumption_household = np.nan_to_num(consumption_household, nan=0)
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]

        params = {
                "n_households": 24,
                "input_directory" : "pv_example_2",
                "output_directory" : "19_may_other_data",
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                
        }
        multi = MultiHousehold(params, enercom)
        for year in range(3):
                multi.total_electric_consumption[:,:,year] = consumption_household
        multi.repartition_elec()
       
        multi.compute_metrics()
        print("production", multi.production_year)
        print("injection", multi.injection_year)
        print("self_consumption", multi.self_consumption)
        #print("total repartition", multi.total_repartition)
        multi.pricing()
        
        cv_coeff = 0
        kWc = pv_params["PV_area"][0] * pv_params["PV_efficiency"]
        if kWc < 5:
                cv_coeff = 2.055
        elif kWc < 36:
                cv_coeff = 1.953
        elif kWc < 100:
                cv_coeff = 1.016
        elif kWc < 250:
                cv_coeff = 0.642
        else : 
                cv_coeff = 0.58
        cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
        print("Annualized revenue from cv : ", cv_revenue)
        cost = multi.annualized_investment_cost  #+ 0.05433*10000
        print("Annualized cost : ", cost)
        tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
        print("Total gain : ", tot_gain)
        tot_gain += cv_revenue
        print("Total gain with cv : ", tot_gain)
        #rev_from_ev = np.mean(multi.total_revenue_from_ev[:])
        #print("Total gain from ev : ", rev_from_ev)
        #print("ev_from_pv", multi.ev_total_from_pv)
        #print("ev_share", multi.ev_share_from_pv)
        #print("ev_conso", multi.ev_charger_tot_conso)

        multi.save_results()
#example_with_other_data()
        
def price_bat_pv_other_var():
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [548], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000
                }
        #"EV_charger" : True, "EV_price" : 0.3, 'EV_file' : 'C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/code/memoire_partage_elec/ev_charging_profile/data_2023_selected.csv', 'number_ev_charger' : 3
        file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/data/individual+household+electric+power+consumption/household_power_consumption_24.npy"
        consumption_household = np.load(file)
        consumption_household = np.nan_to_num(consumption_household, nan=0)
        
        enercom = EnergyCommunity(pv_params)
        #enercom.get_weather_data()
        enercom.func_compute_total_production()
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]

        params = {
                "n_households": 24,
                "input_directory" : "pv_example_2",
                "output_directory" : "19_may_other_data_var",
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,        
        }
        multi = MultiHousehold(params, enercom)
        
        enercom_array = []
        
        area_array = np.linspace(20,600, 10)
        #area_array = np.linspace(500,600, 10)
        kWc_array = area_array * pv_params["PV_efficiency"]
        bat_array = np.linspace(0,30000, 10)
        #bat_array = np.linspace(5000,10000, 10)
       
        ################Compute the production
        print("beginning of the production computation")
        for i in range(len(area_array)):
                print("i", i)
                pv_params["PV_area"] = [area_array[i]]
                kWc = kWc_array[i]
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                this_enercom = EnergyCommunity(pv_params)   
                this_enercom.func_compute_total_production()
                enercom_array.append(this_enercom)
                
        #compute the repartition as a fonction of the battery power
        print("beginning of the repartition computation")
        optimal_points = {}
        optimal_gains = {}
        total_consumption = {}
        
        for k in range(1, 25):
                
                gains = np.zeros((len(bat_array), len(area_array)))
                autoconsommation = np.zeros((len(bat_array), len(area_array)))
                autoproduction = np.zeros((len(bat_array), len(area_array))) 
                annualized_costs_norm = np.zeros((len(bat_array), len(area_array)))
                net_gain_matrix = np.zeros((len(bat_array), len(area_array)))
                consumption = np.zeros((len(bat_array), len(area_array)))
                params["n_households"] = k
                multi = MultiHousehold(params, enercom_array[0])
                for y in range(3):
                        multi.total_electric_consumption[:,:,y] = consumption_household[:,0:k]
                for i in range(len(bat_array)):
                        for j in range(len(enercom_array)):
                                print("i", i)
                                print("j", j)
                                this_enercom = enercom_array[j]
                                kWc = this_enercom.PV_area[0] * this_enercom.PV_efficiency
                                this_enercom.battery_capacity = bat_array[i]
                                multi.enercom = this_enercom
                                multi.production = this_enercom.total_production
                                #print("sum production", np.sum(multi.production[:,0]))
                                multi.repartition_elec()
                                multi.compute_metrics()
                                multi.pricing()
                                cv_coeff = 0
                                if kWc < 5:
                                        cv_coeff = 2.055
                                elif kWc < 36:
                                        cv_coeff = 1.953
                                elif kWc < 100:
                                        cv_coeff = 1.016
                                elif kWc < 250:
                                        cv_coeff = 0.642
                                else : 
                                        cv_coeff = 0.58
                                cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                                tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                                tot_gain += cv_revenue
                                #cost = this_enercom.annualized_investment_cost + 0.05433 * bat_array[i]
                                cost = this_enercom.annualized_investment_cost + 0.03 * bat_array[i]  #300eur/kWh sur 10 ans
                                annualized_costs_norm[i,j] = cost
                                
                                autoconsommation[i, j] = np.mean(multi.self_consumption[:])
                                autoproduction[i, j] = np.mean(multi.self_sufficiency[:,:])
                                gains[i,j] = tot_gain
                                net_gain_matrix[i,j] = tot_gain - cost
                                consumption[i,j] = np.sum(multi.consumption_year[:,:])/3 #sum over 3 years
                                multi.clean_production()
                
                max_indices = np.unravel_index(np.argmax(net_gain_matrix), net_gain_matrix.shape)
                optimal_points[k] = max_indices
                optimal_gains[k] = net_gain_matrix[max_indices]
                total_consumption[k] = consumption[max_indices]
                print("number of households", k)
                print("optimal points", optimal_points)
                print("optimal gains", optimal_gains)
                print("total consumption", total_consumption)
                
        kwc_plot = np.zeros(24)
        bat_plot = np.zeros(24)
        for k in range(1, 25):
                i = optimal_points[k][0] # 
                j = optimal_points[k][1]
                this_bat = bat_array[i]
                this_area = area_array[j]
                kWc = this_area * pv_params["PV_efficiency"]
                this_gain = optimal_gains[k]
                this_consumption = total_consumption[k]
                kwc_plot[k-1] = kWc
                bat_plot[k-1] = this_bat
                print("number of households", k)
                print("optimal battery capacity", this_bat)
                #print("optimal area", this_area)
                print("optimal kWc", kWc)
                print("optimal gain", this_gain)
                print("total consumption", this_consumption)
                
                
        
        plt.plot(kwc_plot)
        plt.show()
        plt.plot(bat_plot)
        plt.show()
                

#price_bat_pv_other_var()
                
def ev_optimum():
        """Cette fonction regarde, pour chaque nombre de households et chaque optimum pv_bat, l'injection disponible qui pourrait 
        etre utilisé pour charger une voiture
        """                     
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [548], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000
                }
        
        pv_bat_dict = {
                1 : (3333,148.35),
                2 : (3333,148.35),
                3 : (6666,148.35),
                4 : (10000,535.71),
                5 : (10000,535.71),
                6 : (13333,535.71),
                7 : (13333,535.71),
                8 : (13333,535.71),
                9 : (13333,535.71),
                10 : (13333,535.71),
                11 : (13333,535.71),
                12 : (16666,535.71),
                13 : (16666,535.71),
                14 : (16666,535.71),
                15 : (16666,535.71),
                16 : (13333,535.71),
                17 : (13333,535.71),
                18 : (13333,535.71),
                19 : (13333,535.71),
                20 : (13333,535.71),
                21 : (13333,535.71),
                22 : (13333,535.71),
                23 : (13333,535.71),
                24 : (13333,535.71)            
        }
                
        input_directory = "pv_example_2"
        output_directory = "exemple_2_21_mai"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [95] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        for n_house in pv_bat_dict.keys():
                print("number of households", n_house)
                params["output_directory"] = output_directory + "_" + str(n_house) + "_households" + "_" + str(pv_bat_dict[n_house][0]) + "_battery_" + str(pv_bat_dict[n_house][1]) + "_area"
                params["n_households"] = n_house
                pv_params["battery_capacity"] = pv_bat_dict[n_house][0]
                pv_params["PV_area"] = [pv_bat_dict[n_house][1]]
                kWc = pv_params["PV_area"][0] * pv_params["PV_efficiency"] 
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                this_enercom = EnergyCommunity(pv_params)
                this_enercom.func_compute_total_production()
                multi = MultiHousehold(params, this_enercom)
                multi.run()
                multi.repartition_elec()
                multi.compute_metrics()
                multi.pricing()
                cv_coeff = 0
                if kWc < 5:
                        cv_coeff = 2.055
                elif kWc < 36:
                        cv_coeff = 1.953
                elif kWc < 100:
                        cv_coeff = 1.016
                elif kWc < 250:
                        cv_coeff = 0.642
                else : 
                        cv_coeff = 0.58
                cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                tot_gain += cv_revenue
                print("Total gain : ", tot_gain)
                multi.save_results()
#ev_optimum()

def ev_optimum_other():
        """Cette fonction regarde, pour chaque nombre de households et chaque optimum pv_bat, l'injection disponible qui pourrait 
        etre utilisé pour charger une voiture
        """                     
        
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_example_2", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [548], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03,
                "battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000
                }
        file = "C:/Users/simva/OneDrive/Documents/1 Master 2/Mémoire/data/individual+household+electric+power+consumption/household_power_consumption_24.npy"
        consumption_household = np.load(file)
        consumption_household = np.nan_to_num(consumption_household, nan=0)
        pv_bat_dict = {
                1 : (3333,148.35),
                2 : (6666,148.35),
                3 : (10000,148.35),
                4 : (23333,535.71),
                5 : (23333,535.71),
                6 : (13333,535.71),
                7 : (23333,535.71),
                8 : (23333,535.71),
                9 : (23333,535.71),
                10 : (23333,535.71),
                11 : (20000,535.71),
                12 : (23333,535.71),
                13 : (23333,535.71),
                14 : (23333,535.71),
                15 : (23333,535.71),
                16 : (16666,535.71),
                17 : (13333,535.71),
                18 : (20000,535.71),
                19 : (13333,535.71),
                20 : (13333,535.71),
                21 : (13333,535.71),
                22 : (13333,535.71),
                23 : (13333,535.71),
                24 : (13333,535.71)            
        }
                
        input_directory = "pv_example_2"
        output_directory = "folder_other_opti/exemple_2_21_mai_other"
        n_households = 24
        cooking_params = ["low", "medium", "medium", "high", "high", "high", "low", "low", "high", "medium", "medium", "medium", "high", "low", "low", "medium", "low", "medium", "high", "high", "high", "low", "medium", "medium" ]
        wh_capacity_params = ["low", "medium", "medium", "high", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "medium", "low", "medium", "medium", "medium", "medium", "high", "low", "low", "medium"]
        n_cold_source_params = [1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2,2,2,2,2,1,1,2]
        wm_frequency_params = ["medium", "medium", "medium", "medium", "high", "medium", "low", "low", "medium", "low", "medium", "medium", "high", "low", "low", "low", "medium", "high", "medium", "high", "high", "low", "low", "medium"]
        have_dryer_params = [False, False, True, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False]
        dryer_type_params = [None, None, "condensation", None, "evacuation", None, None, None, None, None, None, None, "heat_pump", None, None, None, None, None, None, "evacuation", "condensation", None, None, None]
        dryer_frequency_params = [None, None, "medium", None, "medium", None, None, None, None, None, None, None, "low", None, None, None, None, None, None, "medium", "low", None, None, None]
        have_dw_params = [False, True, True, True, True, True, False, False, True, False, True, True, True, False, False, False, False, True, True, True, True, False, False, False]
        dw_frequency_params = [None, "low", "medium", "medium", "high", "high", None, None, "medium", None, "low", "high", "medium", None, None, None, None, "medium", "low", "medium", "low", None, None, None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,9,14,11,13,13,11,13,12,10,11,9,13,15,12,12,12,11,13,14,9,9,14,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        annual_heating_value_params = [95] * n_households
        #PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
        #wh_night = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        wh_night = [False]*n_households
        wh_intelligence_params = True
        #wh_hour_mode = "perfect_knowledge"
        wh_hour_mode = "fixed"
        if wh_hour_mode == "perfect_knowledge":
                wh_multiyears_params = [True]*n_households
        else:
                wh_multiyears_params = [False]*n_households
        
        params = {
                "input_directory": input_directory,
                "output_directory": output_directory,
                "n_households": n_households,
                "cooking_params": cooking_params,
                "wh_usage_params": wh_capacity_params,
                "n_cold_source_params": n_cold_source_params,
                "wm_frequency_params": wm_frequency_params,
                "have_dryer_params": have_dryer_params,
                "dryer_type_params": dryer_type_params,
                "dryer_frequency_params": dryer_frequency_params,
                "have_dw_params": have_dw_params,
                "dw_frequency_params": dw_frequency_params,
                "grid_price_day_params": grid_price_day_params,
                "grid_price_night_params": grid_price_night_params,
                "wh_intelligence_params": wh_intelligence_params,
                "heating_is_elec_params": heating_is_elec_params,
                "T_ext_th_params": T_ext_th_params,
                "T_ext_th_night_params": T_ext_th_night_params,
                "annual_heating_value_params": annual_heating_value_params,
                #"PEB_params": PEB_params,
                "heating_eff_params": heating_eff_params,
                "flat_area_params": flat_area_params,
                "wh_night_params": wh_night,
                "wh_hour_mode": wh_hour_mode,
                "wh_multiyears_params": wh_multiyears_params,
                "wh_intelligence_params" : wh_intelligence_params,
        }
        
        for n_house in pv_bat_dict.keys():
                print("number of households", n_house)
                params["output_directory"] = output_directory + "_" + str(n_house) + "_households" + "_" + str(pv_bat_dict[n_house][0]) + "_battery_" + str(pv_bat_dict[n_house][1]) + "_area"
                params["n_households"] = n_house
                pv_params["battery_capacity"] = pv_bat_dict[n_house][0]
                pv_params["PV_area"] = [pv_bat_dict[n_house][1]]
                kWc = pv_params["PV_area"][0] * pv_params["PV_efficiency"] 
                if kWc <=10:
                        x = -240
                        y = 3700
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=50:
                        x = -3.75
                        y = 1337.5
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                elif kWc <=100:
                        x = -3
                        y = 1300
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc  
                else : 
                        x = -0.66
                        y = 1066.6
                        price_per_kwc = x * kWc + y
                        pv_params["investment_cost"] = price_per_kwc * kWc
                this_enercom = EnergyCommunity(pv_params)
                this_enercom.func_compute_total_production()
                multi = MultiHousehold(params, this_enercom)
                print(multi.n_households)
                for y in range(3):
                        print("elconso", len(multi.total_electric_consumption[:,:,y]))
                        multi.total_electric_consumption[:,:,y] = consumption_household[:,0:n_house]
                #multi.run()
                multi.repartition_elec()
                multi.compute_metrics()
                multi.pricing()
                cv_coeff = 0
                if kWc < 5:
                        cv_coeff = 2.055
                elif kWc < 36:
                        cv_coeff = 1.953
                elif kWc < 100:
                        cv_coeff = 1.016
                elif kWc < 250:
                        cv_coeff = 0.642
                else : 
                        cv_coeff = 0.58
                cv_revenue = np.mean(multi.production_year[:]) * cv_coeff * 65 * 10 /(25 * 1000000)
                tot_gain = np.mean(multi.total_revenue_with_pv[:]) + (np.sum(multi.total_price_without_pv[:,:]) - np.sum(multi.total_price_with_pv[:,:]))/24
                tot_gain += cv_revenue
                print("Total gain : ", tot_gain)
                multi.save_results()
                

        
#ev_optimum_other()      
        
        