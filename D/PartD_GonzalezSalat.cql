// PageRank
// We are using GDS1.x, which means that to call PageRank, we first need to create an in-memory projection.

CALL gds.graph.project(
  'paperGraph',
  'Paper',
  {
    CITES: {
      type: 'CITES',
      orientation: 'NATURAL'
    }
  }
);


CALL gds.pageRank.stream('paperGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).title AS paper_title, score
ORDER BY score DESC
LIMIT 10;

// Remove projection
CALL gds.graph.drop('paperGraph');

// Louvain

// We are going to look for communities looking at a citation network since we were interested in communities in previous parts of this project. 
// We will be storing the community data into each node, this way i could be used to do similar tasks to part C of the project. Even tagging the events
// according to the communities of the papers published in them could be done thanks to Louvaing algorithm.

//First we project the graph. It will be undirected since we don't care about which paper cites which, only that they are related
CALL gds.graph.project(
  'paperGraphLouvain',
  'Paper',
  {
    CITES: {
      type: 'CITES',
      orientation: 'UNDIRECTED'
    }
  }
);

// To remove the relation in case of wanting to modify it we can use:
CALL gds.graph.drop('paperGraphLouvain', false);

// Execute Louvain algorithm
CALL gds.louvain.stream('paperGraphLouvain')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).title AS paper_title, communityId
ORDER BY communityId, paper_title
LIMIT 50;

// Write the community to each Paper node
CALL gds.louvain.write('paperGraphLouvain', {
  writeProperty: 'louvainCommunity'
})
YIELD communityCount, modularity;

// Query example to see the communities:
MATCH (p:Paper)
WHERE exists(p.louvainCommunity)
RETURN p.louvainCommunity AS community_id,
       collect(p.title) AS papers_in_community,
       count(*) AS total_papers
ORDER BY total_papers DESC
LIMIT 10;


