import csv
import random

def load_paper_years(input_papers_path):
    paper_year = {}
    with open(input_papers_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_year[row["paper_id"]] = row["year"]
    return paper_year

def load_paper_venues(input_published_in_path):
    paper_venue = {}
    with open(input_published_in_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper = row["paper_id"]
            venue = row["name"]
            paper_venue[paper] = venue
    return paper_venue

def generate_editions(paper_year, paper_venue, cities=None):
    if cities is None:
        cities = ["Barcelona", "London", "Tokyo", "New York", "Paris", "Berlin", "Amsterdam", "Lisbon"]

    edition_map = {}
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

    return edition_rows, paper_ed_rels, edition_event_rels

def write_csv(path, header, rows):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def main():
    INPUT_PAPERS = "data/paper_nodes.csv"
    INPUT_PUBLISHED_IN = "data/paper_published_in.csv"
    OUTPUT_EDITION = "data/edition_nodes.csv"
    OUTPUT_PUBLISHED_IN_ED = "data/paper_published_in_edition.csv"
    OUTPUT_PERTAINS = "data/edition_pertains_event.csv"

    paper_year = load_paper_years(INPUT_PAPERS)
    paper_venue = load_paper_venues(INPUT_PUBLISHED_IN)
    edition_rows, paper_ed_rels, edition_event_rels = generate_editions(paper_year, paper_venue)

    write_csv(OUTPUT_EDITION, ["edition_id", "year", "city", "proceeding"], edition_rows)
    write_csv(OUTPUT_PUBLISHED_IN_ED, ["paper_id", "edition_id"], paper_ed_rels)
    write_csv(OUTPUT_PERTAINS, ["edition_id", "name"], edition_event_rels)

    print("✅ Nodos Edition y relaciones generadas correctamente")

if __name__ == "__main__":
    main()
