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
                "n_households" : 8, "key" : "hybrid", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.991, 0.0075],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 126792, "estimated_lifetime" : 25, "interest_rate" : 0.03
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
        
example_2()

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
        
        