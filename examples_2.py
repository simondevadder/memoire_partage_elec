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
                "n_households" : 8, "key" : "prorata", "PV_inclination": [20], "PV_orientation" : [200], "PV_area" : [320], "PV_efficiency" : 0.22, "PV_module_size": [1.6, 0.99, 0.008],
                "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 90000, "estimated_lifetime" : 25, "interest_rate" : 0.03
                }
        
        #"battery": True, "battery_capacity": 10000, "battery_efficiency": 0.9, "battery_charging_power": 5000, "battery_discharging_power": 5000,
        #"EV_charger" : True, "EV_price" : 0.45
        

        input_directory = "pv_example_2"
        output_directory = "example_2"
        n_households = 24
        cooking_params = ["high", "medium", "low", "low", "medium", "low", "high", "medium", "high", "medium", "low", "low", "medium", "low", "high", "medium", "high", "medium", "high", "medium", "low", "low", "medium", "low" ]
        wh_capacity_params = ["low", "medium", "medium", "medium", "high", "medium", "medium", "medium", "low", "medium", "medium", "low", "low", "medium", "medium", "medium", "high", "medium", "low", "medium", "low", "medium", "high", "medium"]
        n_cold_source_params = [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2,1,1,1,1,2,1,2,1]
        wm_frequency_params = ["medium", "medium", "medium", "low", "low", "low", "low", "low", "medium", "high", "medium", "low", "low", "high", "low", "medium", "medium", "high", "medium", "low", "low", "low", "low", "high"]
        have_dryer_params = [True, False, True, False, False, False, False, False, True, False, True, False, False, False, False, False, True, False, True, False, False, False, True, False]
        dryer_type_params = [None, None, "condensation", None, None, None, None, None, "evacuation", None, "heat-pump", None, None, None, None, None, "heat-pump", None, "evacuation", None, None, None, "condensation", None]
        dryer_frequency_params = [None, None, "medium", None, None, None, None, None, "low", None, "medium", None, None, None, None, None, "medium", None, "low", None, None, None, "medium", None]
        have_dw_params = [True, True, True, True, False, False, True, False, True, True, True, True, True, False, False, False, False, False, True, True, True, True, False, False, True, False]
        dw_frequency_params = ["medium", "low", "medium", "medium", None, None, "low", None, "medium", "medium", "low", "high", "medium", "high", None, None, None, None, None, "medium", "low", "medium", "low", None, None, "low", None]
        grid_price_day_params=[0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36,0.36,0.39,0.39,0.39,0.36,0.36,0.36,0.36]
        grid_price_night_params=[0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29,0.30,0.30,0.30,0.33,0.33,0.29,0.29,0.29]
        heating_is_elec_params = [True]*n_households
        T_ext_th_params = [12,8,14,11,13,13,11,14,12,10,11,9,13,15,12,12,12,11,13,15,9,8,16,12]
        T_ext_th_night_params = [7,5,9,9,5,7,6,8,7,8,7,6,5,9,10,7,7,6,8,8,4,5,10,7]
        PEB_params = ["A","A", "A", "B", "A", "B", "A", "B", "B","B", "A", "B", "A", "A", "B", "B", "A","B", "A", "A", "A","B", "A","B"]
        heating_eff_params = [2.3]*n_households
        
        flat_area_params = [60,100,120,150,250,120,60,80,100,80,120,150,250,66,100,75,110,120,120,150,250,66,80,90]
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
        
        