"""
 test file pour la cuisson
"""

import numpy as np
import matplotlib.pyplot as plt
import random as rd
import pandas as pd
import os





class inhabitants:
    
    def __init__(self, params):
        
        self.activities = params['activities']
        self.current_activity = None
        self.time = 0
        self.isbusy = False
        self.time_left_for_activity = 0
        self.input_directory = params['input_directory']
        self.output_directory = params['output_directory'] 
        
        
        
    
    def update_activities(self):
        self.activities[self.current_activity] = 0
        for activity in self.activities:
            self.update_activity(activity)
    
    
    def update_activity(self, activity):
        if activity == "oven":
            pass
    
    def choose_activity(self):
        """ choose an activity on the list of activities 
            The activity is chosen using the weights of each activities
            Before calling this function, the weights of each activities must be updated (update_activities)
            
            This function calls launch_activity that will compute the length  and the power curve of the activity 

        Returns:
            self.current_activity (str): the activity that has been chosen
        """
        
        possibilities = []
        probabilities = []
        
        for activity in self.activities:
            possibilities.append(activity)
            probabilities.append(self.activities[activity])
            
        probabilities = probabilities/np.sum(probabilities)
        index = rd.choices(range(len(probabilities)), weights=probabilities, k=1)[0]
        
        self.current_activity = possibilities[index]
        self.launch_activity()
        
        return self.current_activity

    def launch_activity(self):
        """ launch the activity that has been chosen
        
        
        """
        pass
    
    def create_probability_file(self, kind):
        """This function creates a file with the probabilities of each activity, using the ademe load profile
        
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
        
        


def oven_usage():
    t_court = 0.25
    t_moy = 0.75
    t_long = 2
    
    p_cycle = 765 # Wh
    p_moy =900 #W
    
    proba_cycle_court = 0.3
    proba_cycle_moyen = 0.5
    proba_cycle_long = 0.2
    
    guess = rd.random()
    
    if guess < proba_cycle_court:
        dt = t_court
    elif proba_cycle_court < guess < proba_cycle_court + proba_cycle_moyen:
        dt = t_moy
    else:
        dt = t_long
        
    
    return dt, p_moy



    
    
    
        
    
    