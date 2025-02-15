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
                - heat_pump (bool): True if the heating is done (partially or not) through a heat pump, False otherwise
                
                
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
        self.input_directory = params['input_directory']
        self.output_directory = params['output_directory']
        self.time = 0
        self.hour = 0
        self.day = 1
        self.consumption = np.zeros((35040))  # To be changed, 35 040 is the number of time step in a year, 1 is the number of columns
        self.cooking = np.zeros((35040))
        self.wh = np.zeros((35040))
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
        self.heat_pump = params.get('heat_pump', False)           
        

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
        
        Either I use the annual load curve provided by ademe, either I use the meteo data to compute the need
        """
        if self.heating_is_elec :
            hourly_weight = np.array([0.725,0.7,0.775,0.775,0.8,0.95,0.95,1,1,0.98,0.9,0.8,0.8,0.72,0.7,0.68,0.7,0.775,0.875,0.9,0.9,0.8,0.75,0.725])
            if self.day < 135 or self.day > 304 : 
                hourly_weight = hourly_weight * 1.3
        
    
    def cold_sources(self):
        """
        This function computes the consumption of the cold sources (frigo, congel)
        
        using annual load curve provided by ademe
        
        """
        pass