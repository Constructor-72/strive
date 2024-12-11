from flask import Flask, send_from_directory, jsonify, request
import os
import json

app = Flask(__name__, static_folder='.')

DATA_FOLDER = 'data'
feedback_data = []

# Lade Textdaten
def load_text_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Lade Datensätze
def load_data():
    dataset = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith('.txt'):
            data_id = os.path.splitext(file)[0]
            image_path = os.path.join(DATA_FOLDER, f"{data_id}.jpg")
            text_path = os.path.join(DATA_FOLDER, file)
            if os.path.exists(image_path):
                text = load_text_data(text_path)
                dataset.append({'id': data_id, 'image': image_path, 'text': text})
    
    # Sortiere Datensätze nach der ID (numerisch)
    dataset.sort(key=lambda x: int(x['id']))  # Sortiert nach der ID
    return dataset

# API: Nächster Datensatz
@app.route('/get_car', methods=['GET'])
def get_car():
    dataset = load_data()
    
    # Verwende den Request-Parameter `id` oder setze ihn auf 1, wenn nicht angegeben
    current_id = int(request.args.get('id', 1))  # Start bei ID 1, nicht 0

    if current_id - 1 < len(dataset):  # Stellen Sie sicher, dass `current_id` im gültigen Bereich liegt
        car = dataset[current_id - 1]  # Da die Liste bei 0 indiziert ist, subtrahiere 1
        return jsonify({
            'id': car['id'],
            'image': car['image'],
            'details': car['text']
        })
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

    # Speichere Feedback in einer Datei (optional)
    with open('feedback.json', 'w') as f:
        json.dump(feedback_data, f, indent=4)

    return jsonify({'status': 'success'})

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