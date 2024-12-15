import os

# Fahrzeugdaten für die Textdateien
car_data = [
    "Kilometerstand: 10.000 km\nLeistung: 150 PS\nErstzulassung: 01/2018\nGetriebe: Automatik\nFarbe: Schwarz",
    "Kilometerstand: 25.000 km\nLeistung: 120 PS\nErstzulassung: 03/2019\nGetriebe: Manuell\nFarbe: Silber",
    "Kilometerstand: 5.000 km\nLeistung: 200 PS\nErstzulassung: 07/2020\nGetriebe: Automatik\nFarbe: Rot",
    "Kilometerstand: 50.000 km\nLeistung: 110 PS\nErstzulassung: 10/2017\nGetriebe: Manuell\nFarbe: Silber",
    "Kilometerstand: 15.000 km\nLeistung: 180 PS\nErstzulassung: 08/2021\nGetriebe: Automatik\nFarbe: Grau",
    "Kilometerstand: 30.000 km\nLeistung: 90 PS\nErstzulassung: 05/2016\nGetriebe: Manuell\nFarbe: Silber",
    "Kilometerstand: 70.000 km\nLeistung: 140 PS\nErstzulassung: 06/2015\nGetriebe: Automatik\nFarbe: Schwarz",
    "Kilometerstand: 40.000 km\nLeistung: 130 PS\nErstzulassung: 09/2018\nGetriebe: Manuell\nFarbe: Weiß",
    "Kilometerstand: 20.000 km\nLeistung: 170 PS\nErstzulassung: 12/2019\nGetriebe: Automatik\nFarbe: Blau",
    "Kilometerstand: 10.000 km\nLeistung: 100 PS\nErstzulassung: 04/2020\nGetriebe: Manuell\nFarbe: Rot",
    "Kilometerstand: 55.000 km\nLeistung: 160 PS\nErstzulassung: 01/2017\nGetriebe: Automatik\nFarbe: Schwarz",
    "Kilometerstand: 12.000 km\nLeistung: 200 PS\nErstzulassung: 11/2021\nGetriebe: Automatik\nFarbe: Silber",
    "Kilometerstand: 35.000 km\nLeistung: 105 PS\nErstzulassung: 03/2015\nGetriebe: Manuell\nFarbe: Grau",
    "Kilometerstand: 18.000 km\nLeistung: 190 PS\nErstzulassung: 02/2020\nGetriebe: Automatik\nFarbe: Weiß",
    "Kilometerstand: 45.000 km\nLeistung: 150 PS\nErstzulassung: 07/2016\nGetriebe: Manuell\nFarbe: Blau",
    "Kilometerstand: 60.000 km\nLeistung: 120 PS\nErstzulassung: 06/2018\nGetriebe: Automatik\nFarbe: Silber",
    "Kilometerstand: 22.000 km\nLeistung: 175 PS\nErstzulassung: 09/2019\nGetriebe: Manuell\nFarbe: Schwarz",
    "Kilometerstand: 33.000 km\nLeistung: 140 PS\nErstzulassung: 01/2021\nGetriebe: Automatik\nFarbe: Grau",
    "Kilometerstand: 80.000 km\nLeistung: 95 PS\nErstzulassung: 05/2014\nGetriebe: Manuell\nFarbe: Silber",
    "Kilometerstand: 7.000 km\nLeistung: 210 PS\nErstzulassung: 10/2022\nGetriebe: Automatik\nFarbe: Blau"
]

# Verzeichnis, in dem die Textdateien gespeichert werden sollen
output_dir = 'data'

# Sicherstellen, dass das Verzeichnis existiert
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Erstellen der Textdateien
for i, data in enumerate(car_data, start=1):
    file_name = f'{i}.txt'
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

print(f'{len(car_data)} Textdateien wurden erstellt im Ordner "{output_dir}".')
