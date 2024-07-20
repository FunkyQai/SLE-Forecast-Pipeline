import os
import logging
import traceback
import argparse
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'features'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))
from features.utils import setup_logging, query_data_from_database

# remove warnings
import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":

    """
    # Create a parser object
    parser = argparse.ArgumentParser(description='Run the end-to-end pipeline with configurable parameters.')
    # Add arguments to the parser

    args = parser.parse_args()
    """
    setup_logging()
    try:
        # Query data from the database
        query1 = 'SELECT * FROM weather'
        query2 = 'SELECT * FROM air_quality'
        current_dir = os.path.dirname(__file__)
        db_dir = os.path.join(current_dir, 'data')
        weather_df = query_data_from_database(query1, db_dir, 'weather.db')
        airquality_df = query_data_from_database(query2, db_dir, 'air_quality.db')

        weather_csv_path = os.path.join(db_dir, 'weather_data.csv')
        airquality_csv_path = os.path.join(db_dir, 'air_quality_data.csv')

        '''Save the dataframes to CSV
        try:
            weather_df.to_csv(weather_csv_path, index=False)
            logging.info(f"Weather data saved to {weather_csv_path}")
            airquality_df.to_csv(airquality_csv_path, index=False)
            logging.info(f"Air quality data saved to {airquality_csv_path}")
        except Exception as e:
            logging.error(f"Failed to save dataframes to CSV: {e}")
            raise SystemExit
        '''

        # Data Preprocessing

    except Exception as e:
        logging.error(f'Error: {e}\n{traceback.format_exc()}')
        raise SystemExit