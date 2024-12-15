import os

def display_jpg_and_collect_data(folder_path):
    """
    Display all .jpg files in the specified folder and collect data via a form for each file.
    Save the data as a .txt file with the same name as the corresponding .jpg file, if it does not already exist.

    Args:
        folder_path (str): Path to the folder containing .jpg files.
    """
    try:
        # List all files in the folder
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

        # Sort files to ensure consistent order
        files.sort()

        # Loop through each file and collect data
        for file in files:
            txt_filename = os.path.splitext(file)[0] + ".txt"
            txt_path = os.path.join(folder_path, txt_filename)

            # Skip if .txt file already exists
            if os.path.exists(txt_path):
                print(f"Skipping {file}, corresponding .txt file already exists.")
                continue

            print(f"Processing file: {file}")
            
            # Collect data via form
            title = input("Enter title: ").strip()
            price = input("Enter price: ").strip()
            mileage = input("Enter mileage (Kilometerstand): ").strip()
            power = input("Enter power (Leistung): ").strip()
            first_registration = input("Enter first registration (Erstzulassung): ").strip()
            transmission = input("Enter transmission (Getriebe): ").strip()
            color = input("Enter color (Farbe): ").strip()
            owners = input("Enter number of vehicle owners (Anzahl der Fahrzeughalter): ").strip()

            # Prepare data string
            data = (
                f"Title: {title}\n"
                f"Price: {price}\n"
                f"Mileage: {mileage}\n"
                f"Power: {power}\n"
                f"First Registration: {first_registration}\n"
                f"Transmission: {transmission}\n"
                f"Color: {color}\n"
                f"Owners: {owners}\n"
            )

            # Save data to a .txt file with the same name as the .jpg file
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(data)

        print(f"Data successfully collected and saved for {len(files)} .jpg files in '{folder_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing .jpg files: ").strip()
    display_jpg_and_collect_data(folder_path)
