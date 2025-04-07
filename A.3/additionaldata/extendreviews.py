import csv
import random
import os

# ⚙️ Configuración de rutas
INPUT_REVIEWS = os.path.join("..", "..", "neo4j_project", "import", "reviews.csv")
OUTPUT_REVIEWS = os.path.join(os.path.dirname(__file__), "reviews_extended.csv")
DECISION_CHOICES = ["Approved", "Denied"]

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

def load_reviews(input_path):
    reviews = []
    papers_positives = {}
    with open(input_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reviews.append((row["person_id"], row["paper_id"]))
            papers_positives[row["paper_id"]] = 0
    return reviews, papers_positives

def generate_reviews(reviews, papers_positives, pos_texts, neg_texts):
    generated = []
    for person_id, paper_id in reviews:
        chance = 1 if papers_positives[paper_id] < 2 else 0.5
        if random.random() < chance:
            content = random.choice(pos_texts)
            decision = "Approved"
            papers_positives[paper_id] += 1
        else:
            content = random.choice(neg_texts)
            decision = "Denied"
        generated.append([person_id, paper_id, content, decision])
    return generated

def write_reviews(output_path, reviews):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "paper_id", "text", "acceptance"])
        writer.writerows(reviews)

def main():
    reviews, papers_positives = load_reviews(INPUT_REVIEWS)
    extended_reviews = generate_reviews(reviews, papers_positives, POSITIVE_CONTENT, NEGATIVE_CONTENT)
    write_reviews(OUTPUT_REVIEWS, extended_reviews)

    print(f"✅ Archivo generado: {OUTPUT_REVIEWS} con {len(extended_reviews)} reviews")

if __name__ == "__main__":
    main()
