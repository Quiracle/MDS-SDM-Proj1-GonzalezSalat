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

def write_organization_nodes(output_path, organizations):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["organization_id", "name", "type"])
        writer.writerows(organizations)

def load_person_ids(input_path):
    with open(input_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row["person_id"] for row in reader]

def assign_affiliations(person_ids, orgs):
    affiliations = []
    for pid in person_ids:
        org_id = random.choice(orgs)[0]
        affiliations.append([pid, org_id])
    return affiliations

def write_affiliations(output_path, affiliations):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "organization_id"])
        writer.writerows(affiliations)

def main():
    write_organization_nodes(OUTPUT_ORGS, orgs)
    person_ids = load_person_ids(INPUT_PERSONS)
    affiliations = assign_affiliations(person_ids, orgs)
    write_affiliations(OUTPUT_AFFILIATIONS, affiliations)

    print("File generated with institutions:")
    print(f" - {OUTPUT_ORGS}")
    print(f" - {OUTPUT_AFFILIATIONS}")

if __name__ == "__main__":
    main()
