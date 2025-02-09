from flask import Flask, send_from_directory, jsonify, request
import os
import json
import pandas as pd
import random
from model import model
import locale

app = Flask(__name__, static_folder='.')

DATA_FOLDER = 'data'
feedback_data = []

# Einmalige Ladevariable für die CSV-Daten
dataset = []

# Setze die lokale Umgebung auf Deutsch, um die Tausendertrennung korrekt zu formatieren
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

# Lade CSV-Daten und extrahiere die relevanten Informationen
def load_csv_data_once():
    global dataset
    if dataset:  # Daten sind bereits geladen
        return dataset

    all_data = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith('.csv'):
            file_path = os.path.join(DATA_FOLDER, file)
            df = pd.read_csv(file_path)
            brand = os.path.splitext(file)[0].title()  # Marke mit Großbuchstaben beginnen
            df['brand'] = brand  # Füge die Marke als neue Spalte hinzu
            all_data.append(df)

    # Kombiniere alle DataFrames zu einem großen DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    dataset = []  # Leere die Liste vor dem Neufüllen
    for index, row in combined_df.iterrows():
        car_data = {
            'title': f"{row['brand']} {row['model']}",
            'price': locale.format_string("%d", row['price'], grouping=True),  # Tausendertrennung für Preis
            'price_ml': float(row['price']),
            'mileage': locale.format_string("%d", row['mileage'], grouping=True),  # Tausendertrennung für Kilometerstand
            'mileage_ml': int(row['mileage']),
            'power': row['engineSize'],
            'power_ml': float(row['engineSize']),
            'firstRegistration': row['year'],
            'firstRegistration_ml': int(row['year']),
            'transmission': row['transmission'],
            'transmission_ml': 1 if row['transmission'].lower() == 'automatic' else 0,
            'fuel': row['fuelType'],
            'fuel_ml': hash(row['fuelType']) % 1000,
            'tax': row.get('tax', 0),
            'mpg': row.get('mpg', 0),
            'image': row.get('image', 'data/gap_filler.jpg'),
        }
        dataset.append(car_data)

    # Mische die Liste zufällig
    random.shuffle(dataset)

    # Weise die `id`s nach dem Mischen neu zu
    for idx, car in enumerate(dataset, start=1):
        car['id'] = idx

    return dataset

# API: Nächster Datensatz
@app.route('/get_car', methods=['GET'])
def get_car():
    dataset = load_csv_data_once()
    current_id = int(request.args.get('id', 1))
    car = next((item for item in dataset if item['id'] == current_id), None)
    if car:
        return jsonify(car)
    else:
        return jsonify({'status': 'failure', 'message': 'Car not found'}), 404

# API: Like oder Dislike
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    if 'car_id' not in data or 'action' not in data:
        return jsonify({'status': 'failure', 'message': 'Missing car_id or action'}), 400

    feedback_entry = {'car_id': data['car_id'], 'action': data['action']}
    feedback_data.append(feedback_entry)

    car = next((item for item in load_csv_data_once() if item['id'] == data['car_id']), None)
    if car:
        # Überprüfen, dass alle 7 Features übergeben werden
        car_features = [
            car['mileage_ml'],           # Kilometerstand
            car['power_ml'],             # Leistung
            car['transmission_ml'],      # Getriebe (1 = Automatik, 0 = Manuell)
            car['fuel_ml'],              # Kraftstofftyp (Hashwert des Kraftstofftyps)
            car['tax'],                  # Kfz-Steuer
            car['mpg'],                  # Verbrauch
            car['firstRegistration_ml']  # Erstzulassung (z. B. 2015)
        ]
        model.update(car_features, data['action'])

    # Speichere Feedback in einer Datei
    with open('feedback.json', 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, indent=4)

    return jsonify({'status': 'success'})

# API: Vorhersage für ein spezifisches Auto
@app.route('/predict/<int:car_id>', methods=['GET'])
def predict(car_id):
    car = next((item for item in load_csv_data_once() if item['id'] == car_id), None)
    if car:
        # Alle 7 Merkmale an das Modell übergeben
        car_features = [
            car['mileage_ml'],           # Kilometerstand
            car['power_ml'],             # Leistung
            car['transmission_ml'],      # Getriebe
            car['fuel_ml'],              # Kraftstofftyp
            car['tax'],                  # Kfz-Steuer
            car['mpg'],                  # Verbrauch
            car['firstRegistration_ml']  # Erstzulassung
        ]
        if len(set(model.y)) <= 1 or len(model.X) < model.min_samples:
            return jsonify({'prediction': 'Keine eindeutige Vorhersage möglich.'})
        prediction, confidence = model.predict(car_features)
        return jsonify({'prediction': prediction, 'confidence': confidence})
    return jsonify({'prediction': 'Keine eindeutige Vorhersage möglich.'})

# Hauptseite
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Statische Dateien
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    load_csv_data_once()  # Lade Daten einmalig beim Start
    app.run(debug=True, host='0.0.0.0')
