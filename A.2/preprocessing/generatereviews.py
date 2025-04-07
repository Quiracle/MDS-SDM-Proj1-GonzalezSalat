import csv
import random
from collections import defaultdict

def load_person_ids(input_path):
    person_ids = set()
    with open(input_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_ids.add(row["person_id"])
    return person_ids

def load_blocked_reviewers(wrote_path, corr_path):
    paper_to_blocked = defaultdict(set)
    for path in [wrote_path, corr_path]:
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                paper_to_blocked[row["paper_id"]].add(row["person_id"])
    return paper_to_blocked

def load_paper_ids(papers_path):
    paper_ids = []
    with open(papers_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_ids.append(row["paper_id"])
    return paper_ids

def generate_reviews(paper_ids, person_ids, blocked_reviewers, num_reviewers=2):
    reviews = []
    for paper in paper_ids:
        blocked = blocked_reviewers.get(paper, set())
        eligible = list(person_ids - blocked)
        to_sample = min(num_reviewers, len(eligible))
        selected = random.sample(eligible, to_sample)
        for reviewer in selected:
            reviews.append((reviewer, paper))
    return reviews

def write_reviews_csv(reviews, output_path):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "paper_id"])
        writer.writerows(reviews)
    print(f"✅ Relaciones REVIEWS generadas: {len(reviews)} totales.")
    print(f"📄 Archivo guardado como: {output_path}")

def main():
    INPUT_PERSON = "data/person_nodes.csv"
    INPUT_WROTE = "data/author_wrote.csv"
    INPUT_CORR = "data/corresponding_author.csv"
    INPUT_PAPERS = "data/paper_nodes.csv"
    OUTPUT_REVIEWS = "data/reviews.csv"
    NUM_REVIEWERS = 3

    person_ids = load_person_ids(INPUT_PERSON)
    blocked_reviewers = load_blocked_reviewers(INPUT_WROTE, INPUT_CORR)
    paper_ids = load_paper_ids(INPUT_PAPERS)
    reviews = generate_reviews(paper_ids, person_ids, blocked_reviewers, NUM_REVIEWERS)
    write_reviews_csv(reviews, OUTPUT_REVIEWS)

if __name__ == "__main__":
    main()
