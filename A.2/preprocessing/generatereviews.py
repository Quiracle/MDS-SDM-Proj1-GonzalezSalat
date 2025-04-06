import csv
import random
from collections import defaultdict

# Archivos
INPUT_PERSON = "data/person_nodes.csv"
INPUT_WROTE = "data/author_wrote.csv"
INPUT_CORR = "data/corresponding_author.csv"
INPUT_PAPERS = "data/paper_nodes.csv"
OUTPUT_REVIEWS = "data/reviewer_reviews.csv"

# Número de reviewers por paper
NUM_REVIEWERS = 2

# 1. Cargar todos los person_id
all_person_ids = set()
with open(INPUT_PERSON, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_person_ids.add(row["person_id:ID(Person)"])

# 2. Cargar autores y corresponding authors por paper
paper_to_blocked_reviewers = defaultdict(set)

for file in [INPUT_WROTE, INPUT_CORR]:
    with open(file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            person = row[":START_ID(Person)"]
            paper = row[":END_ID(Paper)"]
            paper_to_blocked_reviewers[paper].add(person)

# 3. Cargar lista de papers
all_papers = []
with open(INPUT_PAPERS, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_papers.append(row["paper_id:ID(Paper)"])

# 4. Generar relaciones REVIEWS
reviews = []

for paper in all_papers:
    blocked = paper_to_blocked_reviewers.get(paper, set())
    eligible_reviewers = list(all_person_ids - blocked)

    # Evitar errores si hay menos reviewers disponibles
    num_to_sample = min(NUM_REVIEWERS, len(eligible_reviewers))
    selected_reviewers = random.sample(eligible_reviewers, num_to_sample)

    for reviewer in selected_reviewers:
        reviews.append((reviewer, paper))

# 5. Guardar archivo
with open(OUTPUT_REVIEWS, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Person)", ":END_ID(Paper)"])
    writer.writerows(reviews)

print(f"✅ Relaciones REVIEWS generadas: {len(reviews)} totales.")
print(f"📄 Archivo guardado como: {OUTPUT_REVIEWS}")
