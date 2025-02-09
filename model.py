import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler

class CarPredictionModel:
    def __init__(self):
        self.model = self._build_model()
        self.X = []
        self.y = []
        self.min_samples = 25  # Mindestanzahl an Bewertungen
        self.scaler = StandardScaler()

    def _build_model(self):
        model = Sequential([
            Dense(128, activation='relu', input_shape=(7,)),  # 7 Eingabefeatures
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
            X_scaled = self.scaler.fit_transform(np.array(self.X))
            early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
            self.model.fit(X_scaled, np.array(self.y), epochs=200, batch_size=32, verbose=0, callbacks=[early_stopping])

    def predict(self, car_features):
        # Prüfen, ob das Modell ausreichend trainiert wurde
        if len(set(self.y)) <= 1 or len(self.X) < self.min_samples:
            return 'Keine eindeutige Vorhersage möglich.', None
        car_features_scaled = self.scaler.transform(np.array([car_features]))
        prediction = self.model.predict(car_features_scaled)[0][0]
        confidence = prediction if prediction >= 0.5 else 1 - prediction
        return ('Ja' if prediction >= 0.5 else 'Nein'), confidence * 100

    def update(self, car_features, feedback):
        # Trainingsdaten aktualisieren
        self.X.append(car_features)
        self.y.append(1 if feedback == 'like' else 0)
        self.train()

model = CarPredictionModel()
