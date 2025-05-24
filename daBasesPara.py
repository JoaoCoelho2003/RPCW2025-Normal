from rdflib import Namespace, Literal, URIRef, XSD, OWL, Graph, RDF, RDFS

n = Namespace("http://www.semanticweb.org/jojocoelho/ontologies/2025/academia/")
g = Graph()
g.parse("./ontologies/sapientia_ind_estudaCom.ttl", format="ttl")

daBasesPara = URIRef(n.daBasesPara)
g.add((daBasesPara, RDF.type, OWL.ObjectProperty))
g.add((daBasesPara, RDFS.domain, n.Disciplina))
g.add((daBasesPara, RDFS.range, n.Aplicacao))

query = """
CONSTRUCT {
  ?disciplina :daBasesPara ?aplicacao .
}
WHERE {
  ?disciplina :eEstudadoEm ?conceito .
  ?conceito :temAplicacaoEm ?aplicacao .
}
"""

result = g.query(query)

for r in result:
    print(r)
    
print(len(result))

insert_query = """
INSERT {
  ?disciplina :daBasesPara ?aplicacao .
}
WHERE {
  ?disciplina :eEstudadoEm ?conceito .
  ?conceito :temAplicacaoEm ?aplicacao .
}
"""

g.update(insert_query)

g.serialize(destination="./ontologies/sapientia_ind_daBasesPara.ttl", format="ttl")

