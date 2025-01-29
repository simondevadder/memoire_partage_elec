"""
Master thesis :  electricity sharing in a multi-unit building

This file contains the class definition of the appliances.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

class Appliances:
    def __init__(self, params):
        self.df = pd.read_pickle(params['file'])
        self.season = params['season']
        self.applyance = params['applyance']
        self.t_min = params['t_min']
        self.t_max = params['t_max']
        self.load_profile = self.get_load_curve()
        
        
    def get_load_curve(self):
        """ get the normalized load profile of the mean load for 100 households for a given season and appliance

        Returns:
            _type_: _description_
        """
        load_profile = self.df.loc[self.season + ' - ' + self.applyance]
        return load_profile

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
        
    def get_probability_matrix(self):
        """ This function returns, for each duration possible of the appliance, the probability of each starting time
        
            The probability is computed as follow : 
                - for each duration, we compute the probability of each starting time using the get_probability function
                - we normalize the probability vector

            Returns : 
                - a matrix of size (t_max - t_min) * 4 x 24 * 4 (we work on a 15 min resolution)
        """

        