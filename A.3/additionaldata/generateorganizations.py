import csv
import os
import random

BASE = os.path.dirname(__file__)

INPUT_PERSONS = os.path.join("..", "..", "A.2", "preprocessing", "data", "person_nodes.csv")

OUTPUT_ORGS = os.path.join(BASE, "organization_nodes.csv")
OUTPUT_AFFILIATIONS = os.path.join(BASE, "person_affiliated_with.csv")

# 10 organizaciones reales
orgs = [
    ("org1", "Stanford University", "University"),
    ("org2", "MIT", "University"),
    ("org3", "University of Cambridge", "University"),
    ("org4", "ETH Zurich", "University"),
    ("org5", "Tsinghua University", "University"),
    ("org6", "Google", "Company"),
    ("org7", "Microsoft Research", "Company"),
    ("org8", "Meta AI", "Company"),
    ("org9", "IBM Research", "Company"),
    ("org10", "OpenAI", "Company")
]

# 💾 Guardar nodos de organizaciones
with open(OUTPUT_ORGS, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["organization_id:ID(Organization)", "name", "type"])
    writer.writerows(orgs)

# 📄 Cargar persons
with open(INPUT_PERSONS, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    person_ids = [row["person_id:ID(Person)"] for row in reader]

# 🔗 Asignar aleatoriamente organizaciones
affiliations = []
for pid in person_ids:
    org_id = random.choice(orgs)[0]
    affiliations.append([pid, org_id])

# 💾 Guardar relaciones
with open(OUTPUT_AFFILIATIONS, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Person)", ":END_ID(Organization)"])
    writer.writerows(affiliations)

print("✅ Archivos generados con instituciones reales:")
print(f" - {OUTPUT_ORGS}")
print(f" - {OUTPUT_AFFILIATIONS}")
