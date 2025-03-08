from flask import Flask, send_from_directory, jsonify, request, session
import os
import json
import pandas as pd
import random
from model import CarPredictionModel
import locale
import bcrypt

app = Flask(__name__, static_folder='.')
app.secret_key = 'your_secret_key'

DATA_FOLDER = 'data'
CHATS_FILE = 'chats.json'
USERS_FILE = 'users.json'
feedback_data = []

dataset = []
user_models = {}

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def load_csv_data_once():
    global dataset
    if dataset:  # Daten sind bereits geladen
        return dataset

    file_path = os.path.join(DATA_FOLDER, 'cars.csv')  # Pfad zur CSV-Datei

    # Lade die CSV-Datei mit Semikolon als Trennzeichen
    df = pd.read_csv(file_path, delimiter=';')

    dataset = []
    for index, row in df.iterrows():
        car_data = {
            'id': int(row['ID']),
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
            'image': f"data/jpg/{row['ID']}_1.jpg" if os.path.exists(f"data/jpg/{row['ID']}_1.jpg") else 'data/gap_filler.jpg',
            'images': [f"data/jpg/{row['ID']}_{i}.jpg" for i in range(1, int(row['numberofpic']) + 1)] if os.path.exists(f"data/jpg/{row['ID']}_1.jpg") else ['data/gap_filler.jpg']
        }
        dataset.append(car_data)

    # Mische die Liste zufällig
    # random.shuffle(dataset)

    return dataset

# API: Lade die Bilder für ein bestimmtes Auto
@app.route('/get_car_images/<int:car_id>', methods=['GET'])
def get_car_images(car_id):
    dataset = load_csv_data_once()
    car = next((item for item in dataset if item['id'] == car_id), None)
    if car:
        return jsonify({'images': car['images']})
    else:
        return jsonify({'status': 'failure', 'message': 'Car not found'}), 404

# Lade Benutzerdaten
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Speichere Benutzerdaten
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# API: Registrierung
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username in users:
        return jsonify({'status': 'failure', 'message': 'Benutzername bereits vergeben'}), 400

    # Hash das Passwort
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    users[username] = {
        'password': hashed_password,  # Speichere das gehashte Passwort
        'likes': [],
        'dislikes': [],
        'chats': []
    }
    save_users(users)
    return jsonify({'status': 'success'})

# API: Anmeldung
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username not in users:
        return jsonify({'status': 'failure', 'message': 'Ungültige Anmeldedaten'}), 400

    # Überprüfe das Passwort
    hashed_password = users[username]['password'].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        session['username'] = username
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure', 'message': 'Ungültige Anmeldedaten'}), 400

# API: Abmeldung
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'status': 'success'})

# API: Überprüfe den Anmeldestatus
@app.route('/check_login', methods=['GET'])
def check_login():
    if 'username' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    else:
        return jsonify({'logged_in': False})

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
    username = session.get('username', 'guest')  # Standard-Nutzer 'guest' verwenden

    data = request.get_json()
    if 'car_id' not in data or 'action' not in data:
        return jsonify({'status': 'failure', 'message': 'Missing car_id or action'}), 400

    users = load_users()
    if username not in users and username != 'guest':
        return jsonify({'status': 'failure', 'message': 'Nicht angemeldet'}), 401

    # Lade das Modell des Benutzers
    if username not in user_models:
        user_models[username] = CarPredictionModel()

    # Aktualisiere Likes/Dislikes in der Benutzerdatenbank (nur für registrierte Benutzer)
    if username != 'guest':
        if data['action'] == 'like':
            users[username]['likes'].append(data['car_id'])
        elif data['action'] == 'dislike':
            users[username]['dislikes'].append(data['car_id'])
        save_users(users)

    # Lade die Auto-Daten
    car = next((item for item in load_csv_data_once() if item['id'] == data['car_id']), None)
    if car:
        # Überprüfen, dass alle 8 Features übergeben werden
        car_features = [
            car['mileage_ml'],           # Kilometerstand
            car['price_ml'],             # Preis
            car['power_ml'],             # Leistung
            car['transmission_ml'],      # Getriebe (1 = Automatik, 0 = Manuell)
            car['fuel_ml'],              # Kraftstofftyp (Hashwert des Kraftstofftyps)
            car['tax'],                  # Kfz-Steuer
            car['mpg'],                  # Verbrauch
            car['firstRegistration_ml']  # Erstzulassung
        ]
        # Aktualisiere das Modell des Benutzers
        user_models[username].update(car_features, data['action'])

    return jsonify({'status': 'success'})

# API: Vorhersage für ein spezifisches Auto
@app.route('/predict/<int:car_id>', methods=['GET'])
def predict(car_id):
    username = session.get('username', 'guest')  # Standard-Nutzer 'guest' verwenden

    if username not in user_models:
        return jsonify({'prediction': 'Keine eindeutige Vorhersage möglich.', 'confidence': None})

    car = next((item for item in load_csv_data_once() if item['id'] == car_id), None)
    if car:
        # Überprüfen, dass alle 8 Features übergeben werden
        car_features = [
            car['mileage_ml'],           # Kilometerstand
            car['price_ml'],             # Preis
            car['power_ml'],             # Leistung
            car['transmission_ml'],      # Getriebe (1 = Automatik, 0 = Manuell)
            car['fuel_ml'],              # Kraftstofftyp (Hashwert des Kraftstofftyps)
            car['tax'],                  # Kfz-Steuer
            car['mpg'],                  # Verbrauch
            car['firstRegistration_ml']  # Erstzulassung
        ]
        print(f"Car Features for ID {car_id}: {car_features}")  # Debugging: Gib die Features aus
        try:
            prediction, confidence = user_models[username].predict(car_features)
            return jsonify({'prediction': prediction, 'confidence': confidence})
        except Exception as e:
            print(f"Fehler bei der Vorhersage für Auto {car_id}: {e}")
            return jsonify({'prediction': 'Keine eindeutige Vorhersage möglich.', 'confidence': None})
    return jsonify({'prediction': 'Keine eindeutige Vorhersage möglich.', 'confidence': None})

# API: Chat-Nachrichten speichern
@app.route('/save_chat', methods=['POST'])
def save_chat():
    if 'username' not in session:
        return jsonify({'status': 'failure', 'message': 'Nicht angemeldet'}), 401

    chat_entry = request.get_json()
    if not chat_entry or 'car_id' not in chat_entry or 'message' not in chat_entry:
        return jsonify({'status': 'failure', 'message': 'Invalid chat data'}), 400

    users = load_users()
    username = session['username']
    users[username]['chats'].append(chat_entry)
    save_users(users)

    return jsonify({'status': 'success'})

# API: Chat-Übersicht laden
@app.route('/get_chats', methods=['GET'])
def get_chats():
    if 'username' not in session:
        return jsonify({'status': 'failure', 'message': 'Nicht angemeldet'}), 401

    users = load_users()
    username = session['username']
    return jsonify(users[username]['chats'])

# API: Chat-Nachrichten für ein Auto laden
@app.route('/get_chat_messages/<int:car_id>', methods=['GET'])
def get_chat_messages(car_id):
    if 'username' not in session:
        return jsonify({'status': 'failure', 'message': 'Nicht angemeldet'}), 401

    users = load_users()
    username = session['username']
    car_chats = [chat for chat in users[username]['chats'] if chat['car_id'] == car_id]
    return jsonify(car_chats)

# Hauptseite
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Statische Dateien
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    # Stelle sicher, dass die chats.json-Datei existiert und ein gültiges JSON-Array enthält
    if not os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)  # Erstelle eine leere JSON-Array-Datei

    load_csv_data_once()  # Lade Daten einmalig beim Start
    app.run(debug=True, host='0.0.0.0')