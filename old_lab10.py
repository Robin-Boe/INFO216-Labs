import owlrl
from rdflib import Graph, OWL, RDF, RDFS, BNode, Namespace, Literal, XSD, FOAF, URIRef
from rdflib.collection import Collection

g = Graph()

ex = Namespace('http://example.org/')

g.bind("ex", ex)

#anyone who is a graduate has at least one degree
task1_b1 = BNode()
g.add((task1_b1, RDF.type, OWL.Restriction))
g.add((task1_b1, OWL.onProperty, ex.degree))
g.add((task1_b1, OWL.minCardinality, Literal("1", datatype=XSD.integer)))

task1_b2 = BNode()
Collection(g, task1_b2, [ex.Person, task1_b1])
g.add((ex.Graduate, OWL.intersectionOf, task1_b2))

#anyone who is a university graduate has at least one degree from a university
task2_b1 = BNode()
g.add((task2_b1, RDF.type, OWL.Restriction))
g.add((task2_b1, OWL.onProperty, ex.degree))
g.add((task2_b1, OWL.someValuesFrom, ex.University))

task2_b2 = BNode()
Collection(g, task2_b2, [ex.Graduate, task2_b1])
g.add((ex.University_Graduate, OWL.intersectionOf, task2_b2))

#a grade is either an A, B, C, D, E or F
task3_b1 = BNode()
task3_b2 = BNode()
Collection(g, task3_b2, [Literal("A"), Literal("B"), Literal("C"), Literal("D"), Literal("E"), Literal("F")])
g.add((task3_b1, RDF.type, RDFS.Datatype))
g.add((task3_b1, OWL.oneOf, task3_b2))
g.add((ex.grade, RDFS.range, task3_b1))

#a straight A student is a student that has only A grades
task4_b1 = BNode()
g.add((task4_b1, RDF.type, OWL.Restriction))
g.add((task4_b1, OWL.onProperty, ex.grade))
g.add((task4_b1, OWL.allValuesFrom, Literal("A")))

task4_b2 = BNode()
g.add((task4_b2, RDF.type, OWL.Restriction))
g.add((task4_b2, OWL.onProperty, ex.grade))
g.add((task4_b2, OWL.someValuesFrom, Literal("A")))

task4_b3 = BNode()
Collection(g, task4_b3, [ex.Student, task4_b1, task4_b2])
g.add((ex.Straight_A_Student, OWL.intersectionOf, task4_b3))

#a graduate has no F grades
task5_b1 = BNode()
Collection(g, task5_b1, [Literal("A"), Literal("B"), Literal("C"), Literal("D"), Literal("E")])

task5_b2 = BNode()
g.add((task5_b2, RDFS.range, RDFS.Datatype))
g.add((task5_b2, OWL.oneOf, task5_b1))

task5_b3 = BNode()
g.add((task5_b3, RDF.type, OWL.Restriction))
g.add((task5_b3, OWL.onProperty, ex.grade))
g.add((task5_b3, OWL.allValuesFrom, task5_b2))

g.add((ex.Graduate, OWL.intersectionOf, task5_b3))

#a student has a unique student number
g.add((ex.Student_Number, RDF.type, OWL.FunctionalProperty))
g.add((ex.Student_Number, RDF.type, OWL.InverseFunctionalProperty))

#each student has exactly one average grade
task7_b1 = BNode()
g.add((task7_b1, RDF.type, OWL.Restriction))
g.add((task7_b1, OWL.onProperty, ex.averageGrade))
g.add((task7_b1, OWL.cardinality, Literal("1", datatype=XSD.integer)))

task7_b2 = BNode()
g.add((task7_b2, RDF.type, OWL.Restriction))
g.add((task7_b2, OWL.onProperty, ex.studentNumber))
g.add((task7_b2, OWL.cardinality, Literal("1", datatype=XSD.integer)))

task7_b3 = BNode()
Collection(g, task7_b3, [ex.Person, task7_b1, task7_b2])
g.add((ex.Student, OWL.intersectionOf, task7_b3))

#a course is either a bachelor, a master or a Ph.D course
task8_b1 = BNode()
Collection(g, task8_b1, [ex.Bachelor_Course, ex.Master_Course, ex["Ph.D_Course"]])

task8_b2 = BNode()
g.add((task8_b2, OWL.oneOf, task8_b1))
g.add((ex.Course, RDFS.subClassOf, task8_b2))

#a bachelor student takes only bachelor courses
g.add((ex.Bachelor_Student, RDFS.subClassOf, ex.Student))

task9_b1 = BNode()
g.add((task9_b1, RDF.type, OWL.Restriction))
g.add((task9_b1, OWL.onProperty, ex.hasCourse))
g.add((task9_b1, OWL.allValuesFrom, ex.Bachelor_Course))

task9_b2 = BNode()
Collection(g, task9_b2, [ex.Student, task9_b1])
g.add((ex.Bachelor_Student, OWL.intersectionOf, task9_b2))

#a master student takes only master courses, except for at most one bachelor course
g.add((ex.Master_Student, RDFS.subClassOf, ex.Student))

task10_b1 = BNode()
g.add((task10_b1, RDF.type, OWL.Restriction))
g.add((task10_b1, OWL.onProperty, ex.hasCourse))
g.add((task10_b1, OWL.onClass, ex.Bachelor_Course))
g.add((task10_b1, OWL.maxQualifiedCardinality, Literal("1", datatype=XSD.integer)))

task10_b2 = BNode()
g.add((task10_b2, RDF.type, OWL.Restriction))
g.add((task10_b2, OWL.onProperty, ex.hasCourse))
g.add((task10_b2, OWL.someValuesFrom, ex.Master_Course))

task10_b3 = BNode()
Collection(g, task10_b3, [task10_b1, task10_b2])

task10_b4 = BNode()
g.add((task10_b4, RDF.type, OWL.Restriction))
g.add((task10_b4, OWL.onProperty, ex.hasCourse))
g.add((task10_b4, OWL.allValuesFrom, task10_b3))

task10_b5 = BNode()
Collection(g, task10_b5, [ex.Student, task10_b4])
g.add((ex.Master_Student, OWL.intersectionOf, task10_b5))

#a Ph.D student takes only Ph.D courses, except for at most two masters courses
g.add((ex["Ph.D_Student"], RDFS.subClassOf, ex.Student))

task11_b1 = BNode()
g.add((task11_b1, RDF.type, OWL.Restriction))
g.add((task11_b1, OWL.onProperty, ex.hasCourse))
g.add((task11_b1, OWL.onClass, ex.Master_Course))
g.add((task11_b1, OWL.maxQualifiedCardinality, Literal("2", datatype=XSD.integer)))

task11_b2 = BNode()
g.add((task11_b2, RDF.type, OWL.Restriction))
g.add((task11_b2, OWL.onProperty, ex.hasCourse))
g.add((task11_b2, OWL.someValuesFrom, ex["Ph.D_Course"]))

task11_b3 = BNode()
Collection(g, task11_b3, [task11_b1, task11_b2])

task11_b4 = BNode()
g.add((task11_b4, RDF.type, OWL.Restriction))
g.add((task11_b4, OWL.onProperty, ex.hasCourse))
g.add((task11_b4, OWL.allValuesFrom, task11_b3))

task11_b5 = BNode()
Collection(g, task11_b5, [ex.Student, task11_b4])
g.add((ex["Ph.D_Student"], OWL.intersectionOf, task11_b5))

#a Ph.D. student cannot take any bachelor course
task12_b1 = BNode()
g.add((task12_b1, RDF.type, OWL.Restriction))
g.add((task12_b1, OWL.onProperty, ex.course))
g.add((task12_b1, OWL.allValuesFrom, ex.bachelor_courses))

g.add((ex.PhD_Student, OWL.complementOf, task12_b1))

print(g.serialize())
# g.serialize("old_lab10.ttl", format="ttl")