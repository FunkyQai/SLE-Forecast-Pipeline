'''Handles data preprocessing: Data cleaning, feature engineering, and transformation'''

import pandas as pd
import numpy as np

class Preprocessing:
    def __init__(self, weather_data,airquality_data):
        self.weatherdata = weather_data
        self.airqualitydata = airquality_data
        self.merged_data = None

    def clean_weather_data(self):
        '''
        1. Remove duplicate entries and drop `data_ref`
        2. Deal with missing values
        3. Assume negative values for `Wind Speed` and `Wet Bulb Temperature` are typos
        4. Change `Wet Bulb Temperature` unit of measurement to degrees celcius
        5. Standardise `Wind Direction` categories
        6. Standardise `Dew Point Category` categories
        '''

    def clean_airquality_data(self):
        '''
        1. Drop all the psi columns and pm25 central
        2. Remove duplicate rows and drop `data_ref`
        3. Handle Missing Data
        '''

    def merge_data(self):
        '''Merge the weather and airquality data on the date'''

    def feature_engineering(self):
        '''Feature engineering
        1. Average wind speed
        2. create northeast, northwest, southeast, southwest columns for pm25
        3. month, quarter, week of the year
        4. create pm25 column based on wind direction
        '''

    def remove_outliers(self, columns, multiplier=1.5):
        '''Remove outliers from the data'''


    def ordinal_encode(self, columns):
        '''Ordinal encode categorical columns'''

    def normalize_data(self, columns):
        '''Normalize the data'''

    

    


    
