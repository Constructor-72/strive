import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler

class CarPredictionModel:
    def __init__(self):
        # Konfiguration der Features (True = Feature wird verwendet, False = Feature wird ignoriert)
        self.feature_config = {
            'mileage_ml': True,  # Kilometerstand
            'price_ml': True,    # Preis
            'power_ml': False,   # Leistung
            'transmission_ml': False,  # Getriebe (Automatik/Manuell)
            'fuel_ml': False,    # Kraftstofftyp
            'tax': False,        # Kfz-Steuer
            'mpg': False,        # Verbrauch (mpg)
            'firstRegistration_ml': False  # Erstzulassung
        }
        self.model = self._build_model()
        self.X = []  # Features
        self.y = []  # Labels (1 = Like, 0 = Dislike)
        self.min_samples = 5  # Mindestanzahl an Bewertungen
        self.scaler = StandardScaler()

    def _build_model(self):
        # Anzahl der aktiven Features berechnen
        input_shape = (sum(self.feature_config.values()),)
        
        model = Sequential([
            Dense(64, activation='relu', input_shape=input_shape),  # Eingabefeatures
            BatchNormalization(),
            Dropout(0.6),  # Erhöhte Dropout-Rate
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.6),  # Erhöhte Dropout-Rate
            Dense(32, activation='relu'),
            BatchNormalization(),
            Dropout(0.6),  # Erhöhte Dropout-Rate
            Dense(1, activation='sigmoid')  # Ausgabe zwischen 0 und 1
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self):
        if len(set(self.y)) > 1 and len(self.X) >= self.min_samples:
            X_filtered = self._filter_features(self.X)
            X_scaled = self.scaler.fit_transform(X_filtered)
            y_array = np.array(self.y)
            
            # Aufteilung in Trainings- und Validierungsdaten
            split_index = int(0.8 * len(X_scaled))  # 80% Training, 20% Validierung
            X_train, X_val = X_scaled[:split_index], X_scaled[split_index:]
            y_train, y_val = y_array[:split_index], y_array[split_index:]
            
            early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            self.model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=200, batch_size=32, verbose=0, callbacks=[early_stopping])

    def predict(self, car_features):
        # Prüfen, ob das Modell ausreichend trainiert wurde
        if len(set(self.y)) <= 1 or len(self.X) < self.min_samples:
            return 'Keine eindeutige Vorhersage möglich.', None  # Rückgabe von None für die Konfidenz

        # Nur die aktivierten Features verwenden
        car_features_filtered = self._filter_features([car_features])
        car_features_scaled = self.scaler.transform(car_features_filtered)
        prediction = self.model.predict(car_features_scaled)[0][0]
        confidence = prediction if prediction >= 0.5 else 1 - prediction
        return ('Ja' if prediction >= 0.5 else 'Nein'), confidence * 100

    def update(self, car_features, feedback):
        self.X.append(car_features)
        self.y.append(1 if feedback == 'like' else 0)
        
        # Überprüfen Sie das Gleichgewicht zwischen Likes und Dislikes
        likes = sum(self.y)
        dislikes = len(self.y) - likes
        print(f"Likes: {likes}, Dislikes: {dislikes}")  # Debugging
        
        # Trainieren Sie das Modell nur, wenn genügend Daten vorhanden sind
        if len(self.y) >= self.min_samples:
            self.train()

    def _filter_features(self, features):
        # Filtert die Features basierend auf der Konfiguration
        filtered_features = []
        for feature_set in features:
            filtered_set = []
            for i, (key, value) in enumerate(self.feature_config.items()):
                if value:  # Nur aktivierte Features hinzufügen
                    if i < len(feature_set):  # Überprüfe, ob der Index gültig ist
                        filtered_set.append(feature_set[i])
                    else:
                        print(f"Fehler: Feature {key} nicht in feature_set gefunden.")
                        filtered_set.append(0)  # Standardwert, falls Feature fehlt
            filtered_features.append(filtered_set)
        return np.array(filtered_features)

# Globale Variable zur Speicherung der Modelle aller Benutzer
user_models = {}