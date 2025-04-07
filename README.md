# MDS-SDM-Proj1-GonzalezSalat

## HOW TO USE THE DATABASE:

### Start the docker container:

Execute:

```
docker run --publish=7474:7474 --publish=7687:7687 --volume=./neo4j_project/data:/data --volume=./neo4j_project/import:/import --env=NEO4J_AUTH=none -d neo4j
```

and enter [the graphic interface](http://localhost:7474/browser/)

### Fill the database:

```
pip install -r requirements.txt
python ./loadgraph.py
```