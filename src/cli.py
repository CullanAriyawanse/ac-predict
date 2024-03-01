import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from pathlib import Path

PARAMETERS = ['[ARB_FRONT]', '[ARB_REAR]', '[DAMP_BUMP_HF]', '[DAMP_BUMP_HR]',
              '[WING_1]', '[WING_2]']
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

def main():
    """
    Main Function
    """

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

    # Evaluate the model
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f'Root Mean Squared Error: {rmse}')

    # Example car setup parameters
    new_car_setup = {
        '[ARB_FRONT]': 25,
        '[ARB_REAR]': 20,
        '[DAMP_BUMP_HF]': 8,
        '[DAMP_BUMP_HR]': 12,
        '[WING_1]': 30,
        '[WING_2]': 30
    }

    # Convert the car setup parameters to a DataFrame
    new_car_setup_df = pd.DataFrame([new_car_setup])

    # Predict lap time for the new car setup
    predicted_lap_time = model.predict(new_car_setup_df)

    print(f'Predicted Lap Time: {predicted_lap_time[0]}')



if __name__ == '__main__':
    main()
