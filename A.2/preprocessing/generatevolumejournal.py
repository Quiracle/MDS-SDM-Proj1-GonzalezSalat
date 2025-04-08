import csv
import random

def load_venue_types(venue_nodes_path):
    venue_type = {}
    with open(venue_nodes_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            venue_type[row["venue_name"]] = row["type"]
    return venue_type

def load_paper_years(paper_nodes_path):
    paper_year = {}
    with open(paper_nodes_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_year[row["paper_id"]] = row["year"]
    return paper_year

def load_paper_venues(published_in_path):
    paper_venue = {}
    with open(published_in_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_venue[row["paper_id"]] = row["name"]
    return paper_venue

def generate_volume_journal_data(paper_to_year, paper_to_venue, venue_type, orgs=None):
    if orgs is None:
        orgs = ["ACM Press", "IEEE Publishing", "Elsevier", "Springer", "Oxford Press"]

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

    return volume_map, journal_map, paper_vol_rels, vol_jour_rels

def write_volume_nodes(volume_map, path):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["volume_id", "number", "year"])
        for vid, year in volume_map.items():
            writer.writerow([vid, vid.split("_Vol")[-1], year])

def write_journal_nodes(journal_map, path):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["journal_id", "organization"])
        for jid, org in journal_map.items():
            writer.writerow([jid, org])

def write_relationship_csv(rows, path, header):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def main():
    PAPER_NODES = "data/paper_nodes.csv"
    VENUE_NODES = "data/venue_nodes.csv"
    PAPER_PUBLISHED_IN = "data/paper_published_in.csv"
    VOLUME_NODES = "data/volume_nodes.csv"
    JOURNAL_NODES = "data/journal_nodes.csv"
    PAPER_PUBLISHED_IN_VOLUME = "data/paper_published_in_volume.csv"
    VOLUME_PERTAINS_JOURNAL = "data/volume_pertains_journal.csv"

    venue_type = load_venue_types(VENUE_NODES)
    paper_to_year = load_paper_years(PAPER_NODES)
    paper_to_venue = load_paper_venues(PAPER_PUBLISHED_IN)

    volume_map, journal_map, paper_vol_rels, vol_jour_rels = generate_volume_journal_data(
        paper_to_year, paper_to_venue, venue_type
    )

    write_volume_nodes(volume_map, VOLUME_NODES)
    write_journal_nodes(journal_map, JOURNAL_NODES)
    write_relationship_csv(paper_vol_rels, PAPER_PUBLISHED_IN_VOLUME, ["paper_id", "volume_id"])
    write_relationship_csv(vol_jour_rels, VOLUME_PERTAINS_JOURNAL, ["volume_id", "journal_id"])

    print(" Volumes and Journals created sucessfully.")

if __name__ == "__main__":
    main()
