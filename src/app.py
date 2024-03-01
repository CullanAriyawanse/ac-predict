import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from pathlib import Path

PARAMETERS = ['[ARB_FRONT]', '[ARB_REAR]', '[DAMP_BUMP_HF]', '[DAMP_BUMP_HR]', '[DAMP_BUMP_LF]',
              '[DAMP_BUMP_LR]', '[DAMP_BUMP_RF]', '[DAMP_BUMP_RR]', '[DAMP_FAST_BUMP_HF]', 
              '[DAMP_FAST_BUMP_HR]', '[DAMP_FAST_BUMP_LF]', '[DAMP_FAST_BUMP_LR]', 
              '[DAMP_FAST_BUMP_RF]', '[DAMP_FAST_BUMP_RR]',
              '[DAMP_FAST_REBOUND_HF]', '[DAMP_FAST_REBOUND_HR]', '[DAMP_FAST_REBOUND_LF]', 
              '[DAMP_FAST_REBOUND_LR]', '[DAMP_FAST_REBOUND_RF]', '[DAMP_FAST_REBOUND_RR]', 
              '[DAMP_REBOUND_HF]', '[DAMP_REBOUND_HR]', '[DAMP_REBOUND_LF]', '[DAMP_REBOUND_LR]', 
              '[DAMP_REBOUND_RF]', '[DAMP_REBOUND_RR]', '[DIFF_COAST]', '[DIFF_POWER]', 
              '[DIFF_PRELOAD]', '[WING_1]', '[WING_2]']
LAP_TIMES_DIR = Path('lap_times')

def read_setup_parameters(file_path) -> dict:
    """Read parameters from the parameters txt file and return a dictionary 
    Args:
        file_path (str): file path of the text file
    """

    with open(file_path, 'r') as file:
        lines = file.readlines()

    setup_parameters = {}
    lines_iter = iter(lines)
    for line in lines_iter:
        if line.startswith('['):
            key = line.strip()
            if key not in PARAMETERS:
                continue
            value = float(next(lines_iter).split('=')[1].strip())
            setup_parameters[key] = value

    return setup_parameters

def create_and_train_model():
    """
    Main Function
    """
    global model

    merged_data = pd.DataFrame()

    for lap_time in os.listdir(LAP_TIMES_DIR):
        # Read lap times data and clean to obtain information we need 
        totals_row = pd.read_csv(f'{LAP_TIMES_DIR}\\{lap_time}', skiprows=4, index_col=0)
        totals_row = totals_row.iloc[:, :-2]
        totals_row = totals_row.applymap(lambda x: x if x <= 75.3 else None)
        totals_row = totals_row.dropna(axis=1)
        totals_row = totals_row.T.reset_index(drop=True)

        session_dict_df = pd.read_csv('session_dictionary.csv')
        matching_setup = session_dict_df.loc[session_dict_df['Session'] == os.path.splitext(lap_time)[0], 'Setup'].values[0]
        # Read setup parameters
        car_setup_parameters = read_setup_parameters(f'parameters\\{matching_setup}.ini')

        # Merge lap times data and setup parameters
        for parameter, value in car_setup_parameters.items():
            totals_row[parameter] = value

        merged_data = pd.concat([merged_data, totals_row])

    # Save merged data to a new CSV file
    merged_data.to_csv('merged_datatotalsnew.csv')

    # # Load the merged dataset
    data = pd.read_csv('merged_datatotalsnew.csv')

    # # Split the dataset into features (X) and target (y)
    x = data[PARAMETERS]
    y = data['Totals']

    # # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # # Train the model
    model = LinearRegression()
    model.fit(x_train, y_train)

    return model

create_and_train_model()
