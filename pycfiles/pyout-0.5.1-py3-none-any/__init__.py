# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mahound/projects/ourse/ourse/__init__.py
# Compiled at: 2008-04-05 15:27:03
import re
from rdflib import Namespace, RDF
from rdflib.Graph import Graph, ConjunctiveGraph
from rdflib.store.IOMemory import IOMemory
ns_ourse = Namespace('file://ourse.owl#')
ns_xsd = Namespace('http://www.w3.org/2001/XMLSchema#')

class OURSE:

    def __init__(self, configGraph, absoluteURL='/', storage=IOMemory()):
        self.__config = configGraph
        self.__databases = {}
        self.__classMappings = {}
        self.__absoluteURL = absoluteURL
        self.__storage = storage
        self.__graph = ConjunctiveGraph(store=storage)
        self.__objectGraphMap = {}
        self.setupSources()
        self.setupProvidedClassMappings()

    def setupSources(self):
        res = self.__config.query('PREFIX ourse: <file://ourse.owl#>\n                             SELECT ?db ?dsn ?driver ?username ?password WHERE {\n                             ?db     ourse:DSN      ?dsn;\n                                     ourse:Driver   ?driver.\n                             OPTIONAL {\n                                ?db    ourse:username ?username;\n                                       ourse:password ?password.}}')
        for (db, dsn, driver, username, password) in res:
            m = re.match('(?P<protocol>.+)://(?P<address>.+)', dsn)
            if m == None:
                raise Exception('DSN %s is not valid' % dsn)
            protocol = m.group('protocol')
            address = m.group('address')
            driverName = '%sDriver' % driver
            clazz = getattr(__import__('driver.%s' % driverName, globals(), locals(), ['']), driverName)
            self.__databases[db] = clazz(protocol, address.encode('latin-1'), username, password)

        return

    def getSourceList(self):
        return self.__databases

    def setupProvidedClassMappings(self):
        from translation import ResourceClass
        for node in self.__config.subjects(RDF.type, ns_ourse['ClassMap']):
            self.__classMappings[node] = ResourceClass(node, self.__config)

    def getClassMappings(self):
        return self.__classMappings

    def getConjunctiveGraph(self):
        return self.__graph

    def getGraphFromMapping(self, mapping, bindings, expand=False):
        try:
            resourceClass = self.__classMappings[mapping]
        except KeyError:
            return

        provider = resourceClass.getObjectProvider()
        database = self.__databases[provider.getDBMapping()]
        database.startRequest()
        runner = provider.createRunner(database)
        storage = self.__storage
        graph = self.__graph
        from storage import GraphFiller
        filler = GraphFiller(self, self.__objectGraphMap, graph, storage, database)
        obj = runner.execute(bindings)
        this = self.getObjectReference(resourceClass, obj, self.__absoluteURL)
        filler.loadObject(this, resourceClass, obj, expand=expand, uri=self.__absoluteURL)
        database.endRequest()
        return self.__objectGraphMap[this]

    def getObjectReference(self, resourceClass, object, baseURI):
        return resourceClass.getURIForObject(object, baseURI)