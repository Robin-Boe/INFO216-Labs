from rdflib import OWL, RDF, RDFS, BNode, Namespace, Literal, Graph, XSD 
from rdflib.collection import Collection
import owlrl

g = Graph()

ex = Namespace('http://ex.org#')
g.bind('ex', ex)

# /////////////// Task 2A //////////////////

# Author-s, Country-s and Organization-s are Agent-s
g.add((ex.Country, RDFS.subClassOf, ex.Agent))
g.add((ex.Author, RDFS.subClassOf, ex.Agent))
g.add((ex.Organization, RDFS.subClassOf, ex.Agent))

# which have name-s that are string-s.
g.add((ex.name, RDFS.domain, ex.Agent))
g.add((ex.name, RDFS.range, XSD.string)) 

# An Author can have affiliation (organization he/she works for) and country.
b0 = BNode()
g.add((b0, RDF.type, OWL.Restriction))
g.add((b0, OWL.onProperty, ex.affiliation))
g.add((b0, OWL.someValuesFrom, ex.Organization))

b1 = BNode()
g.add((b1, RDF.type, OWL.Restriction))
g.add((b1, OWL.onProperty, ex.country))
g.add((b1, OWL.someValuesFrom, ex.Country))

g.add((ex.Author, RDFS.subClassOf, b0))
g.add((ex.Author, RDFS.subClassOf, b1))

#Paper-s are a type of Publication
g.add((ex.Paper, RDFS.subClassOf, ex.Publication))

b3 = BNode()
g.add((b3, RDF.type, OWL.Restriction))
g.add((b3, OWL.onProperty, ex.publication))
g.add((b3, OWL.someValuesFrom, ex.Publication))

g.add((ex.Paper, RDFS.subClassOf, b3))

# Publication-s have string title-s
g.add((ex.title, RDFS.domain, ex.Publication))
g.add((ex.title, RDFS.range, XSD.string))

# They also have author-s
b4 = BNode()
g.add((b4, RDF.type, OWL.Restriction))
g.add((b4, OWL.onProperty, ex.author))
g.add((b4, OWL.someValuesFrom, ex.Author))

g.add((ex.Publication, RDFS.subClassOf, b4))

# they are published in a year that is described by an integer
g.add((ex.year, RDFS.domain, ex.Publication))
g.add((ex.year, RDFS.range, XSD.integer))

# A Publication can have a publisher, which is an Organization
b5 = BNode()
g.add((b5, RDF.type, OWL.Restriction))
g.add((b5, OWL.onProperty, ex.publisher))
g.add((b5, OWL.someValuesFrom, ex.Organization))

g.add((ex.Publication, RDFS.subClassOf, b5))

# /////////////// Task 2B //////////////////

NS = {
    'ex':ex,
    'rdf':RDF,
    'rdfs':RDFS,
    'owl':OWL,
    'xsd':XSD,
}

g.update("""
INSERT DATA{
    ex:The_semantic_web ex:title "The_semantic_web"^^xsd:string;
                        ex:author ex:Tim_Berners-Lee,
                                  ex:James_Hendler;
                        ex:publication ex:Scientific_American;
                        ex:publisher ex:Springer_Nature;
                        ex:year "2001"^^xsd:integer.
    
    ex:DBpedia_A_nucleus ex:title "DBpedia_A_nucleus"^^xsd:string;
                        ex:author ex:Soren_Auer,
                                  ex:Christian_Bizer;
                        ex:publication ex:The_semantic_web_book;
                        ex:publisher ex:Springer_Nature;
                        ex:year "2007"^^xsd:integer.
    
    ex:Linked_data_The_story_so_far ex:title "Linked_data_The_story_so_far"^^xsd:string;
                        ex:author ex:Tim_Berners-Lee,
                                  ex:Christian_Bizer;
                        ex:publication ex:Semantic_services_interoperability_and_web_applications;
                        ex:publisher ex:IGI_Global;
                        ex:year "2011"^^xsd:integer.
        
    ex:Tim_Berners-Lee ex:affiliation ex:Massachusetts_Institute_of_Technology;
                                                  ex:country ex:United_States;
                                                  ex:name "Tim Bernes-Lee"^^xsd:string.
    
    ex:Soren_Auer ex:affiliation ex:Leibniz_University_Hannover;
                                          ex:country ex:Germany;
                                          ex:name "Soren Auer"^^xsd:string.
    
    ex:Christian_Bizer ex:affiliation ex:University_of_Mannheim;
                                        ex:country ex:Germany;
                                        ex:name "Christian Bizer"^^xsd:string.
    
    ex:James_Hendler ex:affiliation ex:Rensselaer_Polytechnic_Institute;
                                        ex:country ex:United_States;
                                        ex:name "James Hendler"^^xsd:string.
}""", initNs=NS)

owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

# g.serialize("task2.ttl", format="turtle")
print(g.serialize())