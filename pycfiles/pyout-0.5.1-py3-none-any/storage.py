# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mahound/projects/ourse/ourse/storage.py
# Compiled at: 2008-04-05 15:28:27
from rdflib import BNode, RDF, URIRef, Literal
from rdflib.Graph import Graph
from translation import ResourceClass, LiteralClassProperty, ResourceClassProperty

class GraphFiller:

    def __init__(self, ourse, objGraphMap, graph, storage, database):
        self.__graph = graph
        self.__storage = storage
        self.__objectGraphMap = objGraphMap
        self.__ourse = ourse
        self.__database = database

    def loadObject(self, this, resourceClass, object, expand=True, uri='/'):
        existing = self.__objectGraphMap.get(this, None)
        if existing:
            return this
        graph = Graph(store=self.__storage, identifier=this)
        self.__objectGraphMap[this] = graph
        graph.add((this, RDF.type, resourceClass.getTargetClass()))
        for (propMap, prop) in resourceClass.getPropertyMappings().iteritems():
            if prop.__class__ == LiteralClassProperty:
                value = prop.getValue(object)
                if not self.__database.isList(value):
                    value = [
                     value]
                for v in value:
                    if type(v) != URIRef:
                        v = Literal(v)
                    graph.add((this, prop.getPredicate(), v))

            elif prop.__class__ == ResourceClassProperty:
                propObjectList = prop.getResourceObject(object)
                if not self.__database.isList(propObjectList):
                    propObjectList = [
                     propObjectList]
                for propObject in propObjectList:
                    try:
                        classMapping = self.__ourse.getClassMappings()[prop.getTargetClass()]
                    except KeyError:
                        raise Exception("No mapping for target class '%s' was found" % prop.getTargetClass())

                    resource = self.__ourse.getObjectReference(classMapping, propObject, uri)
                    if expand or resource.__class__ == BNode:
                        resource = self.loadObject(resource, classMapping, propObject, expand=True, uri=uri)
                    graph.add((this, prop.getPredicate(), resource))

        return this