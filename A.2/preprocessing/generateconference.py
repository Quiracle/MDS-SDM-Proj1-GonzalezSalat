import csv

def read_venues(input_path):
    conference_names = set()
    with open(input_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            venue = row["venue_name"]
            conference_names.add(venue)
    return conference_names

def write_conferenceworkshop_nodes(venue_names, output_path):
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        for name in sorted(venue_names):
            writer.writerow([name])
    print("✅ Archivo 'conferenceworkshop_nodes.csv' generado correctamente.")

def main():
    INPUT_VENUE = "data/venue_nodes.csv"
    OUTPUT_CW = "data/conferenceworkshop_nodes.csv"
    
    venues = read_venues(INPUT_VENUE)
    write_conferenceworkshop_nodes(venues, OUTPUT_CW)

if __name__ == "__main__":
    main()
