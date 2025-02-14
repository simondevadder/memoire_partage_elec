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
        print(self.consumption.shape)
        #self.normalized_load = pd.read_pickle(self.input_directory + '/Graph_CC_An2_V1_normalized.pkl')
        print("ou_chef")
        
        self.is_cooking = False
        self.time_cooking = 0
        self.time_not_cooking = 0
        
    #Not used  
    def get_load_curve(self):
        """ get the normalized load profile of the mean load for 100 households for a given season and appliance

        Returns:
            _type_: _description_
        """
        load_profile = self.df.loc[self.season + ' - ' + self.applyance]
        return load_profile
    #Not used
    def get_probability(self, t_start, t_end):
        """ Compute the probability of starting the appliance at a given time using the load curve of the appliance (ADEME data)

            The computation is done as follow :
                - The normalized load curve gives us the probability of having the appliance on at each time of the day
                
        """
        
        t_start_arr_down = np.floor(t_start).astype(int)
        t_start_arr_up = np.ceil(t_start).astype(int)
        if t_start_arr_up == 24:
            t_start_arr_up = 0
        t_start_rest = t_start - t_start_arr_down
        
        t_end_arr_down = np.floor(t_end).astype(int)
        t_end_arr_up = np.ceil(t_end).astype(int)
        if t_end_arr_up == 24:
            t_end_arr_up = 0
        t_end_rest = t_end - t_end_arr_down
                
        if t_end>= 24:
            t_end = t_end - 24
            t_end_arr_down = np.floor(t_end).astype(int)
            t_end_arr_up = np.ceil(t_end).astype(int)
            t_end_rest = t_end - t_end_arr_down
            
            probability = 0
            if t_start_arr_up == 0:
                probability = self.load_profile[0:t_end_arr_down].sum()
            else:
                probability = self.load_profile[t_start_arr_up:23].sum()  ## pas bon si t start up = 24 -> 0 
                probability = probability + self.load_profile[0:t_end_arr_down].sum()
            
            before = self.load_profile.iloc[t_start_arr_down] * t_start_rest + self.load_profile.iloc[t_start_arr_up] * (1 - t_start_rest)
            after = self.load_profile.iloc[t_end_arr_down] * t_end_rest + self.load_profile.iloc[t_end_arr_up] * (1 - t_end_rest)
            probability = probability + before + after
        else :
            
            probability = self.load_profile[t_start_arr_up:t_end_arr_down].sum()
            
            before = self.load_profile.iloc[t_start_arr_down] * t_start_rest + self.load_profile.iloc[t_start_arr_up] * (1 - t_start_rest)
            after = self.load_profile.iloc[t_end_arr_down] * t_end_rest + self.load_profile.iloc[t_end_arr_up] * (1 - t_end_rest)
            probability = probability + before + after
        
        #print(load_profile)
        #print(probability)
        return probability
    #Not used 
    def get_probability_matrix(self):
        """ This function returns, for each duration possible of the appliance, the probability of each starting time
        
            The probability is computed as follow : 
                - for each duration, we compute the probability of each starting time using the get_probability function
                - we normalize the probability vector

            Returns : 
                - a matrix of size (t_max - t_min) * 4 x 24 * 4 (we work on a 15 min resolution)
        """

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
        
    def cooking_is_on(self):
        """
        This function returns True if the cooking is on, False otherwise
        
        This function chooses whether the activity "cooking" is carried out or not, based on the probability curve, the past state
        (time since last time cooking, or time since the activity began), and the current time
        
        if True, the function adds the consumption into the consumption matrix, sets the boolean is_cooking to True, and add 1 to the time cooking
                if is_cooking was False before, reset the time not_cooking to 0
        
        if False, the function adds 0 to the consumption matrix, sets the boolean is_cooking to False, and add 1 to the time not_cooking
                if is_cooking was True before, reset the time cooking to 0
        """
        probability = self.normalized_load.loc['Cuisson']
        
        new_state = None
        if self.is_cooking:
            if self.time_cooking <=2: # in this simulation, you can't cook for less than 30min
                new_state = True
            elif self.time_cooking > 16:  # in this simulation, you can't cook for more than 4 hours
                new_state = False
            else: 
                if np.random.rand() < 0.0714: # linear probability of stopping cooking between 2 and 16
                    new_state = False
                else:
                    new_state = True        
        else:
            if self.time_not_cooking <=2: #Once you've cooked, you can't cook again for 30min
                new_state = False
            else :
                random = np.random.rand()
                if random < probability[np.round(self.hour)]: # à verifier l'architecture de probability
                    new_state = True
                else:
                    new_state = False
        
        if new_state:
            pass
            
        
        # TODO : add the consumption to the consumption matrix, and change the time cooking or not cooking
        
    
    def cooking_this_day(self):
        """Second method to compute the cooking activity
        
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
            


            