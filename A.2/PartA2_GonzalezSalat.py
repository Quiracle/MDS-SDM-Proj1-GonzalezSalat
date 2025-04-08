import preprocessing.apicall as apicall
import preprocessing.generateconference as generateconference
import preprocessing.generateeditionpertains as generateeditionpertains
import preprocessing.generateevent as generateevent
import preprocessing.generateperson as generateperson
import preprocessing.generatereviews as generatereviews
import preprocessing.generatevolumejournal as generatevolumejournal

import os
import shutil

def copy_to_import_folder(src_folder, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)

    for filename in os.listdir(src_folder):
        if filename.endswith(".csv"):
            src_path = os.path.join(src_folder, filename)
            dest_path = os.path.join(dest_folder, filename)
            shutil.copy2(src_path, dest_path)
            print(f"✅ Copied: {filename}")

    print("📁 All CSV files copied successfully.")

def main():
    apicall.main()
    generateconference.main()
    generateevent.main()
    generateeditionpertains.main()
    generateperson.main()
    generatereviews.main()
    generatevolumejournal.main()

    # Ahora el script está en A.2/, así que accede a preprocessing/data/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, "preprocessing", "data")
    destination = os.path.join(script_dir, "../neo4j_project/import")

    copy_to_import_folder(source, destination)

if __name__ == '__main__':
    main()
