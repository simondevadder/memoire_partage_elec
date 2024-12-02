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
                self.n_households (int): number of households in the community
                self.key (string): repartition key, either fix1round, fixmultiround, prorata, hybrid
            
                    fix1round: the production is equally distributed to the consumers in 1 round,
                                if the consumer's consumption is lower than what he gets, the rest is injected to the grid
                    
                    fixmultiround: the production is distributed to the consumers in multiple rounds,
                                if the consumer's consumption is lower than what he gets, the rest is redistributed to the other consumers during the next round
                                
                    prorata: the production is distributed to the consumers to the proportion of their consumption on the total consumption of the community
                                In this case, if the total consumption is lower than the production, nothing is injected to the grid
                                
                    hybrid: the production is first distributed to the consumers in 1 round, 
                            then the rest is distributed to the consumers to the proportion of their consumption on the total consumption of the community
        
        """
        self.key = params['key']
        self.n_households = params['n_households']
        self.consumption = np.zeros(self.n_households)
        self.repartition = np.zeros(self.n_households)
        self.production = 0 
        self.taken_to_grid = np.zeros(self.n_households)
        self.injected_to_grid = 0
        
        
        
        
    
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
        