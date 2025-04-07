// Top 3 most cited papers per Conference/Workshop
MATCH (p:Paper)-[:PUBLISHED_IN]->(c:ConferenceWorkshop)
OPTIONAL MATCH (:Paper)-[:CITES]->(p)
WITH c.name AS conference, p.title AS title, p.paper_id AS id, count(*) AS citation_count
ORDER BY conference, citation_count DESC
WITH conference, collect({title: title, id: id, citations: citation_count}) AS papers
RETURN conference, papers[0..3] AS top_3_papers;
//Problems: There are less than 3 Conferences with more than 1 paper, so most results is just a paper with low citations since it's the only one.


//Community
MATCH (a:Person)-[:WROTE]->(p:Paper)-[:PUBLISHED_IN]->(e:Edition)-[:PERTAINS]->(c:ConferenceWorkshop)
WITH c.name AS conference, a.name AS author, count(DISTINCT e.edition_id) AS editions
WHERE editions >= 4
RETURN conference, author, editions
ORDER BY conference, editions DESC;
//Problems: There are no Conferences with more than 2 editions. If the editions are set to >= 2 there is a result.

//Get journal impact factor
MATCH (j:Journal)<-[:PERTAINS]-(v:Volume)<-[:PUBLISHED_IN]-(p:Paper)
OPTIONAL MATCH (:Paper)-[:CITES]->(p)
WITH j.name AS journal, count(DISTINCT p) AS total_papers, count(DISTINCT CASE WHEN EXISTS((:Paper)-[:CITES]->(p)) THEN p END) AS total_cited
RETURN journal,
       total_cited * 1.0 / total_papers AS impact_factor,
       total_cited, total_papers
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
RETURN author, h_index
ORDER BY h_index DESC;