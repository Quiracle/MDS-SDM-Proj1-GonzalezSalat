import csv
import random
import os

# ⚙️ Configuración de rutas
INPUT_PAPERS = os.path.join("..", "..", "A.2", "preprocessing", "data", "paper_nodes.csv")
OUTPUT_REVIEWS = os.path.join(os.path.dirname(__file__), "review_nodes.csv")
NUM_REVIEWS_PER_PAPER = 3
DECISION_CHOICES = ["Approved", "Denied"]
DECISION_PROBABILITIES = [0.7, 0.3]

# Clasificamos los contenidos según sentimiento
POSITIVE_CONTENT = [
    "Excellent contribution to the field.",
    "Well-written and clearly presented.",
    "Good insights and results."
]

NEGATIVE_CONTENT = [
    "Needs stronger experimental support.",
    "Interesting but lacks novelty.",
    "The methodology is flawed.",
    "Insufficient comparison to related work."
]


# 📄 Leer los paper_id
paper_ids = []
with open(INPUT_PAPERS, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        paper_ids.append(row["paper_id:ID(Paper)"])


# Generar reviews con coherencia
rows = []
review_id_counter = 1
for paper_id in paper_ids:
    for _ in range(NUM_REVIEWS_PER_PAPER):
        if random.random() < 0.7:  # 70% de reviews positivas
            content = random.choice(POSITIVE_CONTENT)
            decision = "Approved"
        else:
            content = random.choice(NEGATIVE_CONTENT)
            decision = "Denied"
        review_id = f"r{review_id_counter}"
        rows.append([review_id, content, decision])
        review_id_counter += 1


# 💾 Guardar CSV
with open(OUTPUT_REVIEWS, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["review_id:ID(Review)", "content", "suggested_decision"])
    writer.writerows(rows)

print(f"✅ Archivo generado: {OUTPUT_REVIEWS} con {len(rows)} reviews")
