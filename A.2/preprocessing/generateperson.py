import csv
import random

# Archivos de entrada
INPUT_RAW = "data/person_nodes_raw.csv"  # id + name
INPUT_WRITES = "data/author_wrote.csv"
INPUT_CORR = "data/corresponding_author.csv"

# Archivo de salida
OUTPUT_PERSON = "data/person_nodes.csv"

# Universidades sintéticas
universities = [
    "University of Neo4j", "GraphTech Institute", "Semantic U",
    "Knowledge Graph University", "Data Science College"
]

# 1. Cargar nombres desde el archivo raw
id_to_name = {}
with open(INPUT_RAW, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row["person_id:ID(Person)"]
        name = row["name"]
        id_to_name[pid] = name

# 2. Extraer todos los person_id únicos desde relaciones
person_ids = set()

for file in [INPUT_WRITES, INPUT_CORR]:
    with open(file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_ids.add(row[":START_ID(Person)"])

# 3. Crear nodos con atributos
rows = []
for pid in sorted(person_ids):
    name = id_to_name.get(pid, "Unknown")
    email = name.lower().replace(" ", ".") + "@example.edu"
    org = random.choice(universities)
    rows.append([pid, name, email, org])

# 4. Guardar el CSV final
with open(OUTPUT_PERSON, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["person_id:ID(Person)", "name", "email", "organization"])
    writer.writerows(rows)

print(f"✅ Archivo generado: {OUTPUT_PERSON}")

