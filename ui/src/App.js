import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [setup, setSetup] = useState({
    '[ARB_FRONT]': 30,
    '[ARB_REAR]': 2,
    '[DAMP_BUMP_HF]': 19,
    '[DAMP_BUMP_HR]': 19,
    '[DAMP_BUMP_LF]': 19,
    '[DAMP_BUMP_LR]': 18,
    '[DAMP_BUMP_RF]': 19,
    '[DAMP_BUMP_RR]': 18,
    '[DAMP_FAST_BUMP_HF]': 10,
    '[DAMP_FAST_BUMP_HR]': 7,
    '[DAMP_FAST_BUMP_LF]': 17,
    '[DAMP_FAST_BUMP_LR]': 6,
    '[DAMP_FAST_BUMP_RF]': 17,
    '[DAMP_FAST_BUMP_RR]': 6,
    '[DAMP_FAST_REBOUND_HF]': 18,
    '[DAMP_FAST_REBOUND_HR]': 14,
    '[DAMP_FAST_REBOUND_LF]': 14,
    '[DAMP_FAST_REBOUND_LR]': 9,
    '[DAMP_FAST_REBOUND_RF]': 14,
    '[DAMP_FAST_REBOUND_RR]': 9,
    '[DAMP_REBOUND_HF]': 16,
    '[DAMP_REBOUND_HR]': 16,
    '[DAMP_REBOUND_LF]': 18,
    '[DAMP_REBOUND_LR]': 17,
    '[DAMP_REBOUND_RF]': 18,
    '[DAMP_REBOUND_RR]': 17,
    '[DIFF_COAST]': 30,
    '[DIFF_POWER]': 20,
    '[DIFF_PRELOAD]': 14,
    '[WING_1]': 30,
    '[WING_2]': 30
  });
  const [predictedLapTime, setPredictedLapTime] = useState(null);

  const handleChange = (e) => {
    setSetup({ ...setup, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict', setup);
      setPredictedLapTime(response.data.predicted_lap_time);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="App">
      <h1>Car Setup Predictor</h1>
      {Object.keys(setup).map((key) => (
        <div key={key}>
          <label>
            {key}:
            <input
              type="range"
              name={key}
              value={setup[key]}
              min="1"
              max="50"
              step="1"
              onChange={handleChange}
            />
          </label>
          <span>{setup[key]}</span>
        </div>
      ))}
      <button onClick={handleSubmit}>Predict Lap Time</button>
      {predictedLapTime && <p>Predicted Lap Time: {predictedLapTime}</p>}
    </div>
  );
}

export default App;
