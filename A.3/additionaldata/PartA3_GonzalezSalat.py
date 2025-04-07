import extendreviews, generateorganizations
import os
import shutil


def copy_to_import_folder(src_folder, dest_folder):
    # Ensure destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # List all CSV files in the source folder
    for filename in os.listdir(src_folder):
        if filename.endswith(".csv"):
            src_path = os.path.join(src_folder, filename)
            dest_path = os.path.join(dest_folder, filename)
            shutil.copy2(src_path, dest_path)
            print(f"✅ Copied: {filename}")

    print("📁 All CSV files copied successfully.")

def main():
    extendreviews.main()
    generateorganizations.main()

    # Get the absolute path of the folder where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set relative paths from the script's directory
    source = os.path.join(script_dir, ".")
    destination = os.path.join(script_dir, "../../neo4j_project/import")

    copy_to_import_folder(source, destination)

if __name__ == '__main__':
    main()