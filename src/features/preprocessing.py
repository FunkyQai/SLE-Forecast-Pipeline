'''Handles data preprocessing: Data cleaning, feature engineering, and transformation'''

import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from constants import WIND_DIRECTIONS_MAPPING, WEATHER_DROP, WEATHER_TO_NUMERIC, AIRQUALITY_DROP, AIRQUALITY_TO_NUMERIC, MERGED_DROP

class Preprocessing:

    def __init__(self, weather_data: pd.DataFrame, airquality_data: pd.DataFrame):
        self.weatherdata: pd.DataFrame = weather_data
        self.airqualitydata: pd.DataFrame = airquality_data
        self.merged_data: pd.DataFrame | None = None


    def clean_weather_data(self):
        '''
        1. Remove duplicate entries
        2. Drop irrelevant columns
        3. Convert some columns from object to numeric
        4. Deal with missing values
        5. Take the absolute value of `Wind Speed` 
        6. Standardise `Wind Direction` categories
        '''

        logging.info('Cleaning weather data...')

        # Remove duplicate entries
        self.weatherdata = self.weatherdata.drop_duplicates(subset='data_ref', keep='last')
        
        # Drop irrelevant columns
        self.weatherdata.drop(columns=WEATHER_DROP, inplace=True)

        # Convert selected columns from object to numeric
        for column in WEATHER_TO_NUMERIC:
            self.weatherdata[column] = pd.to_numeric(self.weatherdata[column], errors='coerce')

        # Handle missing values using interpolation
        self.weatherdata.interpolate(method='linear', limit_direction='both', inplace=True)

        # Take the absolute value of `Wind Speed`
        self.weatherdata['Max Wind Speed (km/h)'] = self.weatherdata['Max Wind Speed (km/h)'].abs()

        # Standardise `Wind Direction` categories
        # Convert to lowercase, remove trailing whitespaces, and replace '.' with ''
        self.weatherdata['Wind Direction'] = self.weatherdata['Wind Direction'].str.lower().str.strip().str.replace('.', '', regex=False)
        self.weatherdata['Wind Direction'] = self.weatherdata['Wind Direction'].map(WIND_DIRECTIONS_MAPPING)

        # Log the number of rows and columns in the data
        logging.info(f'Cleaned weather data has {self.weatherdata.shape[0]} rows and {self.weatherdata.shape[1]} columns')


    def clean_airquality_data(self):
        '''
        1. Remove duplicate rows
        2. Drop irrelevant columns
        3. Handle Missing Data
        '''
        
        logging.info('Cleaning air quality data...')

        # Remove duplicate entries and drop `data_ref`
        self.airqualitydata = self.airqualitydata.drop_duplicates(subset='data_ref', keep='last')

        # Drop irrelevant columns
        self.airqualitydata.drop(columns=AIRQUALITY_DROP, inplace=True)

        # Handle missing values using interpolation
        for column in AIRQUALITY_TO_NUMERIC:
            self.airqualitydata[column] = pd.to_numeric(self.airqualitydata[column], errors='coerce')
            self.airqualitydata[column].interpolate(method='linear', limit_direction='both', inplace=True)

        # Log the number of rows and columns in the data
        logging.info(f'Cleaned air quality data has {self.airqualitydata.shape[0]} rows and {self.airqualitydata.shape[1]} columns')


    def merge_data(self):
        '''Merge the weather and airquality data on the date'''

        logging.info('Merging weather and air quality data...')

        self.merged_data = pd.merge(self.weatherdata, self.airqualitydata, on='date', how='inner')

        logging.info(f'Merged data has {self.merged_data.shape[0]} rows and {self.merged_data.shape[1]} columns')


    def feature_engineering(self):
        '''Feature engineering
        1. Average wind speed
        2. create northeast, northwest, southeast, southwest columns for pm25
        3. create pm25 column based on wind direction
        4. month, quarter, week of the year
        5. Add cyclical features for month, quarter, and week of the year
        6. Drop irrelevant columns
        '''

        logging.info('Feature engineering...')

        # Average wind speed
        self.merged_data['Average Wind Speed (km/h)'] = (self.merged_data['Min Wind Speed (km/h)'] + self.merged_data['Max Wind Speed (km/h)']) / 2

        # Create extra columns for pm25 based on wind direction
        self.merged_data['pm25_northeast'] = (self.merged_data['pm25_north'] + self.merged_data['pm25_east'])/2
        self.merged_data['pm25_northwest'] = (self.merged_data['pm25_north'] + self.merged_data['pm25_west'])/2
        self.merged_data['pm25_southeast'] = (self.merged_data['pm25_south'] + self.merged_data['pm25_east'])/2
        self.merged_data['pm25_southwest'] = (self.merged_data['pm25_south'] + self.merged_data['pm25_west'])/2

        # Create pm25 column ba# Conditions for each wind direction
        CONDITIONS = [
            self.merged_data['Wind Direction'] == 'north',
            self.merged_data['Wind Direction'] == 'south',
            self.merged_data['Wind Direction'] == 'east',
            self.merged_data['Wind Direction'] == 'west',
            self.merged_data['Wind Direction'] == 'northeast',
            self.merged_data['Wind Direction'] == 'northwest',
            self.merged_data['Wind Direction'] == 'southeast',
            self.merged_data['Wind Direction'] == 'southwest'
        ]

        # pm25 values for each wind direction
        PM25_VALUES = [
            self.merged_data['pm25_north'],
            self.merged_data['pm25_south'],
            self.merged_data['pm25_east'],
            self.merged_data['pm25_west'],
            self.merged_data['pm25_northeast'],
            self.merged_data['pm25_northwest'],
            self.merged_data['pm25_southeast'],
            self.merged_data['pm25_southwest']
        ]

        self.merged_data['pm25'] = np.select(CONDITIONS, PM25_VALUES)

        # Extract month, quarter, and week of the year from date
        self.merged_data['month'] = pd.to_datetime(self.merged_data['date'], dayfirst=True).dt.month
        self.merged_data['quarter'] = pd.to_datetime(self.merged_data['date'], dayfirst=True).dt.quarter
        self.merged_data['week of the year'] = pd.to_datetime(self.merged_data['date'], dayfirst=True).dt.isocalendar().week

        # Add cyclical features for month, quarter, and week of the year
        self.merged_data['month_sin'] = np.sin(2 * np.pi * self.merged_data['month']/12)
        self.merged_data['month_cos'] = np.cos(2 * np.pi * self.merged_data['month']/12)
        self.merged_data['quarter_sin'] = np.sin(2 * np.pi * self.merged_data['quarter']/4)
        self.merged_data['quarter_cos'] = np.cos(2 * np.pi * self.merged_data['quarter']/4)
        self.merged_data['week_sin'] = np.sin(2 * np.pi * self.merged_data['week of the year']/52)
        self.merged_data['week_cos'] = np.cos(2 * np.pi * self.merged_data['week of the year']/52)

        # Drop irrelevant columns
        self.merged_data.drop(columns=MERGED_DROP, inplace=True)

        # Log the number of rows and columns in the data
        logging.info(f'Cleaned merged data has {self.merged_data.shape[0]} rows and {self.merged_data.shape[1]} columns')


    def remove_outliers(self, columns, multiplier=1.5):
        '''Remove outliers from the data'''
        logging.info('Removing outliers...')
        for column in columns:
            q1 = self.merged_data[column].quantile(0.25)
            q3 = self.merged_data[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - multiplier * iqr
            upper_bound = q3 + multiplier * iqr
            self.merged_data = self.merged_data[self.merged_data[column].between(lower_bound, upper_bound)]

        logging.info(f'Removed outliers')


    def normalize_data(self, columns):
        '''Normalize the data'''
        logging.info('Normalizing data...')
        scaler = StandardScaler()
        for column in columns:
            self.merged_data[column] = scaler.fit_transform(self.merged_data[column].values.reshape(-1, 1))
            
        logging.info('Normalized data')
        logging.info(f'Normalized data has {self.merged_data.shape[0]} rows and {self.merged_data.shape[1]} columns')

    
    def encode_ordinal_columns(self, ordinal_info):
        logging.info('Encoding ordinal columns...')

        # Iterate over the ORDINAL dictionary items
        for column_name, ordinal_list in ordinal_info.items():
            # Create a mapping from the ordinal values to their indices
            ordinal_mapping = {value: index for index, value in enumerate(ordinal_list)}

            # Apply the mapping to the dataset for the current column
            self.merged_data[column_name] = self.merged_data[column_name].map(ordinal_mapping)
            
        logging.info('Encoded ordinal columns using.')
        logging.info(f'Encoded data has {self.merged_data.shape[0]} rows and {self.merged_data.shape[1]} columns')




    



    


    
