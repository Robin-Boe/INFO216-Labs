''' NOTE: Look at the imports, and understand what is imported'''
from rdflib import Graph, RDFS, Namespace, RDF, FOAF, Literal, XSD, OWL, BNode
from rdflib.collection import Collection
import owlrl

g = Graph()
ex = Namespace('http://example.org/')
schema = Namespace('https://schema.org/')
dbpedia = Namespace("https://dbpedia.org/page/")

g.bind("ex", ex)
g.bind("foaf", FOAF)
g.bind("schema", schema)
''' NOTE: Look at the serialized output and spot the differences with and without bind on dbpedia'''
# g.bind("dbr", dbpedia) 

# --- Information about the graph ---
g.add((ex.Emma, RDF.type, ex.Student))
g.add((ex.Emma, FOAF.knows, ex.Cade))

g.add((ex.Emma, ex.neighborTo, ex.Cade))

g.add((ex.Emma, ex.hasFather, ex.Tom))
g.add((ex.Emma, ex.livesWith, ex.Tom))

g.add((ex.Emma, ex.groupPartner, ex.Cade))
g.add((ex.Cade, ex.groupPartner, ex.Jerry))

g.add((ex.Emma, ex.birthdate, Literal("1996-10-22", datatype=XSD.date)))
g.add((ex.Emma, ex.socialSecurityNumber, Literal("123456789", datatype=XSD.integer)))

# b1 = BNode()
# b2 = BNode()
# Collection(g, b2, [ex.Emma, ex.Cade])
# g.add((b1, RDF.type, OWL.AllDifferent))
# g.add((b1, OWL.distinctMembers, b2))

# --- Rules ---
# Inverses, Differences and Equivalences
g.add((ex.hasFather, OWL.inverseOf, ex.fatherOf))
g.add((ex.Emma, OWL.differentFrom, ex.Cade))
g.add((FOAF.knows, OWL.equivalentProperty, schema.knows))
g.add((ex.Student, OWL.equivalentClass, dbpedia.Student))

# Properties
g.add((ex.neighborTo, RDF.type, OWL.SymmetricProperty))

g.add((ex.hasFather, RDF.type, OWL.AsymmetricProperty))
g.add((ex.hasFather, RDF.type, OWL.IrreflexiveProperty))

g.add((ex.livesWith, RDF.type, OWL.ReflexiveProperty))
''' NOTE: Try to run the serializer first with only Reflexive, then Reflexive and Symmetric, 
          than all 3, can you spot the differences? '''
# g.add((ex.livesWith, RDF.type, OWL.SymmetricProperty))
# g.add((ex.livesWith, RDF.type, OWL.TransitiveProperty))

g.add((ex.groupPartner, RDF.type, OWL.TransitiveProperty))
''' NOTE: Notice how Jerry has no group partners, and Cade only has Jerry as his group partner, whilst Emma has both. 
          what happens if we make groupPartner a symmetric property? '''
# g.add((ex.groupPartner, RDF.type, OWL.SymmetricProperty)) 

g.add((ex.birthdate, RDF.type, OWL.FunctionalProperty))
g.add((ex.socialSecurityNumber, RDF.type, OWL.InverseFunctionalProperty))

# Closure
# owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics).expand(g)

# Exports a serialzed XML file of the graph
# g.serialize("lab8_example.xml", format="xml") 

print(g.serialize())