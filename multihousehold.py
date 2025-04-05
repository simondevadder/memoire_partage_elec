## Master Thesis, Simon De Vadder, electricity sharing in a multi-units building
## This file contains the class MultiHouseholds, which is used to create and run several households


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import datetime
from energy_community import EnergyCommunity
from household import Household

class MultiHousehold:
    def __init__(self, params, energcom):
        """ Intialize the MultiHousehold class.
        This class is used to create and run several households.
        This method creates the households and initializes the parameters.

        Args:
            params (dictionnary): 
                - n_households (int): number of households to create
                - input_dir (str): directory where the input data is stored
                - output_dir (str): directory where the output data is stored
                - cooking_params (array of str): cooking parameters for each household (low, medium, high)
                - wh_type_params (array of str): water heater type parameters for each household ('Joules', 'thermodynamic' or 'non-electric')
                - wh_capacity_params (array of str): water heater capacity parameters for each household (low, medium, high)
                - wh_intelligence_params (bool): water heater intelligence parameters for each household (True or False)
                - wh_night_params (array of bool): water heater night parameters for each household (True or False)
                ## the param wh_hour_begin will be computed by this class
                - heating_is_elec_params (array of bool): heating is electric parameters for each household (True or False)
                - T_ext_th_params (array of float): external temperature at which the heating is turned on parameters for each household (in °C)
                - T_ext_th_night_params (array of float): external temperature at which the heating is turned on during the night parameters for each household (in °C)
                - PEB_params (array of str): PEB parameters for each household (A to G)
                - heating_eff_params (array of float): heating efficiency parameters for each household (or COP for heat pumps)
                - n_cold_source_params (array of int): number of cold sources parameters for each household
                - have_wm_params (array of bool): washing machine parameters for each household (True or False)
                - wm_frequency_params (array of float): washing machine frequency parameters for each household (low, medium or high)
                - wm_intelligence_params (array of bool): washing machine intelligence parameters for each household (True or False)
                - have_dryer_params (array of bool): dryer parameters for each household (True or False)
                - dryer_frequency_params (array of float): dryer frequency parameters for each household (low, medium or high)
                - dryer_type_params (array of str): dryer type parameters for each household ('heat-pump', 'condensation', 'evacuation')
                - dryer_intelligence_params (array of bool): dryer intelligence parameters for each household (True or False)
                - have_dw_params (array of bool): dishwasher parameters for each household (True or False)
                - dw_frequency_params (array of float): dishwasher frequency parameters for each household (low, medium or high)
                - dw_intelligence_params (array of bool): dishwasher intelligence parameters for each household (True or False)
                - grid_price_type_params (array of str): grid price type parameters for each household ('mono', 'bi')
                - grid_price_day_params (array of float): grid price parameters for each household (in €)
                - grid_price_night_params (array of float): grid price night parameters for each household (in €)
                
                - wh_hours_mode (str): method used to define the beginning hour of the wh of each household ('perfect_knowledge',' fixed')
                                        'perfect_knowledge' : the power produced by the PV is known in advance (pefect knowledge) and the beginning 
                                        hour of the wh is defined by the self-consumption of the PV production
                                        'fixed' : the beginning hour of the wh is fixed for each household and stays the same all year long
            
            enercom (EnergyCommunity): EnergyCommunity object to which the households belong
                                        
        """
        
        
        self.n_households = params["n_households"]
        self.input_dir = params["input_directory"]
        self.output_dir = params["output_directory"]
        self.cooking_params = params.get("cooking_params", [-1] * self.n_households)
        self.wh_type_params = params.get("wh_type_params", ["Joules"] * self.n_households)
        self.wh_capacity_params = params.get("wh_capacity_params", [-1] * self.n_households)
        self.wh_intelligence_params = params.get("wh_intelligence_params",False)
        self.wh_night_params = params.get("wh_night_params", [-1] * self.n_households)
        self.heating_is_elec_params = params.get("heating_is_elec_params", [False] * self.n_households)
        self.T_ext_th_params = params.get("T_ext_th_params", [12] * self.n_households)
        self.T_ext_th_night_params = params.get("T_ext_th_night_params", [7] * self.n_households)
        self.pEB_params = params.get("PEB_params", None)
        self.heating_eff_params = params.get("heating_eff_params", [1] * self.n_households)
        self.n_cold_source_params = params.get("n_cold_source_params", [-1] * self.n_households)
        self.have_wm_params = params.get("have_wm_params", [True] * self.n_households)
        self.wm_frequency_params = params.get("wm_frequency_params", [-1] * self.n_households)
        self.wm_intelligence_params = params.get("wm_intelligence_params", [False] * self.n_households)
        self.have_dryer_params = params.get("have_dryer_params", [-1] * self.n_households)
        self.dryer_frequency_params = params.get("dryer_frequency_params", [-1] * self.n_households)
        self.dryer_type_params = params.get("dryer_type_params", [-1] * self.n_households)
        self.dryer_intelligence_params = params.get("dryer_intelligence_params", [False] * self.n_households)
        self.have_dw_params = params.get("have_dw_params", [-1] * self.n_households)
        self.dw_frequency_params = params.get("dw_frequency_params", [-1] * self.n_households)
        self.dw_intelligence_params = params.get("dw_intelligence_params", [False] * self.n_households)
        self.grid_price_type_params = params.get("grid_price_type_params", ["bi"] * self.n_households)
        self.grid_price_day_params = params.get("grid_price_day_params", [-1] * self.n_households)
        self.grid_price_night_params = params.get("grid_price_night_params", [-1] * self.n_households)
        self.households_array = self.create_households()
        
        
        self.enercom = energcom
        self.production = self.enercom.total_production   # is an array of 8760*n_years (usually 3)
        self.n_years = self.enercom.n_years
        

        self.households_array = self.create_households()
        
        if self.wh_intelligence_params:
            self.wh_hours_mode= params.get("wh_hours_mode", "fixed")

            if self.wh_hours_mode == "perfect_knowledge":
                self.wh_hours_begin_all = np.zeros((self.n_households, 365, self.n_years))
                self.define_wh_hour_begin()
            elif self.wh_hours_mode == "fixed":
                self.define_wh_hour_begin()
        
        
    
    def create_households(self):
        """
        Create the households and initialize the parameters.
        """
        self.households_array = []
        
        for i in range(self.n_households):
            params = {
                "input_directory": self.input_dir,
                "output_directory": self.output_dir,
                "cooking": self.cooking_params[i],
                "wh_type": self.wh_type_params[i],
                "wh_capacity": self.wh_capacity_params[i],
                "wh_intelligence": self.wh_intelligence_params[i],
                "wh_night": self.wh_night_params[i],
                "heating_is_elec": self.heating_is_elec_params[i],
                "T_ext_th": self.T_ext_th_params[i],
                "T_ext_th_night": self.T_ext_th_night_params[i],
                "PEB": self.pEB_params[i],
                "heating_efficiency": self.heating_eff_params[i],
                "n_cold_sources": self.n_cold_source_params[i],
                "have_washing_machine": self.have_wm_params[i],
                "washing_frequency": self.wm_frequency_params[i],
                "washing_intelligence": self.wm_intelligence_params[i],
                "have_dryer": self.have_dryer_params[i],
                "dryer_usage": self.dryer_frequency_params[i],
                "dryer_type": self.dryer_type_params[i],
                "dryer_intelligence": self.dryer_intelligence_params[i],
                "have_dishwasher": self.have_dw_params[i],
                "dishwasher_frequency": self.dw_frequency_params[i],
                "dishwasher_intelligence": self.dw_intelligence_params[i],
                "grid_price_type": self.grid_price_type_params[i],
                "grid_price_day": self.grid_price_day_params[i],
                "grid_price_night": self.grid_price_night_params[i]
            }
            self.households_array.append(Household(params))
        
        self.households_array = np.array(self.households_array)
        return self.households_array
    
    def define_wh_hour_begin(self):
        """
        Define the water heater hour begin for each household.
        """
        
        if self.wh_hours_mode == "fixed":
            hours_array = np.array([12,14,10,12.5,14.5,10.5,13,11,13.75,12,11.25])
            for i in range(self.n_households):
                self.households_array[i].wh_hours_begin = hours_array[i%11]   # modulo 11 to avoid index error
        
        elif self.wh_hours_mode == "perfect_knowledge":
            for year in range (self.n_years) : 
                for d in range (365):
                    tot_prod = self.production[24*d:24*(d+1), year]
                    q_tot = tot_prod.sum()
                    proba = np.zeros(24)
                    for i in range(24):
                        proba[i] = tot_prod[i:i+2].sum()/(2*q_tot)
                    #print("proba : ", proba)
                    #print("proba_sum : ", proba.sum())
                    proba = proba / proba.sum()  # unitarize the proba
                    self.wh_hours_begin_all[:, d, year] = np.random.choice(np.arange(24), size=self.n_households, p=proba)
    
    
    def run(self):
        """ Simulate the electric consumption of the households. 
        """
        self.total_electric_consumption = np.zeros((35040, self.n_households, self.n_years))
        index = 0
        for household in self.households_array:
            for i in range(365):

                household.cooking_this_day()
                household.electric_water_heater()
                household.cold_sources()
                household.electric_heating()
                household.other()
                if i % 7 == 0:
                    household.washing_utilities()
                household.day += 1
            
            for year in range(household.n_year_temp_data):
                household.total_consumption[:, year] = household.consumption + household.load_heating[:, year] + household.load_wh[:, year]
            
            self.total_electric_consumption[:, index, :] = household.total_consumption
            index += 1
            
    def repartition_elec(self):
        """ Repartition of the electricity amoung the households
        """
        
        self.total_repartition = np.zeros((35040,self.n_households, self.n_years))
        self.total_from_grid = np.zeros((35040,self.n_households, self.n_years))
        self.total_injection = np.zeros((35040, self.n_years ))
        
        for year in range(self.n_years):
            for i in range(35040):
                consumption_to_rep = self.total_electric_consumption[i, :, year]
                production_to_rep = self.production[i//4, year]
                self.total_repartition[i, :, year], self.total_from_grid[i, :, year], self.total_injection[i, year] = self.enercom.func_repartition(consumption_to_rep, production_to_rep)
                
                
    def compute_metrics(self):
        """Compute the self consumption and self sufficiency of the households. Compute the total price that each household would have paid 
        without the PV production and the price that they actually paid.  Compute the total revenue for the pv owner and the total investment cost.
        
        
            self consumption : float : share of pv production that is locally consumed
            self sufficiency : float : share of household consumption that is locally produced
        """
        
        self.self_consumption = np.zeros((self.n_years))
        self.self_sufficiency = np.zeros((self.n_households, self.n_years))
        self.injection_year = np.zeros((self.n_years))
        self.production_year = np.zeros((self.n_years))
        self.consumption_year = np.zeros((self.n_households, self.n_years))
        self.repartition_year = np.zeros((self.n_households, self.n_years))
        
       
        
        for year in range(self.n_years):
            self.injection_year[year] = np.sum(self.total_injection[:, year])
            self.production_year[year] = np.sum(self.production[:, year])
            self.self_consumption[year] = 1 - np.sum(self.total_injection[:,year]) / np.sum(self.production[:, year])
            for i in range(self.n_households):
                self.consumption_year[i, year] = np.sum(self.total_electric_consumption[:, i, year])
                self.repartition_year[i, year] = np.sum(self.total_repartition[:, i, year])
                self.self_sufficiency[i, year] = np.sum(self.total_repartition[:, i, year]) / np.sum(self.total_electric_consumption[:, i, year])
                
    
    def pricing(self):
        """Compute the prices 
        """
        
        self.total_price_without_pv = np.zeros((self.n_households, self.n_years))
        self.total_price_with_pv = np.zeros((self.n_households, self.n_years))
        self.total_revenue_without_pv = np.zeros((self.n_years))
        self.total_revenue_with_pv = np.zeros(( self.n_years))
        
        self.total_conso_night = np.zeros((self.n_households, self.n_years))
        self.total_conso_day = np.zeros((self.n_households, self.n_years))
        self.total_conso_night_with_pv = np.zeros((self.n_households, self.n_years))
        self.total_conso_day_with_pv = np.zeros((self.n_households, self.n_years))
        self.total_conso_from_pv = np.zeros((self.n_households, self.n_years))
        
        for year in range(self.n_years):
            for i in range(35040):
                quart_sem = i % 672
                quart_day = i % 96
                if quart_sem >=478 : 
                    self.total_conso_night[:, year] += self.total_electric_consumption[quart_sem, :, year] * 0.25
                    self.total_conso_night_with_pv[:, year] += self.total_from_grid[quart_sem, :, year] * 0.25
                elif quart_day <= 28 or quart_day >= 88 :
                    self.total_conso_night[:, year] += self.total_electric_consumption[quart_sem, :, year] * 0.25
                    self.total_conso_night_with_pv[:, year] += self.total_from_grid[quart_sem, :, year] * 0.25
                else :
                    self.total_conso_day[:, year] += self.total_electric_consumption[quart_sem, :, year] * 0.25
                    self.total_conso_day_with_pv[:, year] += self.total_from_grid[quart_sem, :, year] * 0.25
            self.total_conso_from_pv[:, year] = self.total_repartition[:, :, year].sum(axis=0) *0.25
            
            for i in range(self.n_households):
                self.total_price_without_pv[i, year] = self.total_conso_night[i, year] * self.grid_price_night_params[i] + self.total_conso_day[i, year] * self.grid_price_day_params[i]
                self.total_price_with_pv[i, year] = self.total_conso_night_with_pv[i, year] * self.grid_price_night_params[i] + self.total_conso_day_with_pv[i, year] * self.grid_price_day_params[i]
                self.total_revenue_without_pv[year] += self.total_injection[i, year] * self.enercom.grid_injection_price
                self.total_revenue_with_pv[i, year] += self.total_conso_from_pv[i, year] * self.enercom.sharing_price
                
        self.enercom.compute_minimal_revenue()
        self.enercom.compute_gc_gain()
        self.annualized_investment_cost = self.enercom.annualized_investment_cost
        
        

        
        
        
    def save_results(self):
        """ Save the results of the simulation in a csv file.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        for year in range(self.n_years):
            conso_name = os.path.join(self.output_dir, f"consumption_{year}.csv")
            to_save_conso = self.total_electric_consumption[:, :, year]
            np.savetxt(conso_name, to_save_conso, delimiter=",", fmt="%.1f")
            
            repart_name = os.path.join(self.output_dir, f"repartition_{year}.csv")
            to_save_repart = self.total_repartition[:, :, year]
            np.savetxt(repart_name, to_save_repart, delimiter=",", fmt="%.1f")
            
            from_grid_name = os.path.join(self.output_dir, f"from_grid_{year}.csv")
            to_save_from_grid = self.total_from_grid[:, :, year]
            np.savetxt(from_grid_name, to_save_from_grid, delimiter=",", fmt="%.1f")
            
        np.savetxt(os.path.join(self.output_dir, "injection.csv"), self.total_injection, delimiter=",", fmt="%.1f")
        
        

        # Tu donnes un nom à chaque array
        arrays = {
            'Bills without sharing': self.total_price_without_pv,
            'Bills with sharing': self.total_price_with_pv,
            'revenue without sharing': self.total_revenue_without_pv,
            'revenue with sharing': self.total_revenue_with_pv,
            'self consumption': self.self_consumption,
            'self sufficiency': self.self_sufficiency,
            'total injection': self.injection_year,
            'total production': self.production_year,
            'total consumption': self.consumption_year,
            'total repartition': self.repartition_year,
        }

        # Créer un writer Excel
        with pd.ExcelWriter(os.path.join(self.output_dir, "main_results.xslx"), engine='xlsxwriter') as writer:
            # Créer une feuille Excel
            workbook  = writer.book
            worksheet = workbook.add_worksheet('Feuille1')
            writer.sheets['Feuille1'] = worksheet

            col_start = 0  # Position de départ en colonne

            for name, arr in arrays.items():
                df = pd.DataFrame(arr, columns=['A', 'B', 'C'])

                # Écrire le nom de l'array en haut
                worksheet.write(0, col_start, name)

                # Écrire les en-têtes de colonnes (A, B, C)
                for i, col_name in enumerate(df.columns):
                    worksheet.write(1, col_start + i, col_name)

                # Écrire les données à partir de la ligne 2 (index 2)
                for row_idx, row in enumerate(df.values):
                    for col_idx, val in enumerate(row):
                        worksheet.write(row_idx + 2, col_start + col_idx, val)

                # Avancer la position de départ pour le prochain array
                col_start += df.shape[1] + 1  # +1 pour une colonne vide entre les blocs

                            
                        
                
            
        
      
        
        