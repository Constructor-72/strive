import os
import random
from datetime import datetime

def generate_random_data():
    """
    Generiert zufällige, aber realistische Daten für Autos.
    """
    # Beispielmarken und Modelle
    car_models = {
        "BMW": ["M5", "X3", "X5", "320i"],
        "Audi": ["A4", "A6", "Q5", "RS5"],
        "Mercedes": ["C200", "E350", "G63", "A180"],
        "Volkswagen": ["Golf", "Passat", "Tiguan", "Polo"],
        "Porsche": ["911", "Cayenne", "Macan", "Panamera"],
    }

    # Zufällige Marke und Modell
    brand = random.choice(list(car_models.keys()))
    model = random.choice(car_models[brand])
    title = f"{brand} {model}"

    # Zufällige Erstzulassung (zwischen 1980 und heute)
    current_year = datetime.now().year
    year = random.randint(2005, current_year)
    month = random.randint(1, 12)
    first_registration = f"{month:02d}.{year}"

    # Kilometerstand, grob passend zum Alter des Autos
    age = current_year - year
    max_mileage = age * 20000 if age > 0 else 5000
    mileage = random.randint(1, max_mileage // 1000) * 1000

    # Preis, abhängig vom Alter des Autos
    if age <= 3:
        price = random.randint(50, 120) * 1000  # Höherer Preis für neuere Autos
    elif age <= 10:
        price = random.randint(20, 50) * 1000  # Mittlerer Preis für mittelalte Autos
    else:
        price = random.randint(1, 20) * 1000  # Niedriger Preis für ältere Autos

    # PS, grob passend zum Modell
    if "M" in model or "RS" in model or "911" in model:
        power = random.randint(300, 700)
    elif "X" in model or "Q" in model or "G" in model:
        power = random.randint(150, 400)
    else:
        power = random.randint(75, 250)

    # Getriebe
    transmission = random.choice(["Automatik", "Schaltgetriebe"])

    # Farbe
    color = random.choice(["Blau", "Gelb", "Grau", "Grün", "Rot", "Schwarz", "Silber", "Weiß", "Andere"])

    # Anzahl der Fahrzeughalter
    owners = random.randint(1, 9)

    return {
        "Title": title,
        "Price": f"{price:,}".replace(",", "."),  # Formatierung mit Punkt statt Komma
        "Mileage": f"{mileage:,}".replace(",", "."),
        "Power": power,
        "First Registration": first_registration,
        "Transmission": transmission,
        "Color": color,
        "Owners": owners,
    }

def create_txt_files(folder_path, num_files):
    """
    Erstellt die angegebene Anzahl an .txt-Dateien mit zufälligen Autodaten.

    Args:
        folder_path (str): Pfad zum Ordner, in dem die Dateien gespeichert werden.
        num_files (int): Anzahl der zu erstellenden Dateien.
    """
    # Sicherstellen, dass der Ordner existiert
    os.makedirs(folder_path, exist_ok=True)

    # Bestehende .txt-Dateien im Ordner finden
    existing_files = [
        int(f.split(".")[0]) for f in os.listdir(folder_path) if f.endswith(".txt") and f.split(".")[0].isdigit()
    ]
    existing_files.sort()

    # Nächste verfügbare Nummer finden
    start_number = existing_files[-1] + 1 if existing_files else 1

    for i in range(start_number, start_number + num_files):
        file_path = os.path.join(folder_path, f"{i}.txt")

        # Daten generieren
        data = generate_random_data()
        
        # Daten in die Datei schreiben
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(
                f"Title: {data['Title']}\n"
                f"Price: {data['Price']}\n"
                f"Mileage: {data['Mileage']}\n"
                f"Power: {data['Power']}\n"
                f"First Registration: {data['First Registration']}\n"
                f"Transmission: {data['Transmission']}\n"
                f"Color: {data['Color']}\n"
                f"Owners: {data['Owners']}\n"
            )
        print(f"Datei {i}.txt erstellt.")

# Beispielaufruf
if __name__ == "__main__":
    folder = input("Geben Sie den Pfad zum Ordner ein: ").strip()
    number_of_files = int(input("Wie viele Dateien sollen erstellt werden? ").strip())
    create_txt_files(folder, number_of_files)