import csv

def load_person_names(input_raw_path):
    id_to_name = {}
    with open(input_raw_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["person_id"]
            name = row["name"]
            id_to_name[pid] = name
    return id_to_name

def extract_unique_person_ids(relation_paths):
    person_ids = set()
    for path in relation_paths:
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                person_ids.add(row["person_id"].rstrip('_corr'))
    return person_ids

def create_person_rows(person_ids, id_to_name):
    rows = []
    for pid in sorted(person_ids):
        name = id_to_name.get(pid, "Unknown")
        rows.append([pid, name])
    return rows

def write_person_csv(rows, output_path):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "name"])
        writer.writerows(rows)
    print(f"✅ Archivo generado: {output_path}")

def main():
    INPUT_RAW = "data/person_nodes_raw.csv"
    INPUT_WRITES = "data/author_wrote.csv"
    INPUT_CORR = "data/corresponding_author.csv"
    OUTPUT_PERSON = "data/person_nodes.csv"

    id_to_name = load_person_names(INPUT_RAW)
    person_ids = extract_unique_person_ids([INPUT_WRITES, INPUT_CORR])
    person_rows = create_person_rows(person_ids, id_to_name)
    write_person_csv(person_rows, OUTPUT_PERSON)

if __name__ == "__main__":
    main()
