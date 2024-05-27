from rdflib import Graph, Namespace, Literal, BNode, RDF
from rdflib.collection import Collection

g = Graph()

ex = Namespace("http://example.org/")

g.bind("ex", ex)

#Reservior Dogs is a movie.
g.add((ex.Reservoir_Dogs, RDF.type, ex.Movie))

#Reservoir Docs is directed by Quentin Tarantino
g.add((ex.Quentin_Tarantino, ex.director_of, ex.Reservoir_Dogs))

#The German title of Reservoir Dogs is "Reservoir Dogs - Wilde Hunde".
g.add((ex.Reservoir_Dogs, ex.title, Literal("Reservoir Dogs - Wilde Hunde", lang="de")))

#Quentin Tarantino is the only director of Pulp Fiction
b1 = BNode()
Collection(g, b1, [ex.Quentin_Tarantino])
g.add((ex.Pulp_Fiction, ex.list_of_directors, b1))

print(g.serialize())