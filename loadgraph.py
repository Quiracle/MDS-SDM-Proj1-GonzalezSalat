from neo4j import GraphDatabase

# Configuración de conexión
uri = "bolt://localhost:7687"
user = "neo4j"
password = "test1234"  # reemplaza esto con la que pusiste tras cambiar test1234

driver = GraphDatabase.driver(uri, auth=(user, password))

cypher_statements = [

    # --- NODOS ---
    """
    LOAD CSV WITH HEADERS FROM 'file:///paper_nodes.csv' AS row
    CREATE (:Paper {paper_id: row.paper_id, title: row.title, year: toInteger(row.year), abstract: row.abstract});
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///person_nodes.csv' AS row
    CREATE (:Person {person_id: row.person_id, name: row.name});
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///keyword_nodes.csv' AS row
    CREATE (:Keyword {word: row.word});
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///conferenceworkshop_nodes.csv' AS row
    CREATE (:ConferenceWorkshop {name: row.name});
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///edition_nodes.csv' AS row
    CREATE (:Edition {edition_id: row.edition_id, year: toInteger(row.year), city: row.city, proceeding: row.proceeding});
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///journal_nodes.csv' AS row
    CREATE (:Journal {journal_id: row.journal_id, name: row.name, organization: row.organization});
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///volume_nodes.csv' AS row
    CREATE (:Volume {volume_id: row.volume_id, number: row.number, year: toInteger(row.year)});
    """,

    # --- RELACIONES ---
    """
    LOAD CSV WITH HEADERS FROM 'file:///paper_keywords.csv' AS row
    MATCH (p:Paper {paper_id: row.paper_id}), (k:Keyword {word: row.word})
    CREATE (p)-[:HAS_KEYWORD]->(k);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///author_wrote.csv' AS row
    MATCH (a:Person {person_id: row.person_id}), (p:Paper {paper_id: row.paper_id})
    CREATE (a)-[:WROTE]->(p);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///corresponding_author.csv' AS row
    MATCH (a:Person {person_id: row.person_id}), (p:Paper {paper_id: row.paper_id})
    CREATE (a)-[:CORRESPONDING_AUTHOR]->(p);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///reviews.csv' AS row
    MATCH (a:Person {person_id: row.person_id}), (p:Paper {paper_id: row.paper_id})
    CREATE (a)-[:REVIEWS]->(p);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///paper_cites.csv' AS row
    MATCH (p1:Paper {paper_id: row.citing}), (p2:Paper {paper_id: row.cited})
    CREATE (p1)-[:CITES]->(p2);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///paper_published_in_edition.csv' AS row
    MATCH (p:Paper {paper_id: row.paper_id}), (e:Edition {edition_id: row.edition_id})
    CREATE (p)-[:PUBLISHED_IN]->(e);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///paper_published_in_volume.csv' AS row
    MATCH (p:Paper {paper_id: row.paper_id}), (v:Volume {volume_id: row.volume_id})
    CREATE (p)-[:PUBLISHED_IN]->(v);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///edition_pertains_conferenceworkshop.csv' AS row
    MATCH (e:Edition {edition_id: row.edition_id}), (c:ConferenceWorkshop {name: row.name})
    CREATE (e)-[:PERTAINS]->(c);
    """,

    """
    LOAD CSV WITH HEADERS FROM 'file:///volume_pertains_journal.csv' AS row
    MATCH (v:Volume {volume_id: row.volume_id}), (j:Journal {journal_id: row.journal_id})
    CREATE (v)-[:PERTAINS]->(j);
    """
]

def run_queries():
    with driver.session() as session:
        for query in cypher_statements:
            print("▶ Ejecutando query...")
            session.run(query)
        print("✅ Todo importado correctamente.")

if __name__ == "__main__":
    run_queries()
