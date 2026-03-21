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
        year = int(request.form['year'])
        km_driven = int(request.form['km_driven'])
        fuel = int(request.form['fuel'])
        transmission = int(request.form['transmission'])
        owner = int(request.form['owner'])
        mileage = float(request.form['mileage'])
        engine = int(request.form['engine'])
        power = float(request.form['power'])
        seats = int(request.form['seats'])

        features = np.array([[year, km_driven, fuel, transmission, owner,
                              mileage, engine, power, seats]])

        prediction = model.predict(features)[0]

        return render_template("result.html", prediction=round(prediction, 2))

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)