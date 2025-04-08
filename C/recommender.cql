// STEP 1

MATCH (p:Paper)
WHERE any(word IN ["data management", "indexing", "data modeling", "big data", "data processing", "data storage", "data querying"]
           WHERE toLower(p.title) CONTAINS word)
SET p:DatabaseCommunityPaper;


// STEP 2

// For Conference/Workshop
MATCH (v:ConferenceWorkshop)<-[:PUBLISHED_IN]-(p:Paper)
WITH v, collect(p) AS papers
UNWIND papers AS p
WITH v, count(DISTINCT p) AS total,
     count(DISTINCT CASE WHEN p:DatabaseCommunityPaper THEN p END) AS db_related
WHERE total > 0 AND db_related * 1.0 / total >= 0.9
SET v:DatabaseVenue;

// Repeat for Journals
MATCH (j:Journal)<-[:PERTAINS]-(v:Volume)<-[:PUBLISHED_IN]-(p:Paper)
WITH j, collect(p) AS papers
UNWIND papers AS p
WITH j, count(DISTINCT p) AS total,
     count(DISTINCT CASE WHEN p:DatabaseCommunityPaper THEN p END) AS db_related
WHERE total > 0 AND db_related * 1.0 / total >= 0.9
SET j:DatabaseVenue;

// STEP 3

// Get DB-related papers
MATCH (p:Paper)-[:PUBLISHED_IN]->(v)
OPTIONAL MATCH (v)<-[:PERTAINS]-(vol:Volume)-[:PERTAINS]->(j:Journal)
WITH p, v, vol, j
WHERE v:DatabaseVenue OR j:DatabaseVenue

// Count citations from other DB-related papers
WITH p
OPTIONAL MATCH (:Paper)-[:CITES]->(p)
WITH p, count(*) AS citations
ORDER BY citations DESC
LIMIT 100
SET p:TopDBPaper;

//STEP 4

// Find authors of TopDBPaper
MATCH (a:Person)-[:WROTE]->(p:TopDBPaper)
WITH a, count(p) AS top_paper_count
SET a:PotentialReviewer
WITH a, top_paper_count
WHERE top_paper_count >= 2
SET a:Guru;
