from rdflib import Graph, RDFS, Namespace, RDF, FOAF, Literal, XSD
import owlrl

g = Graph()
ex = Namespace('http://example.org/')

g.bind("ex", ex)
g.bind("foaf", FOAF)

NS = {
    'ex': ex,
    'rdf': RDF,
    'rdfs': RDFS,
    'foaf': FOAF,
}

#populate the graph
g.add((ex.Cade, RDF.type, ex.Student))
g.add((ex.Cade, ex.studentAt, ex.UIB))

g.add((ex.Emma, ex.flyTo, ex.Bergen)) 

#rules
g.add((ex.Student, RDFS.subClassOf, FOAF.Person))
g.add((ex.studentAt, RDFS.subPropertyOf, ex.attends))

g.add((ex.flyTo, RDFS.domain, FOAF.Person)) 
g.add((ex.flyTo, RDFS.range, ex.City))

print(g.serialize())

# engine = owlrl.RDFSClosure.RDFS_Semantics(g, False, False, False)
# engine.closure()
# engine.flush_stored_triples()

output = g.query("""
    SELECT ?type WHERE{
        ex:Cade rdf:type ?type  
    }
""", initNs = NS)

print(list(output))

owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

print(g.serialize())

output = g.query("""
    SELECT ?type WHERE{
        ex:Cade rdf:type ?type  
    }
""", initNs = NS)

print(list(output))