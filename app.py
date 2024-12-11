from flask import Flask, send_from_directory, jsonify, request
import os
import json

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
            elif line.startswith('Mileage:'):
                car_data['mileage'] = line.replace('Mileage:', '').strip()
            elif line.startswith('Power:'):
                car_data['power'] = line.replace('Power:', '').strip()
            elif line.startswith('First Registration:'):
                car_data['firstRegistration'] = line.replace('First Registration:', '').strip()
            elif line.startswith('Transmission:'):
                car_data['transmission'] = line.replace('Transmission:', '').strip()
            elif line.startswith('Color:'):
                car_data['color'] = line.replace('Color:', '').strip()
            elif line.startswith('Owners:'):
                car_data['owners'] = line.replace('Owners:', '').strip()
    return car_data

# Lade Datensätze
def load_data():
    dataset = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith('.txt'):
            data_id = os.path.splitext(file)[0]
            image_path = os.path.join(DATA_FOLDER, f"{data_id}.jpg")
            text_path = os.path.join(DATA_FOLDER, file)
            if os.path.exists(image_path):
                # Textdaten laden und die Felder extrahieren
                car_data = load_text_data(text_path)
                car_data['id'] = int(data_id)
                car_data['image'] = f"/data/{data_id}.jpg"
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
        return jsonify({'error': 'No more cars available'}), 404

# API: Like oder Dislike
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()

    if 'car_id' not in data or 'action' not in data:
        return jsonify({'status': 'failure', 'message': 'Missing car_id or action'}), 400

    feedback_entry = {'car_id': data['car_id'], 'action': data['action']}
    feedback_data.append(feedback_entry)

    # Speichere Feedback in einer Datei
    with open('feedback.json', 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, indent=4)

    return jsonify({'status': 'success'})

# Vorhersage-Endpunkt
@app.route('/predict', methods=['GET'])
def predict():
    # Wenn kein Feedback existiert, eine einfache zufällige Vorhersage treffen
    if not feedback_data:
        return jsonify({'title': None})

    # Berechne basierend auf Feedback eine einfache Vorhersage
    like_count = sum(1 for entry in feedback_data if entry['action'] == 'like')
    dislike_count = sum(1 for entry in feedback_data if entry['action'] == 'dislike')

    # Beispiel-Logik für Vorhersage: Bei mehr "Likes" als "Dislikes" zeigen wir ein Auto mit einer "beliebten" Farbe an.
    if like_count > dislike_count:
        return jsonify({'title': 'Car_with_liked_color'})
    else:
        return jsonify({'title': 'Car_with_disliked_color'})

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
