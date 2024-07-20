'''Handles data preprocessing: Data cleaning, feature engineering, and transformation'''

import pandas as pd
import numpy as np
import logging
from constants import WIND_DIRECTIONS_MAPPING, DEW_POINT_CATEGORY_MAPPING

class Preprocessing:

    def __init__(self, weather_data: pd.DataFrame, airquality_data: pd.DataFrame):
        self.weatherdata: pd.DataFrame = weather_data
        self.airqualitydata: pd.DataFrame = airquality_data
        self.merged_data: pd.DataFrame | None = None


    def clean_weather_data(self):
        '''
        1. Remove duplicate entries and drop `data_ref`
        2. Deal with missing values
        3. Assume negative values for `Wind Speed` and `Wet Bulb Temperature` are typos
        4. Change `Wet Bulb Temperature` unit of measurement to degrees celcius
        5. Standardise `Wind Direction` categories
        6. Standardise `Dew Point Category` categories
        '''
        # Remove duplicate entries and drop `data_ref`
        self.weatherdata = self.weatherdata[self.weatherdata.duplicated(subset='data_ref', keep='last')]
        self.weatherdata.drop(columns='data_ref', inplace=True)

        # Handle missing values using interpolation
        self.weatherdata.interpolate(method='linear', limit_direction='both', inplace=True)

        # Take the absolute value of `Wind Speed` and `Wet Bulb Temperature`
        self.weatherdata['Max Wind Speed (km/h)'] = self.weatherdata['Max Wind Speed (km/h)'].abs()
        self.weatherdata['Wet Bulb Temperature (deg F)'] = self.weatherdata['Wet Bulb Temperature (deg F)'].abs()

        # Convert `Wet Bulb Temperature` to degrees celcius
        self.weatherdata['Wet Bulb Temperature (deg C)'] = (self.weatherdata['Wet Bulb Temperature (deg F)'] - 32) * 5/9
        self.weatherdata.drop(columns='Wet Bulb Temperature (deg F)', inplace=True)

        # Standardise `Wind Direction` categories
        # Convert to lowercase, remove trailing whitespaces, and replace '.' with ''
        self.weatherdata['Wind Direction'] = self.weatherdata['Wind Direction'].str.lower().str.strip().str.replace('.', '', regex=False)
        self.weatherdata['Wind Direction'] = self.weatherdata['Wind Direction'].map(WIND_DIRECTIONS_MAPPING)

        # Standardise `Dew Point Category` categories
        # Convert to lowercase
        self.weatherdata['Dew Point Category'] = self.weatherdata['Dew Point Category'].str.lower()
        self.weatherdata['Dew Point Category'] = self.weatherdata['Dew Point Category'].map(DEW_POINT_CATEGORY_MAPPING)

        # Log the number of rows and columns in the data
        logging.info(f'Cleaned weather data has {self.weatherdata.shape[0]} rows and {self.weatherdata.shape[1]} columns')


    def clean_airquality_data(self):
        '''
        1. Remove duplicate rows and drop `data_ref`
        3. Handle Missing Data
        '''
        # Remove duplicate entries and drop `data_ref`
        self.airqualitydata = self.airqualitydata[self.airqualitydata.duplicated(subset='data_ref', keep='last')]
        self.airqualitydata.drop(columns='data_ref', inplace=True)

        # Handle missing values using interpolation
        self.airqualitydata.interpolate(method='linear', limit_direction='both', inplace=True)

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

    

    


    
