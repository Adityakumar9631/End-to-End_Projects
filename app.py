from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        year = int(request.form['Year'])
        km_driven = int(request.form['Kilometers_Driven'])
        fuel = request.form['Fuel_Type']
        transmission = request.form['Transmission']
        owner = request.form['Owner_Type']
        mileage = float(request.form['Mileage'])
        engine = float(request.form['Engine'])
        power = float(request.form['Power'])
        seats = int(request.form['Seats'])

        fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'LPG': 3}
        transmission_map = {'Manual': 0, 'Automatic': 1}
        owner_map = {'First': 0, 'Second': 1, 'Third': 2, 'Fourth & Above': 3}

        fuel = fuel_map.get(fuel, 0)
        transmission = transmission_map.get(transmission, 0)
        owner = owner_map.get(owner, 0)

        features = np.array([[year, km_driven, fuel, transmission, owner,
                              mileage, engine, power, seats]])

        prediction = model.predict(features)[0]

        return render_template('result.html', prediction=round(prediction, 2))

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)