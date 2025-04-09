// Top 3 most cited papers per Conference/Workshop
MATCH (p:Paper)-[:PUBLISHED_IN]->(:Edition)-[:PERTAINS]->(c:ConferenceWorkshop)
OPTIONAL MATCH (:Paper)-[:CITES]->(p)
WITH c.name AS conference, p.title AS title, p.paper_id AS id, count(*) AS citation_count
ORDER BY conference, citation_count DESC
WITH conference, collect({title: title, id: id, citations: citation_count}) AS papers
RETURN conference, papers[0..3] AS top_3_papers;


//Community
MATCH (a:Person)-[:WROTE]->(p:Paper)-[:PUBLISHED_IN]->(e:Edition)-[:PERTAINS]->(c:ConferenceWorkshop)
WITH c.name AS conference, a.name AS author, count(DISTINCT e.edition_id) AS editions
WHERE editions >= 4
RETURN conference, author, editions
ORDER BY conference, editions DESC;

//Get journal impact factor
// Step 1: Get all papers and their journals
MATCH (j:Journal)<-[:PERTAINS]-(v:Volume)<-[:PUBLISHED_IN]-(p:Paper)
WITH j, p
// Step 2: Count how many times each paper is cited
OPTIONAL MATCH (p)<-[:CITES]-(:Paper)
WITH j.journal_id AS journal, count(*) AS citation_count, count(DISTINCT p) AS paper_count
RETURN journal,
       sum(citation_count) * 1.0 / paper_count AS impact_factor,    //Use 1.0 to get decimal result
       sum(citation_count) AS total_citations,
       paper_count AS total_papers
ORDER BY impact_factor DESC;


//Get h index
// Step 1: Get each author's papers and their citation counts
MATCH (a:Person)-[:WROTE]->(p:Paper)
OPTIONAL MATCH (:Paper)-[:CITES]->(p)
WITH a.name AS author, p, count(*) AS citation_count

// Step 2: Group citation counts into a list per author
WITH author, collect(citation_count) AS citations

// Step 3: Unwind and sort manually (descending)
UNWIND citations AS c
WITH author, c
ORDER BY author, c DESC

// Step 4: Rank citations per author
WITH author, collect(c) AS sorted_citations
UNWIND range(0, size(sorted_citations)-1) AS i
WITH author, i + 1 AS rank, sorted_citations[i] AS citation
WHERE citation >= rank
WITH author, max(rank) AS h_index
RETURN author, h_index, sorted_citations
ORDER BY h_index DESC;
