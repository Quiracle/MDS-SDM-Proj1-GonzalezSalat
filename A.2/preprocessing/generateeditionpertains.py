import csv

# Entradas y salida
INPUT_EDITION = "data/edition_nodes.csv"              # Tiene edition_id
INPUT_EDITION_EVENT = "data/edition_pertains_event.csv"  # Edition → Venue
OUTPUT_REL = "data/edition_pertains_conferenceworkshop.csv"

# Cargar relaciones existentes
rels = []
with open(INPUT_EDITION_EVENT, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        edition = row[":START_ID(Edition)"]
        event = row[":END_ID(Venue)"]
        rels.append([edition, event])  # Reusamos los mismos valores

# Guardar nuevo archivo con tipo ConferenceWorkshop
with open(OUTPUT_REL, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Edition)", ":END_ID(ConferenceWorkshop)"])
    writer.writerows(rels)

print("✅ Archivo 'edition_pertains_conferenceworkshop.csv' generado correctamente.")
