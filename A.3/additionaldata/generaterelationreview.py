import csv
import random
import os
from collections import defaultdict

# Paths relativos a A.3/additionaldata
BASE = os.path.dirname(__file__)
REVIEW_NODES = os.path.join(BASE, "review_nodes.csv")
PAPER_NODES = os.path.join("..", "..", "A.2", "preprocessing", "data", "paper_nodes.csv")
AUTHOR_WROTE = os.path.join("..", "..", "A.2", "preprocessing", "data", "author_wrote.csv")
CORR_AUTHOR = os.path.join("..", "..", "A.2", "preprocessing", "data", "corresponding_author.csv")
PERSON_NODES = os.path.join("..", "..", "A.2", "preprocessing", "data", "person_nodes.csv")

OUTPUT_REVIEW_REL = os.path.join(BASE, "review_reviews_paper.csv")
OUTPUT_WRITES_REVIEW = os.path.join(BASE, "person_writes_review.csv")

# 📄 Cargar lista de reviews
reviews = []
with open(REVIEW_NODES, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reviews.append(row["review_id:ID(Review)"])

# 📄 Cargar paper_ids en orden
paper_ids = []
with open(PAPER_NODES, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        paper_ids.append(row["paper_id:ID(Paper)"])

# Crear diccionario para autores y corresponding authors
paper_to_authors = defaultdict(set)

# 📄 Cargar autores (WROTE)
with open(AUTHOR_WROTE, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        person_id = row[":START_ID(Person)"]
        paper_id = row[":END_ID(Paper)"]
        paper_to_authors[paper_id].add(person_id)

# 📄 Cargar corresponding authors
with open(CORR_AUTHOR, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        person_id = row[":START_ID(Person)"]
        paper_id = row[":END_ID(Paper)"]
        paper_to_authors[paper_id].add(person_id)

# 📄 Cargar todos los posibles revisores
all_reviewers = []
with open(PERSON_NODES, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_reviewers.append(row["person_id:ID(Person)"])

# 🧠 Generar relaciones
review_reviews_paper = []
person_writes_review = []

assert len(reviews) == len(paper_ids) * 3, "❌ No tienes 3 reviews por paper."

review_index = 0
for paper_id in paper_ids:
    disqualified_reviewers = paper_to_authors.get(paper_id, set())
    reviewers_for_paper = []

    for _ in range(3):
        possible_reviewers = list(set(all_reviewers) - disqualified_reviewers - set(reviewers_for_paper))
        if not possible_reviewers:
            raise Exception(f"No hay revisores válidos para el paper {paper_id}.")
        reviewer = random.choice(possible_reviewers)
        reviewers_for_paper.append(reviewer)

        review_id = reviews[review_index]
        review_reviews_paper.append([review_id, paper_id])
        person_writes_review.append([reviewer, review_id])
        review_index += 1

# 💾 Guardar review_reviews_paper.csv
with open(OUTPUT_REVIEW_REL, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Review)", ":END_ID(Paper)"])
    writer.writerows(review_reviews_paper)

# 💾 Guardar person_writes_review.csv
with open(OUTPUT_WRITES_REVIEW, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Person)", ":END_ID(Review)"])
    writer.writerows(person_writes_review)

print("✅ Archivos generados:")
print(f" - {OUTPUT_REVIEW_REL}")
print(f" - {OUTPUT_WRITES_REVIEW}")
