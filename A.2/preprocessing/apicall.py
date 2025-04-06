import requests
import os
import csv
from pathlib import Path

# Configuración
API_KEY = "EowDUTmICj4b5QQgxTZgw8eZxoZxZ11Z8XPfBYXd"
HEADERS = {"x-api-key": API_KEY}
SEARCH_QUERY = "graph databases"
MAX_PAPERS = 100
FIELDS = "title,year,abstract,venue,authors,externalIds,fieldsOfStudy,citations,references"

# Crear carpeta de datos
Path("data").mkdir(exist_ok=True)

# Inicializar estructuras
papers = {}
people = {}
keywords = set()
venues = {}
wrote_rels = []
cites_rels = []
pubin_rels = []
haskeyword_rels = []

# Función para clasificar el venue
def classify_venue(name):
    if not name:
        return None, None
    lowered = name.lower()
    if any(x in lowered for x in ["conference", "symposium", "workshop", "proceedings"]):
        return name, "Conference"
    return name, "Journal"

# Buscar papers
print("🔎 Buscando papers en Semantic Scholar...")
search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": SEARCH_QUERY,
    "fields": FIELDS,
    "limit": MAX_PAPERS
}
response = requests.get(search_url, headers=HEADERS, params=params)

if response.status_code != 200:
    print(f"❌ Error en la llamada a la API: {response.status_code} - {response.text}")
    exit()

results = response.json().get("data", [])

for paper in results:
    pid = paper.get("paperId")
    if not pid:
        continue

    # Datos del paper
    papers[pid] = {
        "id": pid,
        "title": (paper.get("title") or "").replace("\n", " "),
        "year": paper.get("year"),
        "abstract": (paper.get("abstract") or "").replace("\n", " "),
        "venue": paper.get("venue"),
        "doi": paper.get("externalIds", {}).get("DOI")
    }

    # Venue
    venue_name, venue_type = classify_venue(paper.get("venue"))
    if venue_name:
        venues[venue_name] = venue_type
        pubin_rels.append((pid, venue_name))

    # Autores
    for i, author in enumerate(paper.get("authors", [])):
        aid = author.get("authorId")
        name = author.get("name")
        if aid and name:
            people[aid] = name
            wrote_rels.append((aid, pid))
            # Puedes marcar como corresponding author si i == 0 (opcional)

    # Keywords (solo si no es None)
    for kw in paper.get("fieldsOfStudy") or []:
        keywords.add(kw)
        haskeyword_rels.append((pid, kw))

    # Citaciones (CITES)
    for cited in paper.get("references") or []:
        target = cited.get("paperId")
        if target:
            cites_rels.append((pid, target))

# --------------------- ESCRITURA DE CSVs ---------------------

# Paper
with open("data/paper_nodes.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["paper_id:ID(Paper)", "title", "year:INT", "abstract", "doi"])
    for p in papers.values():
        writer.writerow([p["id"], p["title"], p["year"], p["abstract"], p["doi"] or ""])

# Person
with open("data/person_nodes.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["person_id:ID(Person)", "name"])
    for pid, name in people.items():
        writer.writerow([pid, name])

# WROTE
with open("data/author_wrote.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Person)", ":END_ID(Paper)"])
    writer.writerows(wrote_rels)

# CITES
with open("data/paper_cites.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Paper)", ":END_ID(Paper)"])
    writer.writerows(cites_rels)

# Venue
with open("data/venue_nodes.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["venue_name:ID(Venue)", "type"])
    for v, t in venues.items():
        writer.writerow([v, t])

# PUBLISHED_IN
with open("data/paper_published_in.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Paper)", ":END_ID(Venue)"])
    writer.writerows(pubin_rels)

# Keywords
with open("data/keyword_nodes.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["keyword_name:ID(Keyword)"])
    for kw in keywords:
        writer.writerow([kw])

# HAS_KEYWORD
with open("data/paper_keywords.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([":START_ID(Paper)", ":END_ID(Keyword)"])
    writer.writerows(haskeyword_rels)

print("✅ ¡CSV exportado correctamente en carpeta 'data/'!")

# Guardar person_nodes_raw.csv con solo ID y name
with open("data/person_nodes_raw.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["person_id:ID(Person)", "name"])
    for pid, name in people.items():
        writer.writerow([pid, name])

print("✅ Archivo person_nodes_raw.csv generado")
