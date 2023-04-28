from rdflib import Graph, Namespace, RDF, FOAF
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, GET, POST

#RDFLIB
g = Graph()
g.parse("Russia_investigation_kg.ttl")

ex = Namespace('http://example.org#')

NS = {
    '': ex,
    'rdf': RDF,
    'foaf': FOAF,
}

task1 = g.query("""
SELECT DISTINCT ?president WHERE{
    ?s :president ?president .
}
""", initNs=NS)

# print(list(task1))

# for president in task1:
#     print(f"Here is a list of all the presidents: {president}")

#SPARQLWrapper

namespace = "kb" #Default namespace
sparql = SPARQLWrapper("http://10.111.31.31:9999/blazegraph/namespace/"+ namespace + "/sparql")

sparql.setQuery("""
    PREFIX : <http://example.org#>
    SELECT DISTINCT ?president 
    WHERE{
        ?s :president ?president .
    }
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)

print("The list of all presidents are:")
for result in results["results"]["bindings"]:
    print(result["president"]["value"])