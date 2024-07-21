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

AIRQUALITY_TO_NUMERIC = [
    'pm25_north',
    'pm25_south',
    'pm25_east',
    'pm25_west',
]

MERGED_DROP = [
    "Max Wind Speed (km/h)",
    "Min Wind Speed (km/h)",
    "date",
    "Wind Direction",
    "pm25_north",
    "pm25_south",
    "pm25_east",
    "pm25_west",
    "pm25_northeast",
    "pm25_northwest",
    "pm25_southeast",
    "pm25_southwest",
    "month",
    "quarter",
    "week of the year",
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
        'month_sin',
        'month_cos',
        'quarter_sin',
        'quarter_cos',
        'week_sin',
        'week_cos'
    ],
    
    'TARGET': 'Daily Solar Panel Efficiency',

    'ORDINAL': {'Daily Solar Panel Efficiency': ['Low', 'Medium', 'High']},
    
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


