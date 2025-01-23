"""

Master Thesis :  simulation of an energy community
Master Student: Simon De Vadder
 This file is used to test the functions in the file 'energy_community.py'
"""

import numpy as np
import pandas as pd
from datetime import date
import sys
import os
from matplotlib import pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from energy_community import EnergyCommunity



params = {
        'n_years':3,
        'directory_data': 'brussels',
        'weather_file_name':'brussels_50.8444_4.35609_msg-iodc_60_',
        'directory_output': 'test_directory_brussels_00',
        'begin_year':2017,
        'end_year':2019,
        'n_households': 3,
        'key': 'fix1round',
        'PV_inclination': [20],
        'PV_orientation': [180],
        'PV_module_size':[1.99, 0.991, 0.075],
        'PV_area': [1],
        'PV_efficiency': 0.15,
        'sharing_price': 0.1,
        'grid_price': 0.2,
        'grid_injection_price': 0.05,
        'n_elevators': 1,
        'elevator_consumption': 20,
        'n_floor': 5,
        'common_area': 10,
        'electric_heating': False,   
    }
def test_init():
    params = {'n_households': 3, 'key': 'fix1round'}
    community= EnergyCommunity(params)
    community.consumption = np.array([5, 2, 1])
    community.production = 10
    

#test_init()

def test_get_weather_data():
    community = EnergyCommunity(params)
    community.get_weather_data()

#test_get_weather_data()
     
def test_repartition():
    keys = ["fix1round", "fixmultiround", "prorata", "hybrid"]
    for key in keys :
        params['key'] = key
        community = EnergyCommunity(params)
        community.consumption = np.array([3, 8, 1, 10])

        community.production = 20
        repartition, taken_to_grid, injected_to_grid = community.func_repartition(community.consumption, community.production)
        print(key, repartition, taken_to_grid, injected_to_grid, community.consumption)

#test_repartition()    

def test_func_production(year=2020):
    df = pd.read_csv('weather_data_brussels/50.849062_n_4.352169_e_38.8904_-77.032_psm3-2-2_60_' + str(year)+'.csv', skiprows=2)
    dhi = df['DHI']
    dni = df['DNI']
    year = df['Year']
    month = df['Month']
    day = df['Day']
    hour = df['Hour']
    
    day_number =[date(year[i], month[i], day[i]).timetuple().tm_yday for i in range(len(year))]  #give the day number of the year
    
    params = {
        'n_households': 3,
        'key': 'fix1round',
        'PV_inclination': [30,30],
        'PV_orientation': [108,252],
        'PV_area': [0.5,0.5],
        'PV_efficiency': 0.15,
        'sharing_price': 0.1,
        'grid_price': 0.2,
        'grid_injection_price': 0.05,
        'n_elevators': 1,
        'elevator_consumption': 20,
        'n_floor': 5,
        'common_area': 10,
        'electric_heating': False,   
    }
    community = EnergyCommunity(params)
    print(community.PV_inclination)
    
    production = np.zeros(len(dhi))
    production_per_day = np.zeros(365)
    irr_per_day = np.zeros(365)
    for i in range(len(dhi)):
        community.func_compute_production(dhi[i], dni[i], day_number[i], hour[i])
        production[i] = community.production
        production_per_day[day_number[i]-1] += community.production
        irr_per_day[day_number[i]-1] += dni[i] + dhi[i]
    
    plt.plot(production_per_day)
    plt.plot(irr_per_day)
    plt.title('daily production of a PV panel (2005)')
    plt.xlabel('day of the year')
    plt.ylabel('production (Wh)')
    plt.show()
    plt.plot(production)
    plt.title('hourly production of a PV panel(2005)')
    plt.xlabel('hour of the year')
    plt.ylabel('production (Wh)')
    plt.show()
    plt.plot(dni)
    plt.title('Direct Normal Irradiance (2005)')
    plt.xlabel('hour of the year')
    plt.ylabel('DNI (W/m2)')
    plt.show()
    plt.plot(dhi)
    plt.title('Diffuse Horizontal Irradiance (2005)')
    plt.xlabel('hour of the year')
    plt.ylabel('DHI (W/m2)')
    plt.show()
    plt.plot(irr_per_day)
    plt.title('Total irradiation per day (2005)')
    plt.xlabel('day of the year')
    plt.ylabel('Irradiation(Wh/m2)')
    plt.show()
    
    plt.plot(production_per_day/irr_per_day)
    plt.title('Efficiency of the PV panel (2005)')
    plt.xlabel('day of the year')
    plt.ylabel('Efficiency')
    plt.show()
    a = (1 + np.cos(community.PV_inclination))/2
    print(a)
        

def test_func_compute_total_production():
    community  = EnergyCommunity(params)
    community.func_compute_total_production()
    """
    community = []
    inclination = np.linspace(0, 90, 10)
    orientation = np.linspace(0, 360-360/10, 10)
    for i in range(10):
        for j in range(10):
            params['PV_inclination'] = [inclination[i]]
            params['PV_orientation'] = [orientation[j]]
            community.append(EnergyCommunity(params))
            directory = 'test_directory_incli='+str(inclination[i])+'_orient='+str(orientation[j])
            community[-1].func_compute_total_production('test_directory', directory, 25)
    """
    
    
    

#test_func_compute_total_production()


#test_func_production(year=2005)

def test_func_plot_production():
    
    args={
        'day': 25,
        'month': 5,
        'specific_year': 2017,
    }
    community = EnergyCommunity(params)
    inclination = np.linspace(0, 90, 10)
    orientation = np.linspace(0, 360-360/10, 10)
    """
    for i in range(10):
        for j in range(10):
            params['PV_inclination'] = [inclination[i]]
            params['PV_orientation'] = [orientation[j]]
            #directory = 'test_directory_incli='+str(inclination[i])+'_orient='+str(orientation[j])
            directory = "test_directory"
            community.plot_production(directory, args, plot_day=True, plot_production_per_year=False, plot_daily_production_boxplot=False)
    print(directory)
    """
    community.plot_production( args, plot_day=True, plot_production_per_year=False, plot_daily_production_boxplot=True)
    file = 'test_directory_brussels_00/production.csv'
    production = pd.read_csv(file)
    yearly_sum = production.sum(axis=0)
    print(yearly_sum)



#test_func_plot_production()

def compute_total_mean_production():
    community = EnergyCommunity(params)
    inclination = np.linspace(0, 90, 10)
    orientation = np.linspace(0, 360-360/10, 10)
    mean_production = np.zeros((10, 10))

    for i in range(10):
        for j in range(10):
            params['PV_inclination'] = [inclination[i]]
            params['PV_orientation'] = [orientation[j]]
            params['directory_output'] = 'test_directory_incli='+str(inclination[i])+'_orient='+str(orientation[j])
            community = EnergyCommunity(params)
            community.get_weather_data()
            community.func_compute_total_production()
            file = 'test_directory_incli='+str(inclination[i])+'_orient='+str(orientation[j]) + '/production.csv'
            production = pd.read_csv(file)
            yearly_sum = production.sum(axis=0)
            print(len(yearly_sum))
            mean_production[i, j] = yearly_sum.mean()/1000
            
            
            
    print(mean_production)
    sns.heatmap(np.round(mean_production, 0), xticklabels=orientation, yticklabels=inclination, annot=True,fmt='.0f', cmap='viridis')
    plt.xlabel('PV orientation [°]')
    plt.ylabel('PV inclination [°]')
    plt.title('Mean yearly production [kWh]')
    plt.xticks(rotation=45)  
    plt.yticks(rotation=90)
    plt.gca().invert_yaxis()
    plt.show()
#compute_total_mean_production()


def test_shadowing():
    community = EnergyCommunity(params)
    a = community.func_compute_shadowing(10, 180, 0.10, 180, 0.5, 5, 1.87)
    print(a)
    
#test_shadowing()

def test_shadowing_impact():
    params_2 = params
    params_2['PV_shaddowing'] = [[[2, 0.68, 180, 1.41]]]
    params_2['PV_area'] = [272.15]
    params_2['directory_output'] = 'test_dir_sud_shadow'
    community = EnergyCommunity(params_2)
    community.get_weather_data()
    community.func_compute_total_production()
    args={
        'day': 25,
        'month': 5,
        'specific_year': 2017,
    }
    community.plot_production( args, plot_day=True, plot_production_per_year=False, plot_daily_production_boxplot=False)
    
test_shadowing_impact()