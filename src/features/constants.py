WIND_DIRECTIONS_MAPPING = {
    'n':'north', 
    's':'south', 
    'e':'east', 
    'w':'west', 
    'ne':'northeast', 
    'nw':'northwest', 
    'se':'southeast', 
    'sw':'southwest',
    'northward':'north',
    'southward':'south',
}

WEATHER_DROP = [
    "Wet Bulb Temperature (deg F)",
    "Daily Rainfall Total (mm)",
    "Highest 30 Min Rainfall (mm)",
    "Min Temperature (deg C)",
    "Relative Humidity (%)",
    "Dew Point Category",
    "data_ref"
]

WEATHER_TO_NUMERIC = [ 
    'Highest 60 Min Rainfall (mm)', 
    'Highest 120 Min Rainfall (mm)', 
    'Maximum Temperature (deg C)', 
    'Min Wind Speed (km/h)', 
    'Max Wind Speed (km/h)' 
]

AIRQUALITY_DROP = [
    "psi_north",
    "psi_south",
    "psi_east",
    "psi_west",
    "psi_central",
    "pm25_central",
    "data_ref"
]

MERGED_DROP = [
    "Max Wind Speed (km/h)",
    "Min Wind Speed (km/h)",
    "date",
    "Wind Direction",
    "psi_north",
    "psi_south",
    "psi_east",
    "psi_west",
    "psi_northeast",
    "psi_northwest",
    "psi_southeast",
    "psi_southwest",
]

TRAINING_COLUMNS = {
    'NUMERICAL': 
    [
        'Highest 60 Min Rainfall (mm)',
        'Highest 120 Min Rainfall (mm)',
        'Maximum Temperature (deg C)',
        'Average Wind Speed (km/h)',
        'Cloud Cover (%)',
        'Air Pressure (hPa)',
        'Sunshine Duration (hrs)',
        'pm25',
    ],
    
    'CATEGORICAL': 
    ['month', 
     'quarter', 
     'week of the year'
    ],
    
    'TARGET': 'Daily Solar Panel Efficiency',
    
    'PRESERVE_MORE': 
    [
        'Highest 60 Min Rainfall (mm)',
        'Highest 120 Min Rainfall (mm)',
        'pm25'
    ],

    'PRESERVE_LESS': 
    [   
        'Maximum Temperature (deg C)',
        'Average Wind Speed (km/h)',
        'Cloud Cover (%)',
        'Air Pressure (hPa)',
        'Sunshine Duration (hrs)',
    ]
}


