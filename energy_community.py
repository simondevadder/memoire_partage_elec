"""
This file contains the agent "energy community"

"""
    
import numpy as np


class EnergyCommunity:
    
    def __init__(self, params):
        """
        Initialize the energy community
        Args:
            params (dictionary):  a dictionary containing the following parameters :
                n_households (int): number of households in the community
                key (string): repartition key, either fix1round, fixmultiround, prorata, hybrid
            
                    fix1round: the production is equally distributed to the consumers in 1 round,
                                if the consumer's consumption is lower than what he gets, the rest is injected to the grid
                    
                    fixmultiround: the production is distributed to the consumers in multiple rounds,
                                if the consumer's consumption is lower than what he gets, the rest is redistributed to the other consumers during the next round
                                
                    prorata: the production is distributed to the consumers to the proportion of their consumption on the total consumption of the community
                                In this case, if the total consumption is lower than the production, nothing is injected to the grid
                                
                    hybrid: the production is first distributed to the consumers in 1 round, 
                            then the rest is distributed to the consumers to the proportion of their consumption on the total consumption of the community
                
               
                PV_inclination (array of float): inclination of the PV panels (degrees compared to ground), in an array if multiple groups of PV panels
                PV_orientation (array of float): orientation of the PV panels (degrees compared to north), in an array if multiple groups of PV panels
                PV_efficiency (float): efficiency of the PV panels (%)
                PV_area (array of float): area of the PV panels (m^2), in an array if multiple groups of PV panels
                
                sharing_price (float): price of the energy shared between the consumers (€/kWh). Price considered fixed along the year
                grid_price (float): price of the energy taken from the grid (€/kWh). Price considered fixed along the year (may be modified in the future)
                grid_injection_price (float): price of the energy injected to the grid (€/kWh). Price considered fixed along the year (may be modified in the future)
                
        
        """
        
        self.longitude = 4.3522  #default = 4.3522  brussels
        self.latitude = 50.85    #default = 50.85
        self.TUTC = 1 #default = 1, 2 in summer time
        
        self.key = params['key']
        self.n_households = params['n_households']
        self.consumption = np.zeros(self.n_households)
        self.repartition = np.zeros(self.n_households)
        self.production = 0 
        self.taken_to_grid = np.zeros(self.n_households)
        self.injected_to_grid = 0
        
        self.PV_inclination = np.radians(params['PV_inclination'])
        self.PV_orientation = np.radians(params['PV_orientation'])
        self.PV_efficiency = params['PV_efficiency']
        self.PV_area = params['PV_area']
        
        self.sharing_price = params['sharing_price']
        self.grid_price = params['grid_price']
        self.grid_injection_price = params['grid_injection_price']
        
        self.n_elevators = params['n_elevators']
        self.elevator_consumption = params['elevator_consumption']
        self.n_floor = params['n_floor']
        
        self.common_area = params['common_area'] # for heating and lighting
        

        self.electric_heating = params['electric_heating'] # if false, not taken into account
        if self.electric_heating:
            self.type_heating = params['type_heating'] # either electric boiler, heating or electric radiators
            self.common_area_volume = params['common_area_volume'] # volume of the common area (m^3)
        
    
    
    def func_compute_production(self, DHI, DNI, day, hour ):
        """ This function compute the irradiance on the PV panels at a given time step, and set the production of the community at time t

        Args:
            DHI (float): Diffuse Horizontal Irradiance (W/m^2), taken from the weather data
            DNI (float): Direct Normal Irradiance (W/m^2), taken from the weather data
            day (int): day number (jan 1 : day =1)
            hour (int): hour of the day (0 to 23)
            
        Returns:
            G (array): Irradiance on the PV panels (W/m^2) for each PV panel group
        """
        
        LSTM = 15 *self.TUTC  # Local Standard Time Meridian
        B = np.radians(360/365 * (day - 81))  
        EoT = 9.87 * np.sin(2*B) - 7.53 * np.cos(B) - 1.5 * np.sin(B)  # Equation of Time (minutes)
        TC = 4 * (self.longitude - LSTM) + EoT  # Time Correction (minutes)
        LST = hour + TC/60  # Local Solar Time (hours)
        HRA = np.radians(15 * (LST - 12))  # Hour Angle (radian)
        delta = np.radians(-23.45 * np.cos(2*np.pi/365 * (day + 10)))  # Declination Angle (radian)
        alpha = np.arcsin(np.sin(delta) * np.sin(self.latitude) + np.cos(delta) * np.cos(self.latitude) * np.cos(HRA))  # Solar Altitude Angle (radian)
        azimuth = np.arccos((np.sin(delta) * np.cos(self.latitude) - np.cos(delta) * np.sin(self.latitude) * np.cos(HRA)) / np.cos(alpha))  # Solar Azimuth Angle (radian)
        
        G= np.zeros(len(self.PV_inclination))
        if HRA > 0:
            azimuth = 2*np.pi - azimuth
            
        if alpha < 0:
            for i in range(len(self.PV_inclination)):
                G[i] = 0
        else:   
            G = DNI * (np.cos(alpha)*np.sin(self.PV_inclination)*np.cos(self.PV_orientation - azimuth) + np.sin(alpha) * np.cos(self.PV_inclination)) + DHI * (1 + np.cos(self.PV_inclination))/2
        
        for i in range(len(G)):
            if G[i] < 0:
                G[i] = 0
        production = 0
        for i in range(len(G)):
            production += G[i] * self.PV_area[i] * self.PV_efficiency
        self.production = production
        
        return G
            
            
        
        
        
    
    def func_repartition(self, consumption, production):
        """Repartition of the production to the consumers of the community according to the repartition key

        Args:
            consumption (array): Array of the consumption of the consumers at the current time step
            production (float)): Production of the community at the current time step
       
                
            
        Returns:
            repartition (array): Array of the repartition of the production to the consumers
            taken_to_grid (array): Array of the energy taken to the grid by the consumers
            injected_to_grid (float): Energy injected to the grid by the community
        """
        reparti = 0
        repartition = np.zeros(len(consumption))
        if self.key=="fix1round":
            percentage = 1/len(consumption)
            
            for i in range(len(consumption)):
                if consumption[i] > production * percentage:
                    repartition[i] = production * percentage
                    reparti += production * percentage
                else:
                    repartition[i] = consumption[i]
                    reparti += consumption[i]
        
        
                  
        elif self.key=="fixmultiround":
            still_to_repart = production
            conso_not_full = consumption - repartition
            while still_to_repart > 0 and sum(conso_not_full) > 0:
                remain = 0
                consumed_this_round = 0
                for i in range(len(conso_not_full)):
                    if conso_not_full[i]!= 0:
                        remain+=1
                for i in range(len(conso_not_full)):
                    if conso_not_full[i] > 0:
                        if conso_not_full[i] > still_to_repart/remain:
                            repartition[i] += still_to_repart/remain
                            consumed_this_round += still_to_repart/remain
                            conso_not_full[i] -= still_to_repart/remain
                            reparti += still_to_repart/remain
                        else:
                            repartition[i] += conso_not_full[i]
                            consumed_this_round += conso_not_full[i]
                            reparti += conso_not_full[i]
                            conso_not_full[i] = 0
                still_to_repart -= consumed_this_round
                
                
        
        elif self.key=="prorata":
            total_conso = sum(consumption)
            for i in range(len(consumption)):
                available = production * consumption[i] / total_conso
                if consumption[i] > available:
                    repartition[i] = available
                    reparti += available
                else:
                    repartition[i] = consumption[i]
                    reparti += consumption[i]
                    
        elif self.key=="hybrid":
            percentage = 1/len(consumption)
            for i in range(len(consumption)):
                if consumption[i] > production * percentage:
                    repartition[i] = production * percentage
                    reparti += production * percentage
                else:
                    repartition[i] = consumption[i]
                    reparti += consumption[i]
            
            still_to_repart = production - reparti
            conso_not_full = consumption - repartition
            
            total_conso = sum(conso_not_full)
            for i in range(len(conso_not_full)):
                available = still_to_repart * conso_not_full[i] / total_conso
                if conso_not_full[i] > available:
                    repartition[i] += available
                    reparti += available
                    conso_not_full[i] -= available
                else:
                    repartition[i] += conso_not_full[i]
                    reparti += conso_not_full[i]
                    conso_not_full[i] = 0
                    
        self.injected_to_grid = production - reparti
        self.repartition = repartition
        self.taken_to_grid = consumption - repartition
        return self.repartition, self.taken_to_grid, self.injected_to_grid
        