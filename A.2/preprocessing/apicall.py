import requests
import os
import csv
from pathlib import Path

API_KEY = "EowDUTmICj4b5QQgxTZgw8eZxoZxZ11Z8XPfBYXd"
HEADERS = {"x-api-key": API_KEY}
SEARCH_QUERY = ["graph databases", "big data"]
MAX_PAPERS = 100
FIELDS = "title,year,abstract,venue,authors,externalIds,fieldsOfStudy,citations,references"

def classify_venue(name):
    if not name:
        return None, None
    lowered = name.lower()
    if any(x in lowered for x in ["conference", "symposium", "workshop", "proceedings"]):
        return name, "Conference"
    return name, "Journal"

def fetch_papers(query):
    print("🔎 Buscando papers en Semantic Scholar...")
    search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "fields": FIELDS,
        "limit": MAX_PAPERS
    }
    response = requests.get(search_url, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"❌ Error en la llamada a la API: {response.status_code} - {response.text}")
    
    return response.json().get("data", [])

def process_papers(results):
    papers = {}
    people = {}
    corresponding = []
    keywords = set()
    venues = {}
    wrote_rels = []
    cites_rels = []
    pubin_rels = []
    haskeyword_rels = []

    for paper in results:
        pid = paper.get("paperId")
        if not pid:
            continue

        papers[pid] = {
            "id": pid,
            "title": (paper.get("title") or "").replace("\n", " "),
            "year": paper.get("year"),
            "abstract": (paper.get("abstract") or "").replace("\n", " "),
            "venue": paper.get("venue"),
            "doi": paper.get("externalIds", {}).get("DOI")
        }

        venue_name, venue_type = classify_venue(paper.get("venue"))
        if venue_name:
            venues[venue_name] = venue_type
            pubin_rels.append((pid, venue_name))

        for i, author in enumerate(paper.get("authors", [])):
            aid = author.get("authorId")
            name = author.get("name")
            if aid and name:
                people[aid] = name
                wrote_rels.append((aid, pid))
                if i == 0:
                    corresponding.append((aid, pid))

        for kw in paper.get("fieldsOfStudy") or []:
            keywords.add(kw)
            haskeyword_rels.append((pid, kw))

        for cited in paper.get("references") or []:
            target = cited.get("paperId")
            if target:
                cites_rels.append((pid, target))

    return papers, people, keywords, venues, wrote_rels, cites_rels, pubin_rels, haskeyword_rels, corresponding

def write_csvs(papers, people, keywords, venues, wrote_rels, cites_rels, pubin_rels, haskeyword_rels, corresponding):
    Path("data").mkdir(exist_ok=True)

    with open("data/paper_nodes.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "year", "abstract", "doi"])
        for p in papers.values():
            writer.writerow([p["id"], p["title"], p["year"], p["abstract"], p["doi"] or ""])

    with open("data/person_nodes.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "name"])
        for pid, name in people.items():
            writer.writerow([pid, name])

    with open("data/author_wrote.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "paper_id"])
        writer.writerows(wrote_rels)

    with open("data/corresponding_author.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "paper_id"])
        writer.writerows(corresponding)

    with open("data/paper_cites.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["citing", "cited"])
        writer.writerows(cites_rels)

    with open("data/venue_nodes.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["venue_name", "type"])
        for v, t in venues.items():
            writer.writerow([v, t])

    with open("data/paper_published_in.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "name"])
        writer.writerows(pubin_rels)

    with open("data/keyword_nodes.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word"])
        for kw in keywords:
            writer.writerow([kw])

    with open("data/paper_keywords.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "word"])
        writer.writerows(haskeyword_rels)

    with open("data/person_nodes_raw.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "name"])
        for pid, name in people.items():
            writer.writerow([pid, name])

    print("¡CSV created successfully in 'data/'!")
    print("CSV person_nodes_raw.csv generated")

def main():
    results = []
    for query in SEARCH_QUERY:
        results.extend(fetch_papers(query))
    data = process_papers(results)
    write_csvs(*data)

if __name__ == "__main__":
    main()
