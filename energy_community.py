"""
This file contains the agent "energy community"

"""
    
import numpy as np
import pandas as pd
import os
from datetime import date
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

class EnergyCommunity:
    
    def __init__(self, params):
        """
        Initialize the energy community
        Args:
            params (dictionary):  a dictionary containing the following parameters :
                n_years (int): number of years of weather data
                directory_data (string): relative path to the directory containing the weather data
                weather_file_name (string): name of the weather data file without the extension, nor the year (which must be at the end of the name)
                            e.g. : '50.849062_n_4.352169_e_38.8904_-77.032_psm3-2-2_60_'
                directory_output (string): relative path to the directory where the production will be saved
                begin_year (int): first year of the weather data
                end_year (int): last year of the weather data
                
                
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
                PV_module_size (array of float): the lenght, width, and depth of PV module
                PV_efficiency (float): efficiency of the PV panels(%)
                PV_NOCT (float): Nominal Operating Cell Temperature at G=800W/m^2, Ta = 20°C (°C) ref = 43.6 °C, provided by the manufacturer
                PV_betacoeff (float): Temperature coefficient (°C), positive value. ref = 0.4%/°C, provided by the manufacturer,
                                        can be found in the datasheet under the name : temperature coefficient for P_max 
                PV_Tref (float): reference temperature, Usually 25°C, provided by the manufacturer -> STC contidtions
                PV_area (array of float): area of the PV panels (m^2), in an array if multiple groups of PV panels
                PV_shaddowing (3D array of float): array containing the information for any shadowing object,
                                                    for each PV array, for each shadowing object, the array contains :
                                                            [distance between array and object, object hight, azimuth angle of object, span angle of object]
                                                            span angle means the angle between the center and the edge of the object, as seen by the PV array
                                                    [[[info for obj 1, PV1][info for obj 2, PV 1]][[info for obj 1, PV2][info for obj 2 PV2]]]
                
                
                sharing_price (float): price of the energy shared between the consumers (€/kWh). Price considered fixed along the year
                grid_injection_price (float): price of the energy injected to the grid (€/kWh). Price considered fixed along the year 
                investment_cost (float): investment cost of the PV panels (€), if none, an estimation will be made with the area of the PV panels
                maintenance_cost (float): maintenance cost of the PV panels (€/year), if none, =0
                interest_rate (float): interest rate of the investment (%), if none, =0
                estimated_lifetime (float): estimated lifetime of the PV panels (years), if none, =20
                
        
        """
        
        self.longitude = 4.3522  #default = 4.3522  brussels
        self.latitude = 50.85    #default = 50.85
        self.TUTC = 1 #default = 1, 2 in summer time
        
        self.n_years = params.get('n_years', 1)
        try : 
            self.directory_data = params['directory_data']
        except:
            ValueError("Please, provide the directory containing the weather data")
        try:
            self.weather_file_name = params['weather_file_name']
        except:
            ValueError("Please, provide the name of the weather data file")
        self.directory_output = params.get('directory_output', 'No_name_Output')
        try : 
            self.begin_year = params['begin_year']
            self.end_year = params['end_year']
        except:
            ValueError(" Please, provide the first and last year of the weather data")
            
        self.key = params.get('key', 'hybrid')
        try:
            self.n_households = params['n_households']
        except:
            ValueError("Please, provide the number of households.")
        self.consumption = np.zeros(self.n_households)
        self.repartition = np.zeros(self.n_households)
        self.production = 0 
        self.taken_to_grid = np.zeros(self.n_households)
        self.injected_to_grid = 0
        
        self.PV_inclination = np.radians(params.get('PV_inclination', 20))
        self.PV_orientation = np.radians(params.get('PV_orientation', 180))
        self.PV_module_size = params.get('PV_module_size', 1)  # default = 1m
        self.PV_efficiency = params.get('PV_efficiency', 0.18)  # ref = 18%
        self.PV_NOCT = params.get('PV_NOCT', 43.6) # Nominal Operating Cell Temperature (°C) ref = 43.6 °C
        self.PV_betacoeff = params.get('PV_betacoeff', 0.004)  # Temperature coefficient (°C) ref = 0.4%/°C
        self.PV_Tref = params.get('PV_Tref', 25)  # Usually 25°C
        self.PV_area = params.get('PV_area', 1)
        self.PV_shaddowing = params.get('PV_shaddowing', [])  # if None, return an empty list
        
        
        self.sharing_price = params.get('sharing_price', -1)
        self.compute_price = False
        self.grid_injection_price = params.get('grid_injection_price',-1)
        self.interest_rate = params.get('interest_rate', 0)
        self.investment_cost = params.get('investment_cost', -1)
        self.maintenance_cost = params.get('maintenance_cost', 0)
        self.estimated_lifetime = params.get('estimated_lifetime', 25)
        
        if self.grid_injection_price == -1:
            self.grid_injection_price = 0.015 + np.random.rand() * (0.05 - 0.015)  
        if self.investment_cost == -1:
            price_Wp = 1.5 + np.random.rand() * (3 - 1.5)  # price of the PV panels in €/Wp
            watt_peak = np.sum(self.PV_area) * self.PV_efficiency *1000 # assuming 1000W/m^2
            print("Estimated investment cost between ", 1.5 *watt_peak, " and ", 3 * watt_peak, " €.")
            self.investment_cost = price_Wp * watt_peak
        if self.sharing_price == -1:
            self.compute_price= True
        
        if self.interest_rate != 0 :
            self.annualized_investment_cost = self.investment_cost * self.interest_rate / (1-(1/(1+self.interest_rate))^self.estimated_lifetime)
        else : 
            self.annualized_investment_cost = self.investment_cost / self.estimated_lifetime
        
        self.gc_duration = 10 # Pv installation illigible for green certificate for 10 years
        self.gc_per_kwh = params.get('gc_per_kwh', -1) # 1 green certificate per MWh
        if self.gc_per_kwh == -1:
            watt_peak = np.sum(self.PV_area) * self.PV_efficiency *1000 # assuming 1000W/m^2
            if watt_peak <= 36000:
                self.gc_per_kwh = 1.953/1000
            elif watt_peak <= 100000:
                self.gc_per_kwh = 1.016/1000
            else :
                self.gc_per_kwh = 0.642/1000
        self.selling_price_gc = params.get('selling_price_gc', 65)
        self.gc = np.zeros(self.n_years)
        self.gc_revenue = np.zeros(self.n_years)
        self.minimal_revenue = np.zeros(self.n_years)
        
        
        
        """
        
        self.n_elevators = params.get('n_elevators',0)
        self.elevator_consumption = params('elevator_consumption',0)
        self.n_floor = params.get('n_floor',1)
        
        self.common_area = params.get('common_area', 0) # for heating and lighting
        

        self.electric_heating = params.get('electric_heating', False) # if false, not taken into account
        if self.electric_heating:
            self.type_heating = params.get('type_heating', None) # either electric boiler, heating or electric radiators
            self.common_area_volume = params.get('common_area_volume', 0) # volume of the common area (m^3)
        """
    
    def compute_gc_gain(self):
        """This function computes, considering the annual production of the PV, the number of green certificate earned and the revenue 
        generated by selling them
        """
        production = pd.read_csv(self.directory_output + '/production.csv', header=None)
        production_per_year = production.sum(axis=0)

        for i in range(len(production_per_year)):
            self.gc[i] = production_per_year[i] * self.gc_per_kwh/1000
        self.gc_revenue = self.gc * self.selling_price_gc
        
        
    def compute_minimal_revenue(self):
        """ This function computes the revenue needed to cover the annualized investment cost and the maintenance cost, minus the green certificate revenue
        """
        
        self.minimal_revenue = self.annualized_investment_cost * self.estimated_lifetime + self.maintenance_cost * self.estimated_lifetime - self.gc_revenue[0]*10
        self.minimal_revenue /= self.estimated_lifetime
            
            
    def get_weather_data(self):
        """ This function get the weather data and put them in usable form in self.directory_output

        write :
            dni : .csv file containing the Direct Normal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
            dhi : .csv file containing the Diffuse Horizontal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
            temperature : .csv file containing the temperature (°C) for each hour for each year (8760 x n_years)
            day : .csv file containing the day number of the year for each hour for each year (8760 x n_years)
            hour : .csv file containing the hour of the day for each hour for each year (8760 x n_years)
        """
        
        dhi = np.zeros((8760, self.n_years))
        dni = np.zeros((8760, self.n_years))
        temperature = np.zeros((8760, self.n_years))
        day = np.zeros((8760, self.n_years))
        hour = np.zeros((8760, self.n_years))
        
        for year in range(self.begin_year, self.end_year+1):
            df = pd.read_csv(self.directory_data +'/'+ self.weather_file_name + str(year)+'.csv', skiprows=2)
            dhi[:, year-self.begin_year] = df['DHI']
            dni[:, year-self.begin_year] = df['DNI']
            temperature[:, year-self.begin_year] = df['Temperature']
            day_number =[date(df['Year'][i], df['Month'][i], df['Day'][i]).timetuple().tm_yday for i in range(len(df['Year']))]  #give the day number of the year
            day[:, year-self.begin_year] = day_number
            hour[:, year-self.begin_year] = df['Hour']
       
        
        if not os.path.exists(self.directory_output):
            os.makedirs(self.directory_output)
            
        np.savetxt(self.directory_output + '/dni.csv', dni, delimiter=',', fmt="%.1f")
        np.savetxt(self.directory_output + '/dhi.csv', dhi, delimiter=',', fmt="%.1f")
        np.savetxt(self.directory_output + '/temperature.csv', temperature, delimiter=',', fmt="%.1f")
        np.savetxt(self.directory_output + '/day.csv', day, delimiter=',', fmt="%.1f")
        np.savetxt(self.directory_output + '/hour.csv', hour, delimiter=',', fmt="%.1f")
        
        print('weather data saved')
    
    
    def func_compute_shadowing(self, x, azimuth, elevation, angle_shadow, span_angle, shadow_hight, PV_ground_length, PV_hight ):
        """This function computes the shadowing coefficient of an array of PV panels 

        Args:
            x (float): length between the array of PV panels and the shadowing object (m)
            azimuth (float): azimuth of the sun (radian)
            elevation (float): elevation of the sun (radian)
            angle_shadow (float): azimuth angle where the shadowing object is located (radian)
            span_angle (float) : span angle of the object as seen by the PV array
            shadow_hight (float): hight of the shadowing object (m)
            PV_ground_length (float): length of the PV panels rapported on the ground, this can be computed with the length of the PV 
                                        and the inclination of the PV panels : PV_ground_length = PV_length * cos(inclination) (m)
            PV_hight (float): hight of the PV panels (m), this can be computed with the length of the PV and the inclination of the PV panels :
                                PV_hight = PV_length * sin(inclination) (m)
                                        
        Returns:
            shadowing_coefficient (float): shadowing coefficient of the array of PV panels, between 0 and 1, the proportion of the PV panels that are shadowed
            dhi_shadow_coeff (float): proportion of the sky that is hidden by the shadowing object, between 0 and 1, will be used to reduce the DHI
        """
        shadowing_coefficient = 0
        dhi_shadow_coeff = 0
        alpha_dhi = np.arctan(shadow_hight / x) # for diffuse irradiance, we are interested on computing the portion of the sky that is hidden by the object
        beta_dhi = np.arctan((shadow_hight - PV_hight) / (x + PV_ground_length))
        if beta_dhi > 0 :
                
            dhi_shadow_coeff = (alpha_dhi/np.pi + beta_dhi/np.pi)/2
        else:
            dhi_shadow_coeff = alpha_dhi/np.pi
            
            
        if (angle_shadow - span_angle) < azimuth < (angle_shadow + span_angle):
            #computation of real lentgh between obstacle and PV panels
            x_real = x / np.cos(np.abs(angle_shadow - azimuth))
            
            #computation of elevation angle for which the shadowing coefficient is 0 (for alpha) and 1 (for beta)
            
            alpha = np.arctan(shadow_hight / x_real)
            beta = np.arctan((shadow_hight - PV_hight) / (x_real + PV_ground_length))
            
            #computation of the shadowing coefficient
            
            if alpha < np.pi/2 and beta < np.pi/2:
                if elevation < alpha:
                     if elevation < beta:
                         shadowing_coefficient = 1
                     else:
                         shadowing_coefficient = elevation / (beta - alpha) + alpha / (alpha - beta)
        return shadowing_coefficient, dhi_shadow_coeff
            
        
        
    def func_compute_production_step(self, DHI, DNI, T, day, hour):
        """ This function compute the irradiance on the PV panels at a given time step, and set the production of the community at time t

        Args:
            DHI (float): Diffuse Horizontal Irradiance (W/m^2), taken from the weather data
            DNI (float): Direct Normal Irradiance (W/m^2), taken from the weather data
            T (float): Temperature (°C), taken from the weather data
            day (int): day number (jan 1 : day =1)
            
        Returns:
            production (float): production of the community at time t (Wh)
            G (array): array of the irradiance on the PV panels at time t (W/m^2)
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
        G_dir = np.zeros(len(self.PV_inclination))
        G_diff = np.zeros(len(self.PV_inclination))
        if HRA > 0:
            azimuth = 2*np.pi - azimuth
            
        if alpha < 0:
            for i in range(len(self.PV_inclination)):
                G[i] = 0
        else:         
            G_dir = DNI * (np.cos(alpha)*np.sin(self.PV_inclination)*np.cos(self.PV_orientation - azimuth) + np.sin(alpha) * np.cos(self.PV_inclination)) 
            G_diff = 0.6*DHI * (1 + np.cos(self.PV_inclination)) / 2  #Monocrystalline silicon PV panels absorbs 60% of the diffuse irradiance
            
            
            for i in range(len(self.PV_shaddowing)):
                shadow_coeff = 0
                dhi_coeff = 0
                for j in range(len(self.PV_shaddowing[i])):
                    PV_ground_length = self.PV_module_size[0] * np.cos(self.PV_inclination[i])
                    PV_hight = self.PV_module_size[0] * np.sin(self.PV_inclination[i])
                    sc = self.func_compute_shadowing(self.PV_shaddowing[i][j][0], azimuth, alpha, self.PV_shaddowing[i][j][2], self.PV_shaddowing[i][j][3], self.PV_shaddowing[i][j][1], PV_ground_length, PV_hight)
                    if sc[0] > shadow_coeff : 
                        shadow_coeff = sc[0]
                    if sc[1] > dhi_coeff:
                        dhi_coeff = sc[1]
                    G_dir[i]*=(1-shadow_coeff)
                    G_diff[i]-=dhi_coeff*DHI   # dhi_coeff is the proportion of the sky that is hidden, so the DHI is reduced by this proportion 
        
        G = G_dir + G_diff
        # Temperature effect
        Tcell = T + (G/800) * (self.PV_NOCT - 20)
        efficiency = self.PV_efficiency * (1 - self.PV_betacoeff * (Tcell - self.PV_Tref))
        
        
        for i in range(len(G)):
            if G[i] < 0:
                G[i] = 0
                
        production = 0
        for i in range(len(G)):
            production += G[i] * self.PV_area[i] * efficiency[i]
            
        #self.production = production
        #print("production = ", production)
        
        return production, G[0]
            
    def func_compute_total_production(self):
        """Compute the production of the community for each time step of each year and save it in a new directory using func_compute_production_step

        This function uses the data stored in self.directory_output, this directory must contain the following files :
                                dhi.csv : .csv file containing the Diffuse Horizontal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
                                dni.csv : .csv file containing the Direct Normal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
                                temperature.csv : .csv file containing the temperature (°C) for each hour for each year (8760 x n_years)
                                day.csv : .csv file containing the day number of the year for each hour for each year (8760 x n_years)
                                hour.csv : .csv file containing the hour of the day for each hour for each year (8760 x n_years)       
                                
            Those file can be created using the function get_weather_data
            
        Write : 
        
        This function creates the following files in the directory self.directory_output :
            production.csv : .csv file containing the production of the community for each time step of each year (8760 x n_years)
            G.csv : .csv file containing the irradiance on the PV panels for each time step of each year (8760 x n_years)
        """
        dhi = pd.read_csv(self.directory_output+ '/dhi.csv', header=None)
        #print(dhi)
        dni = pd.read_csv(self.directory_output + '/dni.csv', header=None)
        temperature = pd.read_csv(self.directory_output + '/temperature.csv', header=None)
        day_number = pd.read_csv(self.directory_output + '/day.csv', header=None)
        hour_number = pd.read_csv(self.directory_output + '/hour.csv', header=None)
        
        production = np.zeros((8760,self.n_years))
        G = np.zeros((8760,self.n_years))
        for i in range(8760):
            for j in range(self.n_years):
                production[i][j], G[i][j] = self.func_compute_production_step(dhi.iloc[i, j], dni.iloc[i, j], temperature.iloc[i, j], day_number.iloc[i, j],hour_number.iloc[i, j])
                
                
        if not os.path.exists(self.directory_output):
            os.makedirs(self.directory_output)
            
        np.savetxt(self.directory_output + '/production.csv', production, delimiter=',', fmt="%.1f")
        np.savetxt(self.directory_output + '/G.csv', G, delimiter=',', fmt="%.1f")
        
        print('production saved')
        
        
        
    
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
    
    
    def plot_production(self,  args, plot_day_year=False, plot_day=False, plot_production_per_year=False, 
                        plot_daily_production_year=False, plot_daily_production_boxplot=False):
        """ This function draws different plots of the production of the community

        Args:
            This file uses the production data stored in self.directory_output, this directory must contain the following file :
                                production.csv : .csv file containing the production of the community for each time step of each year (8760 x n_years)
            args (dictionnary): dictionnary of parameters for each plot type : 
                                for plot_day_year :
                                    day (int): day of the month 
                                    month (int): month number (jan = 1)
                                    specific_year (int): year number (optional) if one specific year is chosen, otherwise all years are plotted in boxplot
                                for plot_day :
                                    day (int): day of the month
                                    month (int): month number (jan = 1)
                                for plot_daily_production_year :
                                    specific_year (int): year number
            plot_day_year (bool): if True, plot the production of the community on a specific date (day, month, year to be provided in args)
            plot_day (bool): if True, plot the production of the community on a specific day as a box plot of each year (day, month to be provided in args)
            plot_production_per_year (bool): if True, plot the total production of the community per year, in kWh
            plot_daily_production_year (bool): if True, plot the daily mean production of the community in a specific year (specific_year to be provided in args)
            plot_daily_production_boxplot (bool): if True, plot the daily production of the community as a boxplot for each day of the year
        """
        
        production = pd.read_csv(self.directory_output + '/production.csv', header=None)
        
        if plot_day_year:
            try :
                day = args['day']-1
                month = args['month']
                specific_year = args['specific_year']

            except:
                ValueError("Date is not correctly defined")
            
            specific_year = args.get('specific_year', None)
            day_number = date(specific_year, month, day).timetuple().tm_yday
            production_day = production.iloc[day_number*24:(day_number+1)*24, specific_year-self.begin_year]/1000
            jan_1 = date(specific_year, 1, 1)
            day_to_plot = jan_1 + datetime.timedelta(days=day_number)
            
            hours = np.arange(0,24)
            sns.lineplot(x=hours, y=production_day)
            plt.xlabel('Hour of the day')
            plt.ylabel('Production (kWh)')
            plt.title('Production of the community on ' + day_to_plot.strftime("%d/%m/%Y"))
            plt.show()
        if plot_day :
            try :
                day = args['day']-1
                month = args['month']
            except:
                ValueError("Date is not correctly defined")

            data = {}
            
            for year in range(self.begin_year,self.end_year+1):
                day_number = date(year, month, day).timetuple().tm_yday
                production_day_inter = production.iloc[day_number*24:(day_number+1)*24, year-self.begin_year]/1000
                data[year] = production_day_inter.values
            
            production_day = pd.DataFrame(data)
            production_day.index = range(24)
            jan_1 = date(self.begin_year, 1, 1)
            day_to_plot = jan_1 + datetime.timedelta(days=day_number)
            df_long = production_day.reset_index().melt(id_vars="index", var_name="Year", value_name="production")
            df_long.rename(columns={"index": "Hour"}, inplace=True)
            plt.figure(figsize=(12, 8))
            if self.n_years > 5:
                sns.boxplot(x="Hour", y="production", data=df_long)
            else:
                sns.pointplot(x="Hour", y="production", data=df_long, hue="Year")
            plt.title('Production of the community on ' + day_to_plot.strftime("%d/%m"))
            plt.xlabel("Hour of the day")
            plt.ylabel("Production (kWh)")
            plt.show()
            
        if plot_production_per_year:
            production_per_year = production.sum(axis=0)
            years = np.arange(self.begin_year,self.end_year+1)
            plt.plot(years, production_per_year/1000)
            plt.ylim(0, max(production_per_year)/1000 + 10)
            plt.title('Production of the community per year')
            plt.xlabel('Year')
            plt.ylabel('Production (kWh)')
            plt.show()
            
        
        if plot_daily_production_year :
            try :
                specific_year = args['specific_year']
            except:
                ValueError("Year is not correctly defined")
            
            production_year = production.iloc[:, specific_year-self.begin_year]
            production_per_day = np.zeros(365)
            for i in range(365):
                production_per_day[i] = production_year[i*24:(i+1)*24].sum()
            
            
            jan_1 = date(specific_year, 1, 1)
            datum = []
            for i in range(365):
                datum.append(jan_1 + datetime.timedelta(days=i))
            
            sns.lineplot(x=datum, y=production_per_day/1000)
            plt.xlabel('Day of the year')
            plt.ylabel('Production (kWh)')
            plt.xticks(rotation=45)
            plt.title('Daily mean production of the community in ' + str(specific_year))
            plt.show()
        
        if plot_daily_production_boxplot :
            
            daily_production = {} 
            
            for year in range(self.begin_year,self.end_year+1):
                production_year = production.iloc[:, year-self.begin_year]
                production_per_day = np.zeros(365)
                for i in range(365):
                    production_per_day[i] = production_year[i*24:(i+1)*24].sum()
                daily_production[year] = production_per_day/1000
            
            daily_production_df = pd.DataFrame(daily_production)
            daily_production_df.index = range(1,366)
            df_long = daily_production_df.reset_index().melt(id_vars="index", var_name="Year", value_name="production")
            df_long.rename(columns={"index": "Day"}, inplace=True)
            
            days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  
            cumulative_days = np.cumsum(days_per_month)

            month_ticks = [1] + list(cumulative_days[:-1] + 1)  
            month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            plt.figure(figsize=(12, 8))
            
            sns.boxplot(x="Day",  y="production", data=df_long)
            
            plt.title('Daily production of the community')
            plt.xlabel("Month of the year")
            plt.ylabel("Production (kWh)")
            plt.xticks(ticks=month_ticks, labels=month_labels, rotation=45)
            plt.show()
            

    
        
        
        
        
       