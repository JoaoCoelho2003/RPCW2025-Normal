from rdflib import Namespace, Literal, URIRef, XSD, OWL, Graph, RDF, RDFS

n = Namespace("http://www.semanticweb.org/jojocoelho/ontologies/2025/academia/")
g = Graph()
g.parse("./ontologies/sapientia_ind.ttl", format="ttl")

estudaCom = URIRef(n.estudaCom)
g.add((estudaCom, RDF.type, OWL.ObjectProperty))
g.add((estudaCom, RDFS.domain, n.Aprendiz))
g.add((estudaCom, RDFS.range, n.Mestre))

query = """
CONSTRUCT {
  ?aprendiz :estudaCom ?mestre .
}
WHERE {
  ?aprendiz :aprende ?disciplina .
  ?mestre :ensina ?disciplina .
}
"""

result = g.query(query)

for r in result:
    print(r)
    
print(len(result))

insert_query = """
INSERT {
  ?aprendiz :estudaCom ?mestre .
}
WHERE {
  ?aprendiz :aprende ?disciplina .
  ?mestre :ensina ?disciplina .
}
"""

g.update(insert_query)

g.serialize(destination="./ontologies/sapientia_ind_estudaCom.ttl", format="ttl")