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
                
                available_roof_area (array of float): available roof area where PV panels can be installed (m^2), in an array if multiple groups of PV panels 
                                                      in different directions and inclinations are installed
                PV_inclination (array of float): inclination of the PV panels (degrees compared to ground), in an array if multiple groups of PV panels
                PV_orientation (array of float): orientation of the PV panels (degrees compared to north), in an array if multiple groups of PV panels
                PV_efficiency (float): efficiency of the PV panels (%)
                
                sharing_price (float): price of the energy shared between the consumers (€/kWh). Price considered fixed along the year
                grid_price (float): price of the energy taken from the grid (€/kWh). Price considered fixed along the year (may be modified in the future)
                grid_injection_price (float): price of the energy injected to the grid (€/kWh). Price considered fixed along the year (may be modified in the future)
                
        
        """
        self.key = params['key']
        self.n_households = params['n_households']
        self.consumption = np.zeros(self.n_households)
        self.repartition = np.zeros(self.n_households)
        self.production = 0 
        self.taken_to_grid = np.zeros(self.n_households)
        self.injected_to_grid = 0
        
        self.available_roof_area = params['available_roof_area']
        self.PV_inclination = params['PV_inclination']
        self.PV_orientation = params['PV_orientation']
        self.PV_efficiency = params['PV_efficiency']
        
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
        