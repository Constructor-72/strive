import os
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction import DictVectorizer

# Initialisieren des Modells und der Hilfsstrukturen
base_model = SGDClassifier(loss="log", learning_rate="optimal")
model = CalibratedClassifierCV(base_model, cv="prefit")
vectorizer = DictVectorizer(sparse=False)

# Variable zum Tracking, ob das Modell schon initialisiert wurde
is_initialized = False

# Funktion zur Verarbeitung eines Textfiles
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Daten aus der Datei extrahieren
    data = {}
    for line in lines:
        key, value = line.split(": ", 1)
        data[key.strip()] = value.strip()

    return {
        "price": float(data["Price"].replace(".", "").replace(",", ".").replace("\u20ac", "")),
        "mileage": int(data["Mileage"].replace(".", "").replace(",", "")),
        "power": int(data["Power"]),
        "first_registration": int(data["First Registration"].split(".")[1]),
        "transmission": data["Transmission"],
        "color": data["Color"],
        "owners": int(data["Owners"]),
    }

# Funktion zur Verarbeitung neuer Daten und zur Generierung von Vorhersagen
def predict_and_learn(sample, feedback=None):
    global is_initialized, base_model, model, vectorizer

    # Vektorisieren der Daten
    sample_vectorized = vectorizer.transform([sample]) if is_initialized else vectorizer.fit_transform([sample])

    if is_initialized:
        # Vorhersage basierend auf den Eingabedaten
        prediction = model.predict(sample_vectorized)[0]
        confidence = model.predict_proba(sample_vectorized)[0][prediction]
        print(f"Prediction: {'True' if prediction == 1 else 'False'}, Confidence: {confidence:.2f}")
    else:
        prediction = 1  # Dummy-Vorhersage für die erste Runde
        print("Prediction: True (default), Confidence: N/A")

    # Feedback verarbeiten und Modell aktualisieren
    if feedback is not None:
        feedback_label = 1 if feedback else 0
        if feedback_label != prediction:
            if not is_initialized:
                base_model.partial_fit(sample_vectorized, [feedback_label], classes=[0, 1])
                model = CalibratedClassifierCV(base_model, cv="prefit")
                is_initialized = True
            else:
                base_model.partial_fit(sample_vectorized, [feedback_label])
                model.fit(sample_vectorized, [feedback_label])
            print("Model updated with feedback.")
        else:
            print("No update needed as the feedback matches the prediction.")

# Hauptfunktion zur Verarbeitung eines Ordners mit Dateien
def process_folder(folder_path):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')], key=lambda x: int(x.split('.')[0]))

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        print(f"Processing file: {file_name}")
        
        sample = process_file(file_path)
        predict_and_learn(sample)  # Modell macht Vorhersage

        while True:
            feedback = input("What should the correct label be? (true/false): ").strip().lower()
            if feedback in ["true", "false"]:
                predict_and_learn(sample, feedback=(feedback == "true"))
                break
            else:
                print("Invalid input. Please enter 'true' or 'false'.")

# Beispiel: Ordner mit Textdateien verarbeiten
folder_path = input("Enter the folder path containing the txt files: ").strip()
process_folder(folder_path)
