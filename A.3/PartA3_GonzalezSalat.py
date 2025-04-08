import additionaldata.extendreviews as extendreviews
import additionaldata.generateorganizations as generateorganizations
import os
import shutil


def copy_to_import_folder(src_folder, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)

    for filename in os.listdir(src_folder):
        if filename.endswith(".csv"):
            src_path = os.path.join(src_folder, filename)
            dest_path = os.path.join(dest_folder, filename)
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {filename}")

    print("📁 All CSV files copied successfully.")

def main():
    extendreviews.main()
    generateorganizations.main()

    # Ahora el script está en A.3/, accede a additionaldata/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, "additionaldata")
    destination = os.path.join(script_dir, "../neo4j_project/import")

    copy_to_import_folder(source, destination)

if __name__ == '__main__':
    main()
