from flask import Flask, send_from_directory, jsonify, request
import os
import json
from model import model
from datetime import datetime

app = Flask(__name__, static_folder='.')

DATA_FOLDER = 'data'
feedback_data = []

# Lade Textdaten und extrahiere die relevanten Informationen
def load_text_data(file_path):
    car_data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                car_data['title'] = line.replace('Title:', '').strip()
            elif line.startswith('Price:'):
                car_data['price'] = line.replace('Price:', '').strip()
                car_data['price_ml'] = float(car_data['price'].replace('€', '').replace('.', '').strip())
            elif line.startswith('Mileage:'):
                car_data['mileage'] = line.replace('Mileage:', '').strip()
                car_data['mileage_ml'] = int(car_data['mileage'].replace(' km', '').replace('.', '').strip())
            elif line.startswith('Power:'):
                car_data['power'] = line.replace('Power:', '').strip()
                car_data['power_ml'] = int(car_data['power'].replace(' PS', '').strip())
            elif line.startswith('First Registration:'):
                car_data['firstRegistration'] = line.replace('First Registration:', '').strip()
                date_obj = datetime.strptime(car_data['firstRegistration'], '%m.%Y')
                car_data['firstRegistration_ml'] = date_obj.year * 100 + date_obj.month
            elif line.startswith('Transmission:'):
                car_data['transmission'] = line.replace('Transmission:', '').strip()
                car_data['transmission_ml'] = 1 if car_data['transmission'].lower() == 'automatic' else 0
            elif line.startswith('Color:'):
                car_data['color'] = line.replace('Color:', '').strip()
                car_data['color_ml'] = hash(car_data['color']) % 1000
            elif line.startswith('Owners:'):
                car_data['owners'] = line.replace('Owners:', '').strip()
                car_data['owners_ml'] = int(car_data['owners'])
    return car_data

# Lade Datensätze
def load_data():
    dataset = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith('.txt'):
            data_id = os.path.splitext(file)[0]
            image_path = os.path.join(DATA_FOLDER, f"{data_id}.jpg")
            text_path = os.path.join(DATA_FOLDER, file)
            if os.path.exists(text_path):
                car_data = load_text_data(text_path)
                car_data['id'] = int(data_id)
                car_data['image'] = image_path if os.path.exists(image_path) else os.path.join(DATA_FOLDER, 'gap_filler.jpg')
                dataset.append(car_data)
    
    # Sortiere Datensätze nach der ID (numerisch)
    dataset.sort(key=lambda x: x['id'])
    return dataset

# API: Nächster Datensatz
@app.route('/get_car', methods=['GET'])
def get_car():
    dataset = load_data()
    
    # Verwende den Request-Parameter `id` oder setze ihn auf 1, wenn nicht angegeben
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

    car = next((item for item in load_data() if item['id'] == data['car_id']), None)
    if car:
        car_features = [car['mileage_ml'], car['power_ml'], car['transmission_ml']]
        model.update(car_features, data['action'])

    # Speichere Feedback in einer Datei
    with open('feedback.json', 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, indent=4)

    return jsonify({'status': 'success'})

# API: Vorhersage für ein spezifisches Auto
@app.route('/predict/<int:car_id>', methods=['GET'])
def predict(car_id):
    car = next((item for item in load_data() if item['id'] == car_id), None)
    if car:
        car_features = [car['mileage_ml'], car['power_ml'], car['transmission_ml']]
        if len(set(model.y)) <= 1 or len(model.X) < model.min_samples:  # Ensure there are at least two classes and enough samples
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
    app.run(debug=True, host='0.0.0.0')