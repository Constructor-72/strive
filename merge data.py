import pandas as pd

def merge_csv(file1, file2, output_file):
    # CSV-Dateien einlesen
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # CSV-Dateien zusammenführen
    merged_df = pd.concat([df1, df2], ignore_index=True)
    
    # Zusammengeführte Daten in eine neue CSV speichern
    merged_df.to_csv(output_file, index=False)
    print(f"Dateien wurden erfolgreich zusammengeführt und in {output_file} gespeichert.")

# Beispielaufruf
merge_csv('data/alt_ford.csv', 'data/focus.csv', 'data/Ford.csv')