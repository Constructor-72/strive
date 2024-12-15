import shutil
import os

# Pfad zum Originalbild (ersetze dies mit dem tatsächlichen Bildpfad)
input_image_path = 'data/image.jpg'

# Überprüfe, ob das Bild existiert
if not os.path.isfile(input_image_path):
    print(f"Die Datei {input_image_path} wurde nicht gefunden. Aktuelles Verzeichnis: {os.getcwd()}")
else:
    # Verzeichnis, in dem die neuen Bilder gespeichert werden sollen
    output_dir = 'data'

    # Sicherstellen, dass das Verzeichnis existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Kopiere das Bild und speichere es unter neuen Namen (1.jpg bis 20.jpg)
    for i in range(1, 21):
        output_image_path = os.path.join(output_dir, f'{i}.jpg')
        shutil.copy(input_image_path, output_image_path)

    print("20 Bilder wurden erfolgreich erstellt und gespeichert.")
