import csv
import random

# Entradas
PAPER_NODES = "data/paper_nodes.csv"
VENUE_NODES = "data/venue_nodes.csv"
PAPER_PUBLISHED_IN = "data/paper_published_in.csv"

# Salidas
VOLUME_NODES = "data/volume_nodes.csv"
JOURNAL_NODES = "data/journal_nodes.csv"
PAPER_PUBLISHED_IN_VOLUME = "data/paper_published_in_volume.csv"
VOLUME_PERTAINS_JOURNAL = "data/volume_pertains_journal.csv"

# Generar organizaciones sintéticas
orgs = [
    "ACM Press", "IEEE Publishing", "Elsevier", "Springer", "Oxford Press"
]

# 1. Leer tipo de venue
venue_type = {}
with open(VENUE_NODES, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        venue_type[row["venue_name:ID(Venue)"]] = row["type"]

# 2. Leer año y venue por paper
paper_to_year = {}
with open(PAPER_NODES, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        paper_to_year[row["paper_id:ID(Paper)"]] = row["year:INT"]

paper_to_venue = {}
with open(PAPER_PUBLISHED_IN, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        paper_to_venue[row[":START_ID(Paper)"]] = row[":END_ID(Venue)"]

# 3. Generar nodos Volume y Journal
volume_map = {}
journal_map = {}
paper_vol_rels = []
vol_jour_rels = []

for paper, venue in paper_to_venue.items():
    if venue_type.get(venue) != "Journal":
        continue

    year = paper_to_year.get(paper)
    if not year:
        continue

    volume_id = f"{venue}_Vol{year}"
    journal_id = venue

    if volume_id not in volume_map:
        volume_map[volume_id] = year
        if journal_id not in journal_map:
            journal_map[journal_id] = random.choice(orgs)
        vol_jour_rels.append([volume_id, journal_id])

    paper_vol_rels.append([paper, volume_id])

# 4. Guardar volume_nodes.csv
with open(VOLUME_NODES, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["volume_id:ID(Volume)", "number", "year:INT"])
    for vid, year in volume_map.items():
        writer.writerow([vid, vid.split("_Vol")[-1], year])

# 5. Guardar journal_nodes.csv
with open(JOURNAL_NODES, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["journal_id:ID(Journal)", "organization"])
    for jid, org in journal_map.items():
        writer.writerow([jid, org])

# 6. Guardar paper_published_in_volume.csv
with open(PAPER_PUBLISHED_IN_VOLUME, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Paper)", ":END_ID(Volume)"])
    writer.writerows(paper_vol_rels)

# 7. Guardar volume_pertains_journal.csv
with open(VOLUME_PERTAINS_JOURNAL, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Volume)", ":END_ID(Journal)"])
    writer.writerows(vol_jour_rels)

print("✅ Volumes y Journals generados correctamente.")
