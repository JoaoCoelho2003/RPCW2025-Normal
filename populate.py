import json
from rdflib import Graph, Namespace, Literal, URIRef, RDF, XSD, OWL

n = Namespace("http://www.semanticweb.org/jojocoelho/ontologies/2025/academia/")
g = Graph()
g.parse("./ontologies/sapientia_base.ttl", format="ttl")
g.bind("", n)

def create_individual(uri, rdf_type, properties):
    individual = URIRef(uri)
    g.add((individual, RDF.type, OWL.NamedIndividual))
    g.add((individual, RDF.type, rdf_type))
    for prop, value in properties.items():
        if value is not None:
            if prop == n.idade:
                g.add((individual, prop, Literal(value, datatype=XSD.integer)))
            else:
                g.add((individual, prop, Literal(value, datatype=XSD.string)))
    return individual

datasets = {
    "conceitos": json.load(open("./datasets/conceitos.json"))["conceitos"],
    "disciplinas": json.load(open("./datasets/disciplinas.json"))["disciplinas"],
    "mestres": json.load(open("./datasets/mestres.json"))["mestres"],
    "obras": json.load(open("./datasets/obras.json"))["obras"],
    "aprendizes": json.load(open("./datasets/pg55954.json")),
}

for conceito in datasets["conceitos"]:
    conceito_uri = n[conceito["nome"].replace(" ", "_")]
    conceito_ind = create_individual(
        conceito_uri,
        n.Conceito,
        {
            n.nome: conceito.get("nome"),
        },
    )
    if "períodoHistórico" in conceito:
        periodo_uri = n[conceito["períodoHistórico"].replace(" ", "_")]
        create_individual(periodo_uri, n.PeriodoHistorico, {n.nome: conceito["períodoHistórico"]})
        g.add((conceito_ind, n.surgeEm, periodo_uri))
    for aplicacao in conceito.get("aplicações", []):
        aplicacao_uri = n[aplicacao.replace(" ", "_")]
        create_individual(aplicacao_uri, n.Aplicacao, {n.nome: aplicacao})
        g.add((conceito_ind, n.temAplicacaoEm, aplicacao_uri))
        
    for conceito_relacionado in conceito.get("conceitosRelacionados", []):
        conceito_relacionado_uri = n[conceito_relacionado.replace(" ", "_")]
        if not (conceito_relacionado_uri, RDF.type, n.Conceito) in g:
            create_individual(conceito_relacionado_uri, n.Conceito, {n.nome: conceito_relacionado})
        g.add((conceito_uri, n.estaRelacionadoCom, conceito_relacionado_uri))

for disciplina in datasets["disciplinas"]:
    disciplina_uri = n[disciplina["nome"].replace(" ", "_")]
    disciplina_ind = create_individual(
        disciplina_uri,
        n.Disciplina,
        {n.nome: disciplina.get("nome")},
    )
    for tipo in disciplina.get("tiposDeConhecimento", []):
        tipo_uri = n[tipo.replace(" ", "_")]
        create_individual(tipo_uri, n.TipoDeConhecimento, {n.nome: tipo})
        g.add((disciplina_ind, n.pertenceA, tipo_uri))
    for conceito_nome in disciplina.get("conceitos", []):
        conceito_uri = n[conceito_nome.replace(" ", "_")]
        if not (conceito_uri, RDF.type, n.Conceito) in g:
            create_individual(conceito_uri, n.Conceito, {n.nome: conceito_nome})
        g.add((conceito_uri, n.eEstudadoEm, disciplina_uri))

for mestre in datasets["mestres"]:
    mestre_uri = n[mestre["nome"].replace(" ", "_")]
    mestre_ind = create_individual(
        mestre_uri,
        n.Mestre,
        {
            n.nome: mestre.get("nome"),
        },
    )
    if "períodoHistórico" in mestre:
        periodo_uri = n[mestre["períodoHistórico"].replace(" ", "_")]
        if not (periodo_uri, RDF.type, n.PeriodoHistorico) in g:
            create_individual(periodo_uri, n.PeriodoHistorico, {n.nome: mestre["períodoHistórico"]})
        g.add((mestre_ind, n.ativoDurante, periodo_uri))
    for disciplina_nome in mestre.get("disciplinas", []):
        disciplina_uri = n[disciplina_nome.replace(" ", "_")]
        if not (disciplina_uri, RDF.type, n.Disciplina) in g:
            create_individual(disciplina_uri, n.Disciplina, {n.nome: disciplina_nome})
        g.add((mestre_ind, n.ensina, disciplina_uri))

for obra in datasets["obras"]:
    obra_uri = n[obra["titulo"].replace(" ", "_")]
    obra_ind = create_individual(
        obra_uri,
        n.Obra,
        {n.titulo: obra.get("titulo")},
    )
    autor_uri = n[obra["autor"].replace(" ", "_")]
    if not (autor_uri, RDF.type, n.Mestre) in g:
        create_individual(autor_uri, n.Mestre, {})
    g.add((obra_ind, n.foiEscritoPor, autor_uri))
    for conceito_nome in obra.get("conceitos", []):
        conceito_uri = n[conceito_nome.replace(" ", "_")]
        if not (conceito_uri, RDF.type, n.Conceito) in g:
            create_individual(conceito_uri, n.Conceito, {n.nome: conceito_nome})
        g.add((obra_ind, n.explica, conceito_uri))

for i, aprendiz in enumerate(datasets["aprendizes"]):
    aprendiz_uri = n[f"{aprendiz['nome'].replace(' ', '_')}_{i}"]
    aprendiz_ind = create_individual(
        aprendiz_uri,
        n.Aprendiz,
        {
            n.nome: aprendiz.get("nome"),
            n.idade: aprendiz.get("idade"),
        },
    )
    for disciplina_nome in aprendiz.get("disciplinas", []):
        disciplina_uri = n[disciplina_nome.replace(" ", "_")]
        if not (disciplina_uri, RDF.type, n.Disciplina) in g:
            create_individual(disciplina_uri, n.Disciplina, {n.nome: disciplina_nome})
        g.add((aprendiz_ind, n.aprende, disciplina_uri))

g.serialize(destination="./ontologies/sapientia_ind.ttl", format="ttl")