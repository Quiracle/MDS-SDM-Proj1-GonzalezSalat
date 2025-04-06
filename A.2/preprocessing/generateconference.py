import csv

# Entrada y salida
INPUT_VENUE = "data/venue_nodes.csv"
OUTPUT_CW = "data/conferenceworkshop_nodes.csv"

# Leer venues
conference_names = set()
with open(INPUT_VENUE, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        venue = row["venue_name:ID(Venue)"]
        conference_names.add(venue)

# Guardar como conferenceworkshop_nodes.csv
with open(OUTPUT_CW, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name:ID(ConferenceWorkshop)"])
    for name in sorted(conference_names):
        writer.writerow([name])

print("✅ Archivo 'conferenceworkshop_nodes.csv' generado correctamente.")
