import os
import shutil
import random

def duplicate_txt_files(folder_path):
    """
    Dupliziert alle .txt-Dateien in einem Ordner und benennt sie fortlaufend um (in zufälliger Reihenfolge).

    Args:
        folder_path (str): Pfad zum Ordner mit den .txt-Dateien.
    """
    try:
        # Bestehende .txt-Dateien finden und sortieren
        txt_files = [
            f for f in os.listdir(folder_path) if f.endswith(".txt") and f.split(".")[0].isdigit()
        ]
        txt_files.sort(key=lambda x: int(x.split(".")[0]))

        if not txt_files:
            print("Keine .txt-Dateien im Ordner gefunden.")
            return

        # Höchste bestehende Nummer bestimmen
        max_number = int(txt_files[-1].split(".")[0])

        # Dateien duplizieren und umbenennen
        new_numbers = list(range(max_number + 1, max_number + len(txt_files) + 1))
        random.shuffle(new_numbers)  # Zufällige Reihenfolge

        for i, file_name in enumerate(txt_files):
            original_path = os.path.join(folder_path, file_name)
            new_file_name = f"{new_numbers[i]}.txt"
            new_path = os.path.join(folder_path, new_file_name)

            shutil.copy(original_path, new_path)
            print(f"{file_name} -> {new_file_name}")

        print(f"Alle Dateien wurden erfolgreich dupliziert und umbenannt.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispielaufruf
if __name__ == "__main__":
    folder = input("Geben Sie den Pfad zum Ordner ein: ").strip()
    duplicate_txt_files(folder)
