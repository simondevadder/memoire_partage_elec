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
    duplex_params = {"input_directory": "intput_data", "output_directory" : "duplex_out", "wh_type" : 'Joules', 
                     "wh_night" : True, "wh_capacity" : 'high', "heating_type" : 'non-electric',
                     "number_cold_source" : 2, "have_washing_machine" : True, "washing_frequency" : 'medium',
                        "have_dryer" : True, "dryer_usage" : 'medium', "dryer_type" : 'condensation',
                        "have_dishwasher" : True, "dishwasher_frequency" : 'high'}
    flat_1_param = {"input_directory": "intput_data", "output_directory" : "flat_1_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'medium',
                        "have_dryer" : False, "have_dishwasher" : True, "dishwasher_frequency" : 'low'}
    flat_2_param = {"input_directory": "intput_data", "output_directory" : "flat_2_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'medium',
                        "have_dryer" : True, "dryer_usage" : 'medium', "dryer_type" : 'condensation',
                        "have_dishwasher" : True, "dishwasher_frequency" : 'low'}
    flat_3_param = {"input_directory": "intput_data", "output_directory" : "flat_3_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : True, "dishwasher_frequency" : 'medium'}
    flat_4_param = {"input_directory": "intput_data", "output_directory" : "flat_4_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : False}
    flat_5_param = {"input_directory": "intput_data", "output_directory" : "flat_5_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : False}
    flat_6_param = {"input_directory": "intput_data", "output_directory" : "flat_6_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : True, "dishwasher_frequency" : 'low'}
    
    flat_7_param = {"input_directory": "intput_data", "output_directory" : "flat_7_out", "wh_type" : 'Joules',
                        "wh_night" : True, "wh_capacity" : 'medium', "heating_type" : 'non-electric',
                        "number_cold_source" : 1, "have_washing_machine" : True, "washing_frequency" : 'low',
                        "have_dryer" : False, "have_dishwasher" : False}
    pv_params = {"input_directory": "directory_data", "weather_file_name":"", "directory_output" :  "pv_out", "n_years" : 3, "begin_year" : 2017, "end_year" : 2019,
                 "n_households" : 8, "key" : "hybrid", "PV_inclination": [40,40], "PV_orientation" : [80,260], "PV_area" : [122.5,103], "PV_efficiency" : 0.182, "PV_module_size": [1.99, 0.99, 0.008],
                 "PV_NOCT" : 43.6, "PV_betacoeff": 0.0034, "PV_Tref" : 25,  }
    duplex = Household(duplex_params)
    flat_1 = Household(flat_1_param)
    flat_2 = Household(flat_2_param)
    flat_3 = Household(flat_3_param)
    flat_4 = Household(flat_4_param)
    flat_5 = Household(flat_5_param)
    flat_6 = Household(flat_6_param)
    flat_7 = Household(flat_7_param)
    community = EnergyCommunity(pv_params)
    
    
    
    