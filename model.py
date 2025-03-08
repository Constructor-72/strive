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
            'transmission_ml': True,  # Getriebe (Automatik/Manuell)
            'fuel_ml': False,    # Kraftstofftyp
            'tax': False,        # Kfz-Steuer
            'mpg': False,        # Verbrauch (mpg)
            'firstRegistration_ml': True  # Erstzulassung
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
            Dense(128, activation='relu', input_shape=input_shape),  # Eingabefeatures
            BatchNormalization(),
            Dropout(0.5),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(1, activation='sigmoid')  # Ausgabe zwischen 0 und 1
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self):
        # Sicherstellen, dass genug Daten vorhanden sind
        if len(set(self.y)) > 1 and len(self.X) >= self.min_samples:
            # Nur die aktivierten Features verwenden
            X_filtered = self._filter_features(self.X)
            X_scaled = self.scaler.fit_transform(X_filtered)
            early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
            self.model.fit(X_scaled, np.array(self.y), epochs=200, batch_size=32, verbose=0, callbacks=[early_stopping])

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
        # Trainingsdaten aktualisieren
        self.X.append(car_features)
        self.y.append(1 if feedback == 'like' else 0)
        self.train()

    def _filter_features(self, features):
        # Filtert die Features basierend auf der Konfiguration
        filtered_features = []
        for feature_set in features:
            filtered_set = []
            for i, (key, value) in enumerate(self.feature_config.items()):
                if value:  # Nur aktivierte Features hinzufügen
                    filtered_set.append(feature_set[i])
            filtered_features.append(filtered_set)
        return np.array(filtered_features)

# Globale Variable zur Speicherung der Modelle aller Benutzer
user_models = {}