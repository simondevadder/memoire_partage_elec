"""

Main file, this file contains some examples of how to use the model

"""
import numpy as np
import pandas as pd
from datetime import date
import sys
import os
from matplotlib import pyplot as plt
import seaborn as sns
from energy_community import EnergyCommunity
from household import Household



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
        duplex_params = {"input_directory": "input_data", "output_directory" : "duplex_out", "wh_type" : 'Joules', 
                        "wh_night" : True, "wh_capacity" : 'high', "heating_type" : 'non-electric',
                        "number_cold_source" : 2, "have_washing_machine" : True, "washing_frequency" : 'medium',
                        "have_dryer" : True, "dryer_usage" : 'medium', "dryer_type" : 'condensation',
                        "have_dishwasher" : True, "dishwasher_frequency" : 'high', "grid_price_day" : 0.36, "grid_price_night" : 0.29}
        flat_1_param = {"input_directory": "input_data", "output_directory" : "flat_1_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'medium',
                        "have_dryer" : False, "have_dishwasher" : True, "dishwasher_frequency" : 'low', "grid_price_day" : 0.39, "grid_price_night" : 0.30}
        flat_2_param = {"input_directory": "input_data", "output_directory" : "flat_2_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'medium',
                        "have_dryer" : True, "dryer_usage" : 'medium', "dryer_type" : 'condensation',
                        "have_dishwasher" : True, "dishwasher_frequency" : 'low', "grid_price_day" : 0.39, "grid_price_night" : 0.30}
        flat_3_param = {"input_directory": "input_data", "output_directory" : "flat_3_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : True, "dishwasher_frequency" : 'medium', "grid_price_day" : 0.39, "grid_price_night" : 0.30}
        flat_4_param = {"input_directory": "input_data", "output_directory" : "flat_4_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : False, "grid_price_day" : 0.36, "grid_price_night" : 0.33}
        flat_5_param = {"input_directory": "input_data", "output_directory" : "flat_5_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : False, "grid_price_day" : 0.36, "grid_price_night" : 0.33}
        flat_6_param = {"input_directory": "input_data", "output_directory" : "flat_6_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : True, "dishwasher_frequency" : 'low', "grid_price_day" : 0.36, "grid_price_night" : 0.29}

        flat_7_param = {"input_directory": "input_data", "output_directory" : "flat_7_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : False, "grid_price_day" : 0.36, "grid_price_night" : 0.29}
        pv_params = {"directory_data": "brussels", "weather_file_name":"brussels_50.8444_4.35609_msg-iodc_60_", "directory_output" :  "pv_out", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                        "n_households" : 8, "key" : "hybrid", "PV_inclination": [40], "PV_orientation" : [260], "PV_area" : [77], "PV_efficiency" : 0.16, "PV_module_size": [1.6, 0.99, 0.008],
                        "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25, "sharing_price" : 0.2, "grid_injection_price" : 0.04, "investment_cost" : 18000, "estimated_lifetime" : 25 }
        duplex = Household(duplex_params)
        flat_1 = Household(flat_1_param)
        flat_2 = Household(flat_2_param)
        flat_3 = Household(flat_3_param)
        flat_4 = Household(flat_4_param)
        flat_5 = Household(flat_5_param)
        flat_6 = Household(flat_6_param)
        flat_7 = Household(flat_7_param)
        community = EnergyCommunity(pv_params)
        #community.get_weather_data()
        #community.func_compute_total_production()
        production = pd.read_csv("pv_out/production.csv", header=None)
        production_2017 = production[0].to_numpy()
        production_2018 = production[1].to_numpy()
        production_2019 = production[2].to_numpy()

        duplex.launch_year()
        flat_1.launch_year()
        flat_2.launch_year()
        flat_3.launch_year()
        flat_4.launch_year()
        flat_5.launch_year()
        flat_6.launch_year()
        flat_7.launch_year()
        total_conso_2017 = np.zeros((35040, 8))
        total_conso_2018 = np.zeros((35040, 8))
        total_conso_2019 = np.zeros((35040, 8))
        
        total_conso_2017[:, 0] = duplex.total_consumption[:,0]
        total_conso_2018[:, 0] = duplex.total_consumption[:,1]
        total_conso_2019[:, 0] = duplex.total_consumption[:,2]
        total_conso_2017[:, 1] = flat_1.total_consumption[:,0]
        total_conso_2018[:, 1] = flat_1.total_consumption[:,1]
        total_conso_2019[:, 1] = flat_1.total_consumption[:,2]
        total_conso_2017[:, 2] = flat_2.total_consumption[:,0]
        total_conso_2018[:, 2] = flat_2.total_consumption[:,1]
        total_conso_2019[:, 2] = flat_2.total_consumption[:,2]
        total_conso_2017[:, 3] = flat_3.total_consumption[:,0]
        total_conso_2018[:, 3] = flat_3.total_consumption[:,1]
        total_conso_2019[:, 3] = flat_3.total_consumption[:,2]
        total_conso_2017[:, 4] = flat_4.total_consumption[:,0]
        total_conso_2018[:, 4] = flat_4.total_consumption[:,1]
        total_conso_2019[:, 4] = flat_4.total_consumption[:,2]
        total_conso_2017[:, 5] = flat_5.total_consumption[:,0]
        total_conso_2018[:, 5] = flat_5.total_consumption[:,1]
        total_conso_2019[:, 5] = flat_5.total_consumption[:,2]
        total_conso_2017[:, 6] = flat_6.total_consumption[:,0]
        total_conso_2018[:, 6] = flat_6.total_consumption[:,1]
        total_conso_2019[:, 6] = flat_6.total_consumption[:,2]
        total_conso_2017[:, 7] = flat_7.total_consumption[:,0]
        total_conso_2018[:, 7] = flat_7.total_consumption[:,1]
        total_conso_2019[:, 7] = flat_7.total_consumption[:,2]
        
        repartition_2017 = np.zeros((35040, 8))
        repartition_2018 = np.zeros((35040, 8))
        repartition_2019 = np.zeros((35040, 8))
        
        from_grid_2017 = np.zeros((35040, 8))
        from_grid_2018 = np.zeros((35040, 8))
        from_grid_2019 = np.zeros((35040, 8))
        
        injection_2017 = np.zeros((35040))
        injection_2018 = np.zeros((35040))
        injection_2019 = np.zeros((35040))
        
        for i in range(35040):
                consumption_2017 = total_conso_2017[i]
                prod_2017 = production_2017[i//4]
                repartition_2017[i], from_grid_2017[i], injection_2017[i] = community.func_repartition(consumption_2017, prod_2017)
                consumption_2018 = total_conso_2018[i]
                prod_2018 = production_2018[i//4]
                repartition_2018[i], from_grid_2018[i], injection_2018[i] = community.func_repartition(consumption_2018, prod_2018)
                consumption_2019 = total_conso_2019[i]
                prod_2019 = production_2019[i//4]
                repartition_2019[i], from_grid_2019[i], injection_2019[i] = community.func_repartition(consumption_2019, prod_2019)
                
                
        
        if not os.path.exists("total_output"):
            os.makedirs("total_output")
        
        np.savetxt("total_output/total_conso_2017.csv", total_conso_2017, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/total_conso_2018.csv", total_conso_2018, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/total_conso_2019.csv", total_conso_2019, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/repartition_2017.csv", repartition_2017, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/repartition_2018.csv", repartition_2018, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/repartition_2019.csv", repartition_2019, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/from_grid_2017.csv", from_grid_2017, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/from_grid_2018.csv", from_grid_2018, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/from_grid_2019.csv", from_grid_2019, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/injection_2017.csv", injection_2017, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/injection_2018.csv", injection_2018, delimiter=',', fmt="%.1f")
        np.savetxt("total_output/injection_2019.csv", injection_2019, delimiter=',', fmt="%.1f")
        
        #########################################################################################
        # Compute the total gain for each year
        #########################################################################################
        repartition_total_2017 = np.sum(repartition_2017, axis=0)
        repartition_total_2018 = np.sum(repartition_2018, axis=0)
        repartition_total_2019 = np.sum(repartition_2019, axis=0)
        
        from_grid_total_2017 = np.sum(from_grid_2017, axis=0)
        from_grid_total_2018 = np.sum(from_grid_2018, axis=0)
        from_grid_total_2019 = np.sum(from_grid_2019, axis=0)
        
        injection_total_2017 = np.sum(injection_2017)
        injection_total_2018 = np.sum(injection_2018)
        injection_total_2019 = np.sum(injection_2019)
        
        paid_to_PV_2017 = repartition_total_2017 * community.sharing_price/4000  # in €/kWh
        paid_to_PV_2018 = repartition_total_2018 * community.sharing_price/4000  # in €/kWh
        paid_to_PV_2019 = repartition_total_2019 * community.sharing_price/4000  # in €/kWh
        
        paid_from_grid_2017 = injection_total_2017 * community.grid_injection_price/4000  # in €/kWh
        paid_from_grid_2018 = injection_total_2018 * community.grid_injection_price/4000  # in €/kWh
        paid_from_grid_2019 = injection_total_2019 * community.grid_injection_price/4000  # in €/kWh
        
        without_sharing_2017 = np.sum(production_2017) * community.grid_injection_price/1000
        without_sharing_2018 = np.sum(production_2018) * community.grid_injection_price/1000
        without_sharing_2019 = np.sum(production_2019) * community.grid_injection_price/1000
        total_production_2017 = np.sum(production_2017)/1000
        total_production_2018 = np.sum(production_2018)/1000
        total_production_2019 = np.sum(production_2019)/1000
        print("Total production in kWh : ", total_production_2017, ", ", total_production_2018, ", ", total_production_2019)
  
        total_paid_2017 = np.sum(paid_to_PV_2017) + paid_from_grid_2017
        total_paid_2018 = np.sum(paid_to_PV_2018) + paid_from_grid_2018
        total_paid_2019 = np.sum(paid_to_PV_2019) + paid_from_grid_2019
        
        community.compute_gc_gain()
        community.compute_minimal_revenue()
        print("Total paid : ", total_paid_2017, ", ", total_paid_2018, ", ", total_paid_2019)
        print("Total gain without sharing : ", without_sharing_2017, ", ", without_sharing_2018, ", ", without_sharing_2019)
        print("minimum return : ", community.minimal_revenue)
        print("Total gain from gc : ", community.gc_revenue)
        
        

#example_1()
                
def example_1_pricing_evaluation():
        price_grid_day = [0.36,0.39,0.39,0.39,0.36,0.36,0.36, 0.36]  # in €/Wh
        price_grid_day = np.array(price_grid_day)/1000
        
        price_grid_night = [0.29,0.30,0.30,0.30,0.33,0.33,0.29, 0.29]  # in €/Wh
        price_grid_night = np.array(price_grid_night)/1000
        
        price_PV_to_grid = 0.04/1000  # in €/Wh
        
        price_PV_to_home = 0.2/1000  # in €/Wh
        
        consumption_2017 = np.loadtxt("total_output/total_conso_2017.csv", delimiter=',')
        consumption_2018 = np.loadtxt("total_output/total_conso_2018.csv", delimiter=',')
        consumption_2019 = np.loadtxt("total_output/total_conso_2019.csv", delimiter=',')
        repartition_2017 = np.loadtxt("total_output/repartition_2017.csv", delimiter=',')
        repartition_2018 = np.loadtxt("total_output/repartition_2018.csv", delimiter=',')
        repartition_2019 = np.loadtxt("total_output/repartition_2019.csv", delimiter=',')
        from_grid_2017 = np.loadtxt("total_output/from_grid_2017.csv", delimiter=',')
        from_grid_2018 = np.loadtxt("total_output/from_grid_2018.csv", delimiter=',')
        from_grid_2019 = np.loadtxt("total_output/from_grid_2019.csv", delimiter=',')
        injection_2017 = np.loadtxt("total_output/injection_2017.csv", delimiter=',')
        injection_2018 = np.loadtxt("total_output/injection_2018.csv", delimiter=',')
        injection_2019 = np.loadtxt("total_output/injection_2019.csv", delimiter=',')
        production_2017 = np.loadtxt("pv_out/production.csv", delimiter=',')[:,0]
        production_2018 = np.loadtxt("pv_out/production.csv", delimiter=',')[:,1]
        production_2019 = np.loadtxt("pv_out/production.csv", delimiter=',')[:,2]
        
        gain_without_sharing_2017 = np.sum(production_2017) * price_PV_to_grid
        gain_without_sharing_2018 = np.sum(production_2018) * price_PV_to_grid
        gain_without_sharing_2019 = np.sum(production_2019) * price_PV_to_grid
        
        tot_gain_without_sharing = np.zeros((3))
        tot_gain_without_sharing[0] = gain_without_sharing_2017
        tot_gain_without_sharing[1] = gain_without_sharing_2018
        tot_gain_without_sharing[2] = gain_without_sharing_2019
        mean_gain_without_sharing = np.mean(tot_gain_without_sharing)
        #print("production : ", np.sum(production_2017))
        
        tot_conso_day = np.zeros((8, 3))
        tot_conso_night = np.zeros((8, 3))
        tot_cost_grid_without_sharing = np.zeros((8, 3))
        mean_costs_grid_without_sharing = np.zeros((8))
        
        tot_conso_day_sharing = np.zeros((8, 3))
        tot_conso_night_sharing = np.zeros((8, 3))
        total_cost_grid_sharing = np.zeros((8, 3))
        mean_costs_grid_sharing = np.zeros((8))
        tot_conso_grid = np.zeros((8, 3))
                
        
        for i in range(35040):
                quart_sem = i % 672
                quart_day = i % 96
                if quart_sem >=478 : 
                        tot_conso_night[:, 0] += consumption_2017[i]/4
                        tot_conso_night[:, 1] += consumption_2018[i]/4
                        tot_conso_night[:, 2] += consumption_2019[i]/4
                        
                        tot_conso_night_sharing[:, 0] += from_grid_2017[i] /4
                        tot_conso_night_sharing[:, 1] += from_grid_2018[i] /4
                        tot_conso_night_sharing[:, 2] += from_grid_2019[i]/4
                elif quart_day <= 28 or quart_day >= 88 :
                        tot_conso_night[:, 0] += consumption_2017[i]/4
                        tot_conso_night[:, 1] += consumption_2018[i]/4
                        tot_conso_night[:, 2] += consumption_2019[i]/4
                        tot_conso_night_sharing[:, 0] += from_grid_2017[i]/4
                        tot_conso_night_sharing[:, 1] += from_grid_2018[i]/4
                        tot_conso_night_sharing[:, 2] += from_grid_2019[i]/4
                else : 
                        tot_conso_day[:, 0] += consumption_2017[i]/4
                        tot_conso_day[:, 1] += consumption_2018[i]/4
                        tot_conso_day[:, 2] += consumption_2019[i]/4
                        
                        tot_conso_day_sharing[:, 0] += from_grid_2017[i]/4
                        tot_conso_day_sharing[:, 1] += from_grid_2018[i]/4
                        tot_conso_day_sharing[:, 2] += from_grid_2019[i]/4
        
                
        for i in range(8):
                tot_cost_grid_without_sharing[i, 0] = tot_conso_day[i, 0] * price_grid_day[i] + tot_conso_night[i, 0] * price_grid_night[i]
                tot_cost_grid_without_sharing[i, 1] = tot_conso_day[i, 1] * price_grid_day[i] + tot_conso_night[i, 1] * price_grid_night[i]
                tot_cost_grid_without_sharing[i, 2] = tot_conso_day[i, 2] * price_grid_day[i] + tot_conso_night[i, 2] * price_grid_night[i]
                mean_costs_grid_without_sharing[i] = np.mean(tot_cost_grid_without_sharing[i])
                
                total_cost_grid_sharing[i, 0] = tot_conso_day_sharing[i, 0] * price_grid_day[i]+ tot_conso_night_sharing[i, 0] * price_grid_night[i]
                total_cost_grid_sharing[i, 1] = tot_conso_day_sharing[i, 1] * price_grid_day[i] + tot_conso_night_sharing[i, 1] * price_grid_night[i]
                total_cost_grid_sharing[i, 2] = tot_conso_day_sharing[i, 2] * price_grid_day[i] + tot_conso_night_sharing[i, 2] * price_grid_night[i]
                tot_conso_grid[i, 0] = tot_conso_day_sharing[i, 0] + tot_conso_night_sharing[i, 0]
                tot_conso_grid[i, 1] = tot_conso_day_sharing[i, 1] + tot_conso_night_sharing[i, 1]
                tot_conso_grid[i, 2] = tot_conso_day_sharing[i, 2] + tot_conso_night_sharing[i, 2]
                mean_costs_grid_sharing[i] = np.mean(total_cost_grid_sharing[i])
                
        print("total cost without sharing : ", tot_cost_grid_without_sharing)
        
        ################################################################################################"
        # gain with sharing
        ################################################################################################
         
        cost_shared_elec = np.zeros((8, 3))
        cost_shared_elec[:, 0] = np.sum(repartition_2017, axis=0) * price_PV_to_home/4
        cost_shared_elec[:, 1] = np.sum(repartition_2018, axis=0) * price_PV_to_home/4
        cost_shared_elec[:, 2] = np.sum(repartition_2019, axis=0) * price_PV_to_home/4
        cost_shared_elec_mean = np.mean(cost_shared_elec, axis=1)
        
        total_cost_overall = np.zeros((8, 3))
        total_cost_overall[:, 0] = total_cost_grid_sharing[:, 0] + cost_shared_elec[:, 0]
        total_cost_overall[:, 1] = total_cost_grid_sharing[:, 1] + cost_shared_elec[:, 1]
        total_cost_overall[:, 2] = total_cost_grid_sharing[:, 2] + cost_shared_elec[:, 2]
        print("total cost overall : ", total_cost_overall)
        
        mean_cost_overall = np.mean(total_cost_overall, axis=1)
        
        
        
        total_gain_from_sharing = np.zeros((3))
        total_gain_from_sharing[0] = np.sum(cost_shared_elec[:, 0])
        total_gain_from_sharing[1] = np.sum(cost_shared_elec[:, 1])
        total_gain_from_sharing[2] = np.sum(cost_shared_elec[:, 2]) 
        mean_gain_from_sharing = np.mean(total_gain_from_sharing)
        
        total_gain_from_injection= np.zeros((3))
        total_gain_from_injection[0] = np.sum(injection_2017) * price_PV_to_grid/4
        total_gain_from_injection[1] = np.sum(injection_2018) * price_PV_to_grid/4
        total_gain_from_injection[2] = np.sum(injection_2019) * price_PV_to_grid/4
        mean_gain_from_injection = np.mean(total_gain_from_injection)
        
        total_gain_pv = np.zeros((3))
        total_gain_pv[0] = total_gain_from_sharing[0] + total_gain_from_injection[0]
        total_gain_pv[1] = total_gain_from_sharing[1] + total_gain_from_injection[1]
        total_gain_pv[2] = total_gain_from_sharing[2] + total_gain_from_injection[2]
        
        mean_gain_pv = np.mean(total_gain_pv)
        
        proportion_from_pv = np.zeros((8, 3))
        proportion_from_pv[:,0] = np.sum(repartition_2017, axis=0) / np.sum(consumption_2017, axis=0)
        proportion_from_pv[:,1] = np.sum(repartition_2018, axis=0) / np.sum(consumption_2018, axis=0)
        proportion_from_pv[:,2] = np.sum(repartition_2019, axis=0) / np.sum(consumption_2019, axis=0)
        mean_proportion_from_pv = np.mean(proportion_from_pv, axis=1)
        print("taux d'auto production : ",mean_proportion_from_pv)
        
        bar_graph_data_mean_grid = np.zeros((8))
        bar_graph_data_mean_sharing = np.zeros((8))
        
        for i in range(8):
                bar_graph_data_mean_grid[i] = mean_costs_grid_without_sharing[i]
                bar_graph_data_mean_sharing[i] = mean_cost_overall[i]+10.11
        
        print("Mean cost without sharing : ", bar_graph_data_mean_grid)
        print("Mean cost with sharing : ", bar_graph_data_mean_sharing)
                
        
        name = ["duplex", "flat_1", "flat_2", "flat_3", "flat_4", "flat_5", "flat_6", "flat_7"]
        x = np.arange(len(name))
        width_bar = 0.4  # Largeur des barres
        # Création des barres
        plt.bar(x - width_bar/2, bar_graph_data_mean_grid, width_bar, label='Without electricity sharing', color='blue')
        plt.bar(x + width_bar/2, bar_graph_data_mean_sharing, width_bar, label='With electricity sharing', color='orange')
        plt.xlabel('Household')
        plt.ylabel('Cost [€/year]')
        plt.title('Cost of electricity for each household')
        plt.xticks(x, name, rotation=45)
        plt.legend()
        
        plt.show()
        
        bar_plot_investor_gain = np.zeros((3))
        bar_plot_investor_gain[1] = mean_gain_without_sharing
        bar_plot_investor_gain[2] = mean_gain_pv
        bar_plot_investor_gain[0] = 298.52
        
        print("Mean gain without sharing : ", mean_gain_without_sharing)
        print("Mean gain with sharing : ", mean_gain_pv)
        bar_plot_investor_name = ["Without sharing", "With sharing", "Minimal return needed"]
        x = np.arange(len(bar_plot_investor_name))
        plt.bar(x, bar_plot_investor_gain, width_bar, color='blue')
        plt.ylabel('€/year') 
        plt.show()
        
        
        ##############################################################"
        # Evaluation of the self consumption, and the injection into the grid
        ##############################################################
        self_consumption = np.zeros((3))
        self_injection = np.zeros((3))
        self_injection[0] = np.sum(injection_2017)/4
        self_injection[1] = np.sum(injection_2018)/4
        self_injection[2] = np.sum(injection_2019)/4
        production_tot = np.zeros((3))
        production_tot[0] = np.sum(production_2017)
        production_tot[1] = np.sum(production_2018)
        production_tot[2] = np.sum(production_2019)
        for i in range(3) : 
                self_consumption[i] = (production_tot[i] - self_injection[i])/production_tot[i]
                
        print("Self consumption : ", self_consumption)
        print("Self injection : ", self_injection)
        print("Production : ", production_tot)
        

        
        
        
        
        
example_1_pricing_evaluation()      

def test_2():
        
        consumption_2019 = np.loadtxt("total_output/total_conso_2019.csv", delimiter=',')
        repartition_2019 = np.loadtxt("total_output/repartition_2019.csv", delimiter=',')
        
        consumption_duplex = consumption_2019[:, 0]
        repartiton_duplex = repartition_2019[:, 0]
        x = np.linspace(0, 48,192)
        plt.plot(x, consumption_duplex[17376:17568], label='Consumption')
        plt.plot(x, repartiton_duplex[17376:17568], label='Repartition')
        plt.legend()
        plt.ylabel('W')
        plt.xlabel('Hour')
        plt.show()
#test_2()

    
    
    
    