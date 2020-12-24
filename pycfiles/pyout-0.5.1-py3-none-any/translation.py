# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mahound/projects/ourse/ourse/translation.py
# Compiled at: 2008-04-05 14:42:51
from database import ObjectProvider, Getter
from rdflib import Literal, URIRef, RDF, BNode
from urlparse import urljoin
from __init__ import ns_ourse
from __init__ import ns_xsd

class ResourceClass:

    def __init__(self, classMap, confGraph):
        res = confGraph.query('PREFIX ourse: <file://ourse.owl#>\n                                    SELECT ?uri ?prov ?targetCls WHERE {\n                                           ?clsmap ourse:class         ?targetCls;\n                                                   ourse:uriPattern    ?uri.\n                                    OPTIONAL {\n                                           ?clsmap  ourse:objectProvider ?prov.\n                                             }.\n                                  } ', initBindings={'?clsmap': classMap})
        for (uri, prov, targetCls) in res:
            self.__uriPattern = uri
            if prov:
                self.__objectProvider = ObjectProvider.create(confGraph, prov)
            self.__targetCls = targetCls

        self.__bindings = {}
        res2 = confGraph.query('PREFIX ourse: <file://ourse.owl#>\n                                    SELECT ?getter ?parameter WHERE {\n                                           ?clsmap ourse:bind        ?binding.\n                                           ?binding ourse:getter     ?getter;\n                                                    ourse:parameter  ?parameter;\n                                  } ', initBindings={'?clsmap': classMap})
        for (getter, parameter) in res2:
            self.__bindings[str(parameter)] = Getter.create(confGraph, getter)

        self.__mappings = {}
        res3 = confGraph.query('PREFIX ourse: <file://ourse.owl#>\n                                     SELECT ?propMap ?prop WHERE {\n                                            ?clsmap ourse:propertyMapping   ?propMap.\n                                            ?propMap ourse:property ?prop.\n                                      }', initBindings={'?clsmap': classMap})
        for (propMap, prop) in res3:
            self.__mappings[propMap] = ClassProperty.create(confGraph, propMap)

    def getURIForObject(self, object, baseURI):
        uri = self.__uriPattern
        if uri == ns_ourse['blankURI']:
            return BNode()
        else:
            for (param, getter) in self.__bindings.iteritems():
                uri = uri.replace('@@%s@@' % param, getter.apply(object))

            return URIRef(urljoin(baseURI, uri))

    def getPropertyMappings(self):
        return self.__mappings

    def getObjectProvider(self):
        return self.__objectProvider

    def getTargetClass(self):
        return self.__targetCls


class ClassProperty:

    @classmethod
    def create(cls, graph, propMapping):
        trType = graph.value(subject=propMapping, predicate=RDF.type, object=None)
        if trType == ns_ourse['SimplePropertyMapping']:
            return LiteralClassProperty(graph.value(subject=propMapping, predicate=ns_ourse['property'], object=None), Getter.create(graph, graph.value(subject=propMapping, predicate=ns_ourse['getter'], object=None)), graph.value(subject=propMapping, predicate=ns_ourse['datatype'], object=None))
        elif trType == ns_ourse['ComplexPropertyMapping']:
            return ResourceClassProperty(graph.value(subject=propMapping, predicate=ns_ourse['property'], object=None), Getter.create(graph, graph.value(subject=propMapping, predicate=ns_ourse['getter'], object=None)), graph.value(subject=propMapping, predicate=ns_ourse['targetClassMap'], object=None))
        else:
            raise Exception('This type of ClassProperty is not supported (%s)!' % str(trType))
        return

    def __init__(self, prop, getter):
        self._property = prop
        self._getter = getter

    def getPredicate(self):
        return self._property


class LiteralClassProperty(ClassProperty):

    def __init__(self, prop, getter, datatype):
        ClassProperty.__init__(self, prop, getter)
        self.__datatype = datatype

    def getValue(self, object):
        value = self._getter.apply(object)
        if self.__datatype == ns_xsd['anyURI']:
            value = URIRef(value)
        return value


class ResourceClassProperty(ClassProperty):

    def __init__(self, prop, getter, targetClassMap):
        ClassProperty.__init__(self, prop, getter)
        self.__targetClassMap = targetClassMap

    def getResourceObject(self, object):
        return self._getter.apply(object)

    def getTargetClass(self):
        return self.__targetClassMap