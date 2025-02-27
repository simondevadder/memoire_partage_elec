"""
Master thesis :  electricity sharing in a multi-unit building

This file contains the class definition of the household, the goal of this class is to simulate the electric consumption of an household
The consumption is separated into several categories, that have a load curve associated to them.
The normalized load curve of certain categories (cookig, laundry, etc) represents the probability that the activity 
it currently achieved. 

To modelize the variablity of the consumption, at each time step, we will compute whether each activity is carried out or not,
and if it is, it will give out a consumption value. Each activity has a minimum and maximum duration, and a minimum and maximum power consumption.

page 37 du documents : 
    thermique : 47.3%, dont 72% pour l'eau chaude
    froid : 11.2%
    audiovisuel, lavage, cuisine : 6 à 7% chacun
    autres : 10% environ
    
    /!\ EV à prendre en compte (conso X2)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import datetime

class Household:
    def __init__(self, params):
        """

        Args:
            params (dictionary): a dictionary containing the parameters of the household, must contain the following
                - input_directory (str): the directory where the input data is stored
                - output_directory (str): the directory where the output data will be stored
                - wh_type (str): the type of water heater, can be 'Joules', 'thermodynamic' or 'non-electric'
                - wh_night (bool): True if the water heater is only used at night, False otherwise (the water heater is used during the day)
                - wh_capacity (str): the capacity of the water heater 'low' for <149l, 'medium' for 150<=c<201l, 'high' for >201l, -1 if the capacity is unknown
                - heating_type (str): the type of heating, can be 'non-electric', 'only-electric', 'mixed' : 
                                        non-electric : heating is not electric
                                        only-electric : heating is electric
                                        mixed : electricity is used as additional heating source (bathroom, etc), not the main source
                                        if not specified, the type of heating will be randomly chosen
                - PEB (str): the PEB value of the household, can be 'A', 'B', 'C', 'D', 'E', 'F', 'G'
                - heating_efficiency (float): the efficiency or COP of the heating system, default is 1 
                - Appartement_area (int): the area of the flat in m², -1 if the area is unknown
                - T_ext_threshold (float): the threshold outdoor temperature for the heating to be turned on, default is 15°C 
                - number_cold_sources (int): the number of cold sources in the household (frige, freezer, etc), -1 if the number is unknown
                - have_washing_machine (bool): True if the household has a washing machine, False otherwise
                - washing_frequency (str): the frequency of washing, can be 'low', 'medium' or 'high', -1 if the frequency is unknown
                                             - low : up to 2 times a week
                                            - medium : between 3 and 5 times a week
                                            - high : higher than 6 times a week
                - have_dryer (bool): True if the household has a dryer, False otherwise
                - dryer_type (str): the type of dryer, can be 'heat-pump', 'condensation' or 'evacuation', -1 if the type is unknown
                - dryer_usage (str) : the frequency of the dryer, can be 'low', 'medium' or 'high', -1 if the frequency is unknown
                                        - low : up to 2 times a week
                                        - medium : between 3 and 5 times a week
                                        - high : higher than 6 times a week
                - have_dishwasher (bool): True if the household has a dishwasher, False otherwise
                - dishwasher_frequency (str): the frequency of the dishwasher, can be 'low', 'medium' or 'high', -1 if the frequency is unknown
                                                - low : up to 3 times a week
                                                - medium : between 4 and 6 times a week
                                                - high : higher than 7 times a week
                
                
        Other parameters are set to default values, and can be changed later on
            time (int): the number of time step since the beginning of the simulation, the time step is 15 minutes
            hour(float): the hour of the day (sometime used for probability computation)
            day (int): the day of the year (from 1 to 365)
            consumption (np.array): the consumption of the household, of size (35040, 1), 35 040 is the number of time step in a year, 1 is the number of columns
                        the first columns represents the total consumption, the other columns represent the consumption of each appliance
            normalized_load (pd.DataFrame): a dataframe containing the normalized load profile of each activity, using the ademe load profile
            self.is_weekend (bool): True if the day is a weekend, False otherwise
            self.is_weekday (bool): True if the day is a weekday, False otherwise
            
            is_cooking (bool): True if the cooking is on, False otherwise
            time_cooking (int): the number of time step since the cooking began
            time_not_cooking (int): the number of time step since the last time cooking
            
            
        """
        try :
            self.input_directory = params['input_directory']
        except : 
            ValueError("Please provide an input directory")
        self.output_directory = params.get('output_directory', 'no_name_output')
        self.time = 0
        self.hour = 0
        self.day = 1
        self.consumption = np.zeros((35040))  # To be changed, 35 040 is the number of time step in a year, 1 is the number of columns
        self.cooking = np.zeros((35040))
        self.wh = np.zeros((35040))
        self.cold = np.zeros((35040))
        self.washing_usage = np.zeros((35040))
        self.other_power = np.zeros((35040))
        #print(self.consumption.shape)
        #self.normalized_load = pd.read_pickle(self.input_directory + '/Graph_CC_An2_V1_normalized.pkl')
        
        self.is_cooking = False
        self.time_cooking = 0
        self.time_not_cooking = 0
        
        self.wh_type = params.get('wh_type', 'Joules')
        self.wh_is_electric = True
        if self.wh_type == 'non-electric':
            self.wh_is_electric = False
        self.wh_night = params.get('wh_night', True)
        self.wh_capacity = params.get('wh_capacity', -1)
        if self.wh_capacity == -1:
            r = np.random.rand()
            if r < 0.47:
                self.wh_capacity = 'medium'
            elif r < 0.85:
                self.wh_capacity = 'high'
            else:
                self.wh_capacity = 'low'
                
        self.heating_is_elec = True
        self.heating_type = params.get('heating_type', 'not_specified')
        if self.heating_type == 'not_specified':
            r = np.random.rand()
            if r < 0.33:
                self.heating_type = 'non-electric'
            elif r<0.66:
                self.heating_type = 'only-electric'
            else:
                self.heating_type = 'mixed'
        if self.heating_type == 'non-electric':
            self.heating_is_elec = False 
        self.temperature_array = self.load_temperature_data() 
        self.n_year_temp_data = len(self.temperature_array[0])
        self.T_ext_threshold = params.get("T_ext_threshold", 15)
        self.load_heating = np.zeros((35040, self.n_year_temp_data))
        self.total_consumption = np.zeros((35040, self.n_year_temp_data)) 

        try :
            self.peb = params['PEB']
        except:
            ValueError("Please provide a PEB value. If not known, please provide an estimation.")
        if self.peb == 'A':
            self.annual_heating_value_m2 = np.random.randint(25, 46)
        elif self.peb == 'B':
            self.annual_heating_value_m2 = np.random.randint(46, 96)
        elif self.peb == 'C':
            self.annual_heating_value_m2 = np.random.randint(96, 151)
        elif self.peb == 'D':
            self.annual_heating_value_m2 = np.random.randint(151, 211)
        elif self.peb == 'E':
            self.annual_heating_value_m2 = np.random.randint(211, 276)
        elif self.peb == 'F':
            self.annual_heating_value_m2 = np.random.randint(276, 346)
        elif self.peb == 'G':
            self.annual_heating_value_m2 = np.random.randint(346, 450)
        else:
            ValueError("PEB value not recognized")
        self.flat_area = params.get('Appartement_area', -1)
        if self.flat_area == -1:
            r = np.random.rand()
            if r < 0.1:
                self.flat_area = np.random.randint(30,52 )  # mean = 41
            elif r < 0.39:
                self.flat_area = np.random.randint(52, 74)  # mean  = 63
            elif r <0.8:
                self.flat_area = np.random.randint(74, 104)  # mean = 89
            elif r<0.98:
                self.flat_area = np.random.randint(100, 124)  # mean = 112
            elif r<0.99:
                self.flat_area = np.random.randint(124, 162)  # mean = 143
            else:
                self.flat_area = np.random.randint(162, 216)  # mean = 189
        
        self.heating_efficiency = params.get('heating_efficiency', 1)
        self.power_heating = self.flat_area * self.annual_heating_value_m2 *1000 / (self.heating_efficiency * 4198.4)  # Total energy / equivalent heating hours (mean)
            
        
        self.number_cold_sources = params.get('number_cold_sources', -1)
        if self.number_cold_sources == -1:
            if np.random.rand() < 0.8:
                self.number_cold_sources = 2
            else:
                self.number_cold_sources = 1
        if self.number_cold_sources > 0:
            self.cold_power = np.zeros(self.number_cold_sources)
            for i in range (self.number_cold_sources):
                if i ==1:
                    if np.random.rand() < 0.045:
                        self.cold_power[i] = 85  #750kWh/year
                    else:
                        self.cold_power[i] = np.random.randint(22, 57)     #between 200 and 500 kWh/year
                else:
                    if np.random.rand() < 0.37:  # 37% chances of having a big freezer
                        self.cold_power[i] = np.random.randint(34, 80)  #between 300 and 700 kWh/year
                    else:
                        self.cold_power[i] = np.random.randint(11, 34) #between 100 and 300 kWh/year
        
        self.have_washing_machine = params.get('have_washing_machine', True)
        self.washing_frequency = params.get('washing_frequency', -1)
        if self.washing_frequency == -1:
            r = np.random.rand()
            if r < 0.28:  #up to 2 times a week
                self.washing_frequency = "low"
            elif r < 0.47:  #between 3 and 5 times a week
                self.washing_frequency = "medium"
            else:  #between 6 and 14 times a week
                self.washing_frequency = "high"
        self.washing_intelligence = params.get('washing_intelligence', False)
        self.have_dryer = params.get('have_dryer', -1)
        if self.have_dryer == -1:
            if np.random.rand() < 0.31:
                self.have_dryer = True
            else:
                self.have_dryer = False
        if self.have_dryer:
            self.dryer_type = params.get('dryer_type', -1)
            self.dryer_intelligence = params.get('dryer_intelligence', False)
            if self.dryer_type == -1:
                r = np.random.rand()
                if r<0.15:
                    self.dryer_type = 'heat-pump'
                elif r<0.73 : 
                    self.dryer_type = 'condensation'
                else:
                    self.dryer_type = 'evacuation'
            if self.dryer_type == 'heat-pump':
                self.dryer_power = 416  # 416 W, means energy = 860Wh/cycle for cycle dur  = 124min
            elif self.dryer_type == 'condensation':
                self.dryer_power = 1112  # 1112 W, means energy = 1632Wh/cycle for cycle dur  = 88min
            else : 
                self.dryer_power = 1215  # 1215 W, means energy = 2067Wh/cycle for cycle dur  = 102min
            self.dryer_usage = params.get('dryer_usage', -1)
            if self.dryer_usage == -1:
                r = np.random.rand()
                if r< 0.4516 : # 14/31 is low
                    self.dryer_usage = 'low'  # low means 2 cycle or less per week
                elif r<0.742:  # 9/31 is medium
                    self.dryer_usage = 'medium'  # medium means between 3 and 5 cycles per week
                else:  #8/31 is high
                    self.dryer_usage = 'high' # high means more than 6 cycles per week (up to 9 in this model)
        self.have_dishwasher = params.get('have_dishwasher', -1)
        if self.have_dishwasher == -1:
            if np.random.rand() < 0.71:
                self.have_dishwasher = True
            else:
                self.have_dishwasher = False
        self.dishwasher_frequency = params.get('dishwasher_frequency', -1)
        if self.dishwasher_frequency == -1:
            r = np.random.rand()
            if r < 0.4:  # 2 or less cycle per week  29/72
                self.dishwasher_frequency = "low"
            elif r < 0.79:  #between 3 and 4 cycles per week  28/72
                self.dishwasher_frequency = "medium"
            else:  # more than 5 cycles a week 15/72, up to 10 
                self.dishwasher_frequency = "high"
        self.dishwasher_intelligence = params.get('dishwasher_intelligence', False)
        
        self.other_random_param = np.random.rand()
        
        
        
            
                
    def load_temperature_data(self):
        df = pd.read_csv(self.output_directory + '/temperature.csv',header=None, sep=',', encoding='ISO-8859-1', decimal='.')
        return df.values
    def create_normalized_load_profile_file(self, kind):
        """This function creates a file with the normalized load profile of each activity, using the ademe load profile
        
        Args:
            kind (str): the kind of file that will be created (csv, pickle, excel)
        """
        df = pd.read_csv(self.input_directory + '/Graph_CC_An2_V1.csv', header=0, sep=';', encoding='ISO-8859-1', decimal=',')
        #print(df.columns)
        df['Période_Poste'] = df['Période'] + ' - ' + df['Poste']
        df = df.drop(columns=['Période', 'Poste'])
        df = df.set_index('Période_Poste')
        #print(df.head())
        #print(df.columns)
        df_normalized = df.div(df.sum(axis=1), axis=0)
        #print(df_normalized.head())
        
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
     
        if kind == "pickle":
            df_normalized.to_pickle(self.output_directory + '/Graph_CC_An2_V1_normalized.pkl' )
            print("Normalized load profile saved in " + self.output_directory + '/Graph_CC_An2_V1_normalized.pkl')
        elif kind == "csv":
            df_normalized.to_csv(self.output_directory + '/Graph_CC_An2_V1_normalized.csv')
            print("Normalized load profile saved in " + self.output_directory + '/Graph_CC_An2_V1_normalized.csv')
        elif kind == "excel":
            df_normalized.to_excel(self.output_directory + '/Graph_CC_An2_V1_normalized.xlsx')
            print("Normalized load profile saved in " + self.output_directory + '/Graph_CC_An2_V1_normalized.xlsx')
              
    
    def cooking_this_day(self):
        """Second method to compute the cooking activity  300kWh/year
        
        In this function, we use the probability of having a meal at midday or in the evening
        This function has to run once per day, and will compute the consumption for the cooking post for the day
        
        
        """
        lunch = False
        supper = False
        if self.day % 7 == 6 or self.day % 7 == 7:  # Saturday or Sunday
            if np.random.rand() < 0.82:
                lunch = True
            if np.random.rand() < 0.87:
                supper = True
        else:
            if np.random.rand() < 0.6:  # 6 households out of 10 have dinner at home during weekday
                lunch = True
            if np.random.rand() < 0.85:  # almost every household has supper at home during weekday
                supper = True
        
        ### Breakfast 
        breakfast_beginning_hour = np.random.randint(24, 37)  # between 6h and 9h
        breakfast_duration = np.random.randint(1, 3)
        if np.random.rand() < 0.8:
            breakfast_wh = np.random.random() * 150
        else:
            breakfast_wh = np.random.random() * 500   # between 0 and 500 Wh
        breakfast_power = breakfast_wh*4 / breakfast_duration # in W 
        
        breakfast_index_begin = (self.day - 1) * 24 * 4 + breakfast_beginning_hour
        breakfast_index_end = breakfast_index_begin + breakfast_duration

        self.consumption[breakfast_index_begin:breakfast_index_end] += breakfast_power
        self.cooking[breakfast_index_begin:breakfast_index_end] += breakfast_power  
        
        ### Lunch
        
        if lunch : 
            lunch_beginning_hour = np.random.randint(46, 57)  # between 11h30 and 14h
            lunch_duration = np.random.randint(1, 4)
            if np.random.rand() < 0.8:
                lunch_wh = np.random.random() * 200
            else:
                lunch_wh = np.random.random() * 1000  # between 0 and 1000 Wh
            lunch_power = lunch_wh*4 / lunch_duration # in W
            
            lunch_index_begin = (self.day - 1) * 24 * 4 + lunch_beginning_hour
            lunch_index_end = lunch_index_begin + lunch_duration
            self.consumption[lunch_index_begin:lunch_index_end] += lunch_power
            self.cooking[lunch_index_begin:lunch_index_end] += lunch_power
            
        ### supper
        if supper : 
            supper_beginning_hour = np.random.randint(72, 87)  # between 18h and 21h30
            supper_duration = np.random.randint(1, 7)
            supper_wh = 200 + np.random.random() * 1000
            supper_power = supper_wh*4 / supper_duration
            
            supper_index_begin = (self.day - 1) * 24 * 4 + supper_beginning_hour
            supper_index_end = supper_index_begin + supper_duration
            self.consumption[supper_index_begin:supper_index_end] += supper_power
            self.cooking[supper_index_begin:supper_index_end] += supper_power
            
    def electric_water_heater(self):
        """This function computes the electric water heater consumption  1582kwh/year si EWH (between 200 and 4200)
        consumption between 21h and 5h
        The electric water heater is used every day, 
        
        """
        
        if self.wh_is_electric : 
            if self.wh_night : 
                wh_beginning_hour = np.random.randint(0, 33)
                if wh_beginning_hour > 21:
                    wh_beginning_hour = 21*4+(wh_beginning_hour-21)
            else :
                wh_beginning_hour = np.random.randint(32,64)
            
            wh_duration = np.random.randint(6, 11) # entre 1h30 et 2h30
            if self.wh_type == 'Joules':
                if self.wh_capacity == 'low':
                    wh_power = 1200
                elif self.wh_capacity == 'medium':
                    wh_power = 2200
                elif self.wh_capacity == 'high':
                    wh_power = 3000 
            elif self.wh_type == 'thermodynamic':         
                wh_power = 1000
            
            if self.day < 135 or self.day > 304 : 
                wh_duration  = int(wh_duration * 1.3)
            else :
                wh_duration  = int(wh_duration * 0.65)
                
            wh_index_begin = (self.day - 1) * 24 * 4 + wh_beginning_hour
            wh_index_end = wh_index_begin + wh_duration
            self.consumption[wh_index_begin:wh_index_end] += wh_power
            self.wh[wh_index_begin:wh_index_end] += wh_power
    
    
    def electric_heating(self):
        """
        this function computes the consumption of the electric heating
        For each day, the heating is either turned on or off, based on the average outdoor temperature
        
        If turned on, the maximum power is computed with the PEB and the area of the flat, the actual power is computed using the hourly weight
        derived from the ademe load profile 
        
        As the temperature data are available for several years, the function will compute the heating consumption for each year
        """
        if self.heating_is_elec :
            hours_begin = (self.day -1 ) * 24
            heating_is_on = []
            for i in range(self.n_year_temp_data):
                is_on = 0
                T_tot = 0
                for h in range(7,22):
                    T_tot += self.temperature_array[hours_begin + h][i]
                T_avg = T_tot / 15
                if T_avg < self.T_ext_threshold:
                    is_on = 1
                heating_is_on.append(is_on)
            heating_is_on = np.array(heating_is_on)
                        
         
            
            hourly_weight = np.array([0.725,0.7,0.775,0.775,0.8,0.95,0.95,1,1,0.98,0.9,0.8,0.8,0.72,0.7,0.68,0.7,0.775,0.875,0.9,0.9,0.8,0.75,0.725])

            for i in range(24*4):
                it = (self.day-1) * 24 * 4 + i
                hours = i // 4
                self.load_heating[it] = self.power_heating * hourly_weight[hours] * heating_is_on
        
    
    def cold_sources(self):
        """
        This function computes the consumption of the cold sources (fridge, freezer)
        The first applyance is automatically refered as a fridge, or fridge-freezer, the second one is a freezer 
        For each applyance, a random power consumption has been chosen, using statistics from ademe
        
        For each day, a constant consumption is added to the consumption array.
        A seasonal factor is taken into account (the cold source consumes more in summer and less in winter)
        """
        cold_index_begin = (self.day - 1) * 24 * 4 
        cold_index_end = cold_index_begin + 96
        summer_factor = 1.2
        winter_factor = 0.9
        if self.day < 90 or self.day > 304 :  #between november and march
            for i in range(self.number_cold_sources):
                self.consumption[cold_index_begin:cold_index_end] += self.cold_power[i] * winter_factor
                self.cold[cold_index_begin:cold_index_end] += self.cold_power[i] * winter_factor
        elif self.day > 151 and self.day < 273 : #between june and october
            for i in range(self.number_cold_sources):
                self.consumption[cold_index_begin:cold_index_end] += self.cold_power[i] * summer_factor
                self.cold[cold_index_begin:cold_index_end] += self.cold_power[i] * summer_factor
        else:
            for i in range(self.number_cold_sources):
                self.consumption[cold_index_begin:cold_index_end] += self.cold_power[i]
                self.cold[cold_index_begin:cold_index_end] += self.cold_power[i]
        
    def washing_utilities(self):
        """
        This function computes the consumption of the washing machine, dryer and the dishwasher
        
        Statistics from ademe shows that 99% of the household have a washing machine, 31% have a dryer and 71% have a dishwasher
        
        washing-machine : 
            For each household having a washing machine, the user can choose a frequency of washing (low, medium, high)
                      - low means 2 or less cycles per week
                        - medium means between 3 and 5 cycles per week
                        - high means more than 6 cycles per week
            at each beginning of the week, a number of cycle to do will be randomly chosen between those ranges
            For each cycle, the power and length of the cycle will be chosen using statistical data from ademe
            for each cycle of the week, a starting time will be chosen using hourly load of ademe -> this can be modified if the user is maximising
            the self consumption
        
        Dryer : 
            A cycle has a high consumption, but dryer are rarely used, especially in summer
            After each washing-machine cycle, the dryer is either turned on or not, based on seasonality and statistical datas
                if a lot of machine cycle, the dryer is more used (no place to dry the clothes)
                in winter, the dryer is more often used
            The power and duration of the cycle are chosen using statistical datas from ademe 
            we have 3 types of dryer : heat-pump, condensation, evacuation, each of them have a fixed power computed with statistical datas
            The duration of the cycle of the dryer is randomnly drown with statistical data 
            
        Dishwasher :
            Each household having a dishwasher will be put into 3 categories of frequency (low, medium, high)
                     - low means 3 or less cycles per week
                     - medium means between 4 and 6 cycles per week
                     - high means more than 7 cycles per week
            at each beginning of the week, a number of cycle to do will be randomly chosen between those ranges
            For each cycle, the power and length of the cycle will be chosen using statistical data from ademe
        for each cycle of the week, a starting time will be chosen using hourly load of ademe -> this can be modified if the user is maximising
            the self consumption -> dishwasher are often used after a meal
        """
        if self.have_washing_machine:
            number_of_cycle = 0
            if self.washing_frequency == 'low':
                number_of_cycle = np.random.randint(0, 3)
            elif self.washing_frequency == 'medium':
                number_of_cycle = np.random.randint(3, 6)
            else : 
                number_of_cycle = np.random.randint(6, 15)
            cycles_energy = np.zeros(number_of_cycle)
            cycles_power = np.zeros(number_of_cycle)
            cycle_duration = np.zeros(number_of_cycle)
            cycle_beginning_timestep = np.zeros(number_of_cycle)
            last_timestep = 0
            week_duration = 7 * 24 * 4 - 7*7*4  # 7 days, minus 7h a day of night -> 476 timesteps
            remaining_timesteps = week_duration 
            
            
            energy_ranges = [(0, 100), (100, 200), (200, 300), (300,400), (400, 500), (500, 600), (600, 700), (700, 800), (800, 900), (900, 1000),
                            (1000, 1100), (1100, 1200), (1200, 1300), (1300, 1400), (1400, 1500), (1500, 1600), (1600, 4000)]
            energy_ranges_proba = [7,11.75,15,14.25,12.75,11.25,7.75,5,3.75,3.5,2.25,1.25,1,0.75,0.5,0.5,1.75]
            energy_ranges_proba = [x/100 for x in energy_ranges_proba]
            for i in range(number_of_cycle):
                energy_ranges_len = np.linspace(0, 16, 17)
                energy_cycle_int = np.random.choice(energy_ranges_len, p=energy_ranges_proba)
                energy_cycle = energy_ranges[int(energy_cycle_int)]
                cycles_energy[i] = np.random.randint(energy_cycle[0], energy_cycle[1])
                if cycles_energy[i] < 300:
                    cycle_duration[i] = np.random.randint(1, 5)  # between 15min and 1h
                elif cycles_energy[i] < 700:
                    cycle_duration[i] = np.random.randint(5, 9)  #between 1h15 and 2h
                else :
                    cycle_duration[i] = np.random.randint(9, 13)   #between 2h15 and 4h
                cycles_power[i] = cycles_energy[i] * 4 / cycle_duration[i]
                if not self.washing_intelligence : 
                    window = remaining_timesteps / (number_of_cycle - i)
                    cycle_beginning_timestep[i] = last_timestep + np.random.randint(0, window)
                    last_timestep = cycle_beginning_timestep[i] + 16 # we can't start another cycle before 4h
                    remaining_timesteps = week_duration - last_timestep
                else:
                    pass
                washing_day = cycle_beginning_timestep[i] // (17*4)
                washing_hour = cycle_beginning_timestep[i] % (17*4) + 6 * 4
                cycle_beginning_timestep[i] = self.day * 24 * 4 + washing_day * 24 * 4 + washing_hour
                cycle_end_timestep = cycle_beginning_timestep[i] + cycle_duration[i]
                self.consumption[int(cycle_beginning_timestep[i]):int(cycle_end_timestep)] += cycles_power[i] 
                self.washing_usage[int(cycle_beginning_timestep[i]):int(cycle_end_timestep)] += cycles_power[i]
        
            if self.have_dryer :  # an household can not have a dryer if it does not have a washing machine
                for i in range(number_of_cycle):  # a dryer can just be used after a washing machine cycle
                    r = np.random.rand()
                    if self.day < 151 or self.day > 273 : #from october to june  winter
                        if self.washing_frequency == 'high': # if a lot of cycle during winter, we almost always use the dryer
                            if r < 0.9:
                                dryer_is_active = True
                            else : 
                                dryer_is_active = False
                        elif self.washing_frequency == 'medium':  # if a medium number of cycle, we use the dryer 60% of the time
                            if r < 0.6:
                                dryer_is_active = True
                            else:
                                dryer_is_active = False
                        else : 
                            if r < 0.4:  # if a low number of cycle, we use less the dryer
                                dryer_is_active = True
                            else:
                                dryer_is_active = False
                            
                    else:
                        if self.washing_frequency == 'high': # if a lot of cycle during summer, we often use the dryer, but not always
                            if r < 0.6: # modify proba
                                dryer_is_active = True
                            else:
                                dryer_is_active = False
                        elif self.washing_frequency == 'medium':  # if a medium number of cycle, we use the dryer 40% of the time
                            if r < 0.4:
                                dryer_is_active = True
                            else:
                                dryer_is_active = False
                        else :  # if a low number of cycle, we use less the dryer
                            if r < 0.1:
                                dryer_is_active = True
                            else:
                                dryer_is_active = False 
                    if dryer_is_active:
                        if self.dryer_type == 'heat-pump':
                            dryer_power = 416
                            dryer_duration = 6 + np.random.randint(0, 5)  # between 1h30 and 2h30 
                        elif self.dryer_type == 'condensation':
                            dryer_power = 1112
                            dryer_duration = 4 + np.random.randint(0, 5)  # between 1h and 2h
                        else:
                            dryer_power = 1215
                            dryer_duration = 5 + np.random.randint(0, 5)  # between 1h15 and 2h15
                        if self.dryer_intelligence == False : 
                            dryer_index_begin = int(cycle_end_timestep + np.random.randint(0, 5))  # up to 1h after end of washing machine cycle
                        dryer_index_end = dryer_index_begin + dryer_duration
                        self.consumption[dryer_index_begin:dryer_index_end] += dryer_power
                        self.washing_usage[dryer_index_begin:dryer_index_end] += dryer_power
        
        if self.have_dishwasher:
            ## cycle energy using the probability fig 4-24
            ## duration :  3 ranges depending of the total energy consumed 
            
            if self.dishwasher_frequency == 'low':
                dishwasher_num_cycle = np.random.randint(0,3)
            elif self.dishwasher_frequency == 'medium':
                dishwasher_num_cycle = np.random.randint(3,5)
            else : 
                dishwasher_num_cycle = np.random.randint(5, 11)
            
            dishwasher_energy_choice = [(100,200), (200,300), (300,400),(400,500), (500,600), (600,700), (700,800),(800,900),(900,1000),
                                        (1000,1100),(1100,1200),(1200,1300),(1300,1400),(1400,1500),(1500,1600),(1600,1700),(1700,1800),(1800,2500)]
            dishwasher_probabilities = [0.5,1.25,3,4,5.25,7.25,12.25,11.75,11.25,8.5,8.5,8.5,6.5,4.5,3.25,2,1,0.75]
            dishwasher_probabilities = [x/100 for x in dishwasher_probabilities]
            dishwasher_energy_len = np.linspace(0, len(dishwasher_energy_choice)-1, len(dishwasher_energy_choice))
            if self.dishwasher_intelligence == False :
                dishwasher_windows = np.linspace(0,13,14) # we start the dishwasher either afetr lunch or supper
                taken = np.random.choice(dishwasher_windows, size=dishwasher_num_cycle, replace=False)
                for i in taken : 
                    if i % 2 ==0 : #after lunch
                        timestep_window_begin = self.day *24 *4 + i * 24 * 2 + 12 * 4
                        timestep_window_end = timestep_window_begin + 4*4
                        timestep_begin = int(np.random.randint(timestep_window_begin, timestep_window_end+1))
                    else : 
                        timestep_window_begin = self.day * 24 * 4 + (i-1) * 24 * 2 + 18 * 4
                        timestep_window_end = timestep_window_begin + 3*4
                        timestep_begin = int(np.random.randint(timestep_window_begin, timestep_window_end+1))

                    de_i = int(np.random.choice(dishwasher_energy_len, p=dishwasher_probabilities))
                    dishwasher_energy = np.random.randint(dishwasher_energy_choice[de_i][0], dishwasher_energy_choice[de_i][1])
                    if dishwasher_energy < 700:
                        dishwasher_duration = np.random.randint(2,5)
                    elif dishwasher_energy <1300 : 
                        dishwasher_duration = np.random.randint(4, 9)
                    else : 
                        dishwasher_duration = np.random.randint(8,13)
                    
                    dishwasher_power = dishwasher_energy * 4 / dishwasher_duration
                    timestep_end = int(timestep_begin + dishwasher_duration)
                    self.consumption[timestep_begin:timestep_end]+=dishwasher_power
                    self.washing_usage[timestep_begin:timestep_end]+=dishwasher_power
                        
                        
            
    
    
    def other(self):
        """ This function computes the consumption of the other appliances, such as TV, computer, lights, etc.
        
            A standard load curve is used, with a random parameter that will modify the power
            This consumption is constant all year long, and is not affected by the seasonality
        """
        other_loads = [65,52,42,38,36,35,44,58,60,62,65,67,72,75,72,73,76,87,105,122,128,132,112,87]
        other_loads = np.array(other_loads)
        real_other_loads = other_loads * (self.other_random_param + 0.5)  # between 0.5 and 1.5 times the load
        it_begin = (self.day - 1) * 24 * 4
        for i in range(24*4):
            self.consumption[it_begin + i] += real_other_loads[i // 4]
            self.other_power[it_begin + i] += real_other_loads[i // 4] 


    def elec_vehicle(self):
        
        """
        This function computes the consumption of the electric vehicle
        
        """
        pass
    def launch_year(self):
        """
        This function computes the consumption of the household for the whole year
        
        """
        for i in range(365):
            self.cooking_this_day()
            self.electric_water_heater()
            self.cold_sources()
            self.electric_heating()
            self.other()
            if i % 7 == 0:
                self.washing_utilities()
            self.day += 1
        
        for year in range(self.n_year_temp_data):
            self.total_consumption[:, year] = self.consumption + self.load_heating[:, year]
            
        
    def plot_consumption(self, args, plot_day=False, plot_week=False, plot_to_from=False, plot_whole_year=False):
        """
        This function plots the consumption of the household
        """
        
        if plot_day:
            try:
                day = args['day'] - 1
                month = args['month']
                
            except: 
                ValueError("You must provide a day and a month to plot the consumption of a day")
            
            day_number = datetime.date(2021, month, day).timetuple().tm_yday
            index_begin = (day_number - 1) * 24 * 4
            index_end = index_begin + 24 * 4
            conso_to_plot = self.consumption[index_begin:index_end]
            day_to_plot = datetime.date(2021, 1,1) + datetime.timedelta(days=day_number)
            hours = np.linspace(0, 24, 24*4)
            
            sns.lineplot(x=hours, y=conso_to_plot)
            plt.xlabel('Hour of the day')
            plt.ylabel('Consumption (W)')
            plt.xticks(rotation=45)
            plt.title('Consumption of the household on ' + day_to_plot.strftime("%d/%m"))
            plt.show()
        
        if plot_week:
            try :
                week = args['week']
            except:
                ValueError("You must provide a week number to plot the consumption of a week")
            
            index_begin = (week - 1) * 7 * 24 * 4
            index_end = index_begin + 7 * 24 * 4
            conso_to_plot = self.consumption[index_begin:index_end]
            timestep_per_day = 24 * 4
            day_ticks =  np.linspace(0, 576, 7)
            day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            sns.lineplot(x=np.linspace(0, 672, 672), y=conso_to_plot/1000)
            plt.xticks(ticks=day_ticks, labels=day_labels, rotation=45)
            plt.xlabel('Day of the week')
            plt.ylabel('Consumption (kW)')
            plt.title('Consumption of the household during week ' + str(week))
            plt.show()
        
        if plot_to_from:
            try : 
                from_day_number = args['from_day']
                to_day_number = args['to_day']
            except:
                ValueError("You must provide a starting day and an ending day to plot the consumption between two days")
            

            index_begin = (from_day_number - 1) * 24 * 4
            index_end = (to_day_number) * 24 * 4
            conso_to_plot = self.consumption[index_begin:index_end]
            days = np.linspace(from_day_number, to_day_number, to_day_number - from_day_number + 1)
            cumulative_days = np.linspace(0, (to_day_number - from_day_number + 1) * 24 * 4, to_day_number - from_day_number+ 1)
            day_ticks = [1] + list(cumulative_days[:-1] + 1)
            day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            sns.lineplot(x=np.linspace(0, (to_day_number- from_day_number+ 1) * 24 * 4, (to_day_number- from_day_number+ 1) * 24 * 4), y=conso_to_plot)
            plt.xticks(ticks=day_ticks, labels=cumulative_days, rotation=45)
            plt.xlabel('Day')
            plt.ylabel('Consumption (W)')
            date_start = (datetime.date(2021, 1,1) + datetime.timedelta(days=from_day_number)).strftime("%d/%m")
            date_end = (datetime.date(2021, 1,1) + datetime.timedelta(days=to_day_number)).strftime("%d/%m")
            plt.title('Consumption of the household between ' +  date_start + ' and ' + date_end)
            plt.show()
        
        if plot_whole_year:
            
            days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  
            cumulative_days = np.cumsum(days_per_month)
            cumulative_timestep = np.cumsum(days_per_month) * 24 * 4

            month_ticks = [1] + list(cumulative_timestep[:-1] + 1)  
            month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            sns.lineplot(x=np.linspace(0, 35040, 35040), y=self.consumption/1000)
            plt.xticks(ticks=month_ticks, labels=month_labels, rotation=45)
            plt.xlabel('Time step')
            plt.ylabel('Consumption (kW)')
            plt.title('Consumption of the household during the year')
            plt.show()
            
    def save_consumption(self):
        """
        This function saves the consumption of the household in a csv file
        """
        
        
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        df = pd.DataFrame(self.total_annual_consumption)
        df.to_csv(self.output_directory + '/consumption.csv')
        print("Consumption saved in " + self.output_directory + '/consumption.csv')