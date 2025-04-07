import csv

def read_edition_event_rels(input_path):
    rels = []
    with open(input_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            edition = row["edition_id"]
            event = row["name"]
            rels.append([edition, event])
    return rels

def write_conferenceworkshop_rels(rels, output_path):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["edition_id", "name"])
        writer.writerows(rels)
    print("✅ Archivo 'edition_pertains_conferenceworkshop.csv' generado correctamente.")

def main():
    INPUT_EDITION_EVENT = "data/edition_pertains_event.csv"
    OUTPUT_REL = "data/edition_pertains_conferenceworkshop.csv"

    rels = read_edition_event_rels(INPUT_EDITION_EVENT)
    write_conferenceworkshop_rels(rels, OUTPUT_REL)

if __name__ == "__main__":
    main()
