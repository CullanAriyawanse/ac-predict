from flask import Flask, request, jsonify
from flask_cors import CORS
import app
import pandas as pd

api = Flask(__name__)
CORS(api)

@api.route('/predict', methods=['POST'])
def predict():
    setup_data = request.json
    new_car_setup_df = pd.DataFrame([setup_data])
    predicted_lap_time = app.model.predict(new_car_setup_df)
    return jsonify({'predicted_lap_time': predicted_lap_time[0]})

if __name__ == '__main__':
    api.run(debug=True)
