import os

def rename_jpg_files(folder_path):
    """
    Rename all .jpg files in the specified folder to be sequentially numbered (1.jpg, 2.jpg, ...).

    Args:
        folder_path (str): Path to the folder containing .jpg files.
    """
    try:
        # List all files in the folder
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

        # Sort files to ensure consistent renaming order
        files.sort()

        # Rename each file with a sequential number
        for index, file in enumerate(files, start=1):
            new_name = f"{index}.jpg"
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)

        print(f"Successfully renamed {len(files)} .jpg files in '{folder_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing .jpg files: ").strip()
    rename_jpg_files(folder_path)