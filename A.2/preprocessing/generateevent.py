import csv
import random

# Archivos de entrada
INPUT_PAPERS = "data/paper_nodes.csv"
INPUT_PUBLISHED_IN = "data/paper_published_in.csv"  # Paper → Venue
OUTPUT_EDITION = "data/edition_nodes.csv"
OUTPUT_PUBLISHED_IN_ED = "data/paper_published_in_edition.csv"
OUTPUT_PERTAINS = "data/edition_pertains_event.csv"

# Ciudades sintéticas
cities = ["Barcelona", "London", "Tokyo", "New York", "Paris", "Berlin", "Amsterdam", "Lisbon"]

# Mapas auxiliares
paper_year = {}
paper_venue = {}

# 1. Leer año por paper
with open(INPUT_PAPERS, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        paper_year[row["paper_id:ID(Paper)"]] = row["year:INT"]

# 2. Leer venue por paper
with open(INPUT_PUBLISHED_IN, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        paper = row[":START_ID(Paper)"]
        venue = row[":END_ID(Venue)"]
        paper_venue[paper] = venue

# 3. Generar ediciones únicas
edition_map = {}  # (venue, year) -> edition_id
edition_rows = []
paper_ed_rels = []
edition_event_rels = []

for paper, venue in paper_venue.items():
    year = paper_year.get(paper)
    if not year:
        continue

    ed_key = (venue, year)
    ed_id = f"{venue.replace(' ', '_')}_{year}"

    if ed_key not in edition_map:
        city = random.choice(cities)
        proceedings = f"Proceedings of {venue} {year}"
        edition_rows.append([ed_id, year, city, proceedings])
        edition_event_rels.append([ed_id, venue])
        edition_map[ed_key] = ed_id

    paper_ed_rels.append([paper, edition_map[ed_key]])

# 4. Guardar edition_nodes.csv
with open(OUTPUT_EDITION, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["edition_id:ID(Edition)", "year:INT", "city", "proceeding"])
    writer.writerows(edition_rows)

# 5. Guardar paper_published_in_edition.csv
with open(OUTPUT_PUBLISHED_IN_ED, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Paper)", ":END_ID(Edition)"])
    writer.writerows(paper_ed_rels)

# 6. Guardar edition_pertains_event.csv
with open(OUTPUT_PERTAINS, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Edition)", ":END_ID(Venue)"])
    writer.writerows(edition_event_rels)

print("✅ Nodos Edition y relaciones generadas correctamente")
