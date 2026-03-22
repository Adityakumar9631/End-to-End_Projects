from flask import Flask, render_template, request, redirect, session, jsonify
import pickle
import numpy as np
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = '123'

model = pickle.load(open('model.pkl', 'rb'))

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            session['user'] = user
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (user, pwd))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['features']
        features = np.array(data, dtype=float).reshape(1, -1)

        prediction = model.predict(features)

        prediction_value = float(prediction.flatten()[0])

        
        confidence = round((prediction_value / (prediction_value + 1)) * 100, 2)

        return jsonify({
            'prediction': prediction_value * 1000,
            'confidence': confidence
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)