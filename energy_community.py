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
                PV_efficiency (float): efficiency of the PV panels(%)
                PV_NOCT (float): Nominal Operating Cell Temperature at G=800W/m^2, Ta = 20°C (°C) ref = 43.6 °C, provided by the manufacturer
                PV_betacoeff (float): Temperature coefficient (°C), positive value. ref = 0.4%/°C, provided by the manufacturer,
                                        can be found in the datasheet under the name : temperature coefficient for P_max 
                PV_Tref (float): reference temperature, Usually 25°C, provided by the manufacturer -> STC contidtions
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
        self.PV_efficiency = params.get('PV_efficiency', 0.18)  # ref = 18%
        self.PV_NOCT = params.get('PV_NOCT', 43.6) # Nominal Operating Cell Temperature (°C) ref = 43.6 °C
        self.PV_betacoeff = params.get('PV_betacoeff', 0.004)  # Temperature coefficient (°C) ref = 0.4%/°C
        self.PV_Tref = params.get('PV_Tref', 25)  # Usually 25°C
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
        
    
    def get_weather_data(self, directory_new):
        """ This function get the weather data and put them in usable form in a new directory

        Args:
            directory_new (string): directory where the new weather data will be stored
            
        write :
            dni : .csv file containing the Direct Normal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
            dhi : .csv file containing the Diffuse Horizontal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
            temperature : .csv file containing the temperature (°C) for each hour for each year (8760 x n_years)
        """
        dhi = np.zeros((8760, 25))
        dni = np.zeros((8760, 25))
        temperature = np.zeros((8760, 25))
        day = np.zeros((8760, 25))
        hour = np.zeros((8760, 25))
        
        for year in range(1998, 2023):
            df = pd.read_csv('weather_data_brussels/50.849062_n_4.352169_e_38.8904_-77.032_psm3-2-2_60_' + str(year)+'.csv', skiprows=2)
            dhi[:, year-1998] = df['DHI']
            dni[:, year-1998] = df['DNI']
            temperature[:, year-1998] = df['Temperature']
            day_number =[date(df['Year'][i], df['Month'][i], df['Day'][i]).timetuple().tm_yday for i in range(len(df['Year']))]  #give the day number of the year
            day[:, year-1998] = day_number
            hour[:, year-1998] = df['Hour']

        if not os.path.exists(directory_new):
            os.makedirs(directory_new)
            
        np.savetxt(directory_new + '/dni.csv', dni, delimiter=',', fmt="%.1f")
        np.savetxt(directory_new + '/dhi.csv', dhi, delimiter=',', fmt="%.1f")
        np.savetxt(directory_new + '/temperature.csv', temperature, delimiter=',', fmt="%.1f")
        np.savetxt(directory_new + '/day.csv', day, delimiter=',', fmt="%.1f")
        np.savetxt(directory_new + '/hour.csv', hour, delimiter=',', fmt="%.1f")
        
        print('weather data saved')
    
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
        if HRA > 0:
            azimuth = 2*np.pi - azimuth
            
        if alpha < 0:
            for i in range(len(self.PV_inclination)):
                G[i] = 0
        else:   
            G = DNI * (np.cos(alpha)*np.sin(self.PV_inclination)*np.cos(self.PV_orientation - azimuth) + np.sin(alpha) * np.cos(self.PV_inclination)) + DHI * (1 + np.cos(self.PV_inclination))/2
        
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
            
    def func_compute_total_production(self, directory_data, directory_output, n_years):
        """Compute the production of the community for each time step of each year and save it in a new directory using func_compute_production_step

        Args:
            directory_data (string): relative path to the directory containing the weather data, directory must contain the following files :
                                dhi.csv : .csv file containing the Diffuse Horizontal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
                                dni.csv : .csv file containing the Direct Normal Irradiance (W/m^2) for each hour for each year (8760 x n_years)
                                temperature.csv : .csv file containing the temperature (°C) for each hour for each year (8760 x n_years)
                                day.csv : .csv file containing the day number of the year for each hour for each year (8760 x n_years)
                                hour.csv : .csv file containing the hour of the day for each hour for each year (8760 x n_years)       
            directory_output (string): relative path to the directory where the production will be saved, can be the same as directory_data
        """
        dhi = pd.read_csv(directory_data + '/dhi.csv', header=None)
        #print(dhi)
        dni = pd.read_csv(directory_data + '/dni.csv', header=None)
        temperature = pd.read_csv(directory_data + '/temperature.csv', header=None)
        day_number = pd.read_csv(directory_data + '/day.csv', header=None)
        hour_number = pd.read_csv(directory_data + '/hour.csv', header=None)
        
        production = np.zeros((8760,n_years))
        G = np.zeros((8760,n_years))
        for i in range(8760):
            for j in range(25):
                production[i][j], G[i][j] = self.func_compute_production_step(dhi.iloc[i, j], dni.iloc[i, j], temperature.iloc[i, j], day_number.iloc[i, j],hour_number.iloc[i, j])
                
                
        if not os.path.exists(directory_output):
            os.makedirs(directory_output)
            
        np.savetxt(directory_output + '/production.csv', production, delimiter=',', fmt="%.1f")
        np.savetxt(directory_output + '/G.csv', G, delimiter=',', fmt="%.1f")
        
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
    
    
    def plot_production(self, directory_production, args, plot_day_year=False, plot_day=False, plot_production_per_year=False, 
                        plot_daily_production_year=False, plot_daily_production_boxplot=False):
        """ This function draws different plots of the production of the community

        Args:
            directory_production (string): relative path to the directory containing the production data, directory must contain the following file :
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
        
        production = pd.read_csv(directory_production + '/production.csv', header=None)
        
        if plot_day_year:
            try :
                day = args['day']-1
                month = args['month']
                specific_year = args['specific_year']

            except:
                ValueError("Date is not correctly defined")
            
            specific_year = args.get('specific_year', None)
            day_number = date(specific_year, month, day).timetuple().tm_yday
            production_day = production.iloc[day_number*24:(day_number+1)*24, specific_year-1998]/1000
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
            for year in range(1998, 2023):
                day_number = date(year, month, day).timetuple().tm_yday
                production_day_inter = production.iloc[day_number*24:(day_number+1)*24, year-1998]/1000
                data[year] = production_day_inter.values
            
            production_day = pd.DataFrame(data)
            production_day.index = range(24)
            jan_1 = date(1998, 1, 1)
            day_to_plot = jan_1 + datetime.timedelta(days=day_number)
            df_long = production_day.reset_index().melt(id_vars="index", var_name="Year", value_name="production")
            df_long.rename(columns={"index": "Hour"}, inplace=True)
            plt.figure(figsize=(12, 8))
            sns.boxplot(x="Hour", y="production", data=df_long)
            plt.title('Production of the community on ' + day_to_plot.strftime("%d/%m"))
            plt.xlabel("Hour of the day")
            plt.ylabel("Production (kWh)")
            plt.show()
            
        if plot_production_per_year:
            production_per_year = production.sum(axis=0)
            years = np.arange(1998, 2023)
            plt.plot(years, production_per_year/1000)
            plt.ylim(0, max(production_per_year)/1000 + 10)
            plt.title('Production of the community per year')
            plt.xlabel('Year')
            plt.ylabel('Production (kWh)')
            plt.show()
            
        ## TODO :  moyenne par jour, pour une année ou toutes (boxplot et lineplot)
        
        if plot_daily_production_year :
            try :
                specific_year = args['specific_year']
            except:
                ValueError("Year is not correctly defined")
            
            production_year = production.iloc[:, specific_year-1998]
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
            for year in range(1998, 2023):
                production_year = production.iloc[:, year-1998]
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
            

    
        
        
        
        
       