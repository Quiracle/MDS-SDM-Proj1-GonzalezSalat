from neo4j import GraphDatabase

# Configuración de conexión
uri = "bolt://localhost:7687"
user = "neo4j"
password = "test1234"  # reemplaza esto con la que pusiste tras cambiar test1234

driver = GraphDatabase.driver(uri, auth=(user, password))

cypher_statements = [

    # --- NODOS ---
    """
    LOAD CSV WITH HEADERS FROM 'file:///organization_nodes.csv' AS row
    CREATE (:Organization {organization_id: row.organization_id, name: row.name, type: row.type});
    """,

    # --- RELACIONES ---
    """
    LOAD CSV WITH HEADERS FROM 'file:///person_affiliated_with.csv' AS row
    MATCH (p:Person {person_id: row.person_id}), (k:Organization {organization_id: row.organization_id})
    CREATE (p)-[:IS_AFFILIATED]->(k);
    """,

    # --- MODIFICATIONS ---
    """
    LOAD CSV WITH HEADERS FROM 'file:///reviews_extended.csv' AS row
    MATCH (a:Person {person_id: row.person_id})-[r:REVIEWS]->(p:Paper {paper_id: row.paper_id})
    SET r.text = row.text,
        r.acceptance = row.acceptance;
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
