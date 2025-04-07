import csv
import os
import random

BASE = os.path.dirname(__file__)

INPUT_CONF = os.path.join("..", "..", "A.2", "preprocessing", "data", "conferenceworkshop_nodes.csv")
INPUT_JOUR = os.path.join("..", "..", "A.2", "preprocessing", "data", "journal_nodes.csv")

OUTPUT_CONF_REL = os.path.join(BASE, "conference_has_reviewpolicy.csv")
OUTPUT_JOUR_REL = os.path.join(BASE, "journal_has_reviewpolicy.csv")

REVIEW_POLICIES = ["rp1", "rp2", "rp3"]

# 📄 Leer conferencias y asignar política
with open(INPUT_CONF, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    conf_rows = [[row["name:ID(ConferenceWorkshop)"], random.choice(REVIEW_POLICIES)] for row in reader]


# 📄 Leer journals y asignar política
with open(INPUT_JOUR, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    jour_rows = [[row["journal_id:ID(Journal)"], random.choice(REVIEW_POLICIES)] for row in reader]


# 💾 Guardar relaciones
with open(OUTPUT_CONF_REL, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(ConferenceWorkshop)", ":END_ID(ReviewPolicy)"])
    writer.writerows(conf_rows)

with open(OUTPUT_JOUR_REL, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Journal)", ":END_ID(ReviewPolicy)"])
    writer.writerows(jour_rows)

print("✅ Relaciones generadas:")
print(f" - {OUTPUT_CONF_REL}")
print(f" - {OUTPUT_JOUR_REL}")
