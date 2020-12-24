# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mahound/projects/ourse/ourse/database.py
# Compiled at: 2008-04-05 15:02:15
import re
from rdflib import RDF
from __init__ import ns_ourse

class ObjectProvider:

    @classmethod
    def create(cls, graph, provider):
        provType = graph.value(subject=provider, predicate=RDF.type, object=None)
        if provType == ns_ourse['PathObjectProvider']:
            return PathObjectProvider(graph.value(subject=provider, predicate=ns_ourse['DBPath'], object=None), graph.value(subject=provider, predicate=ns_ourse['dataStorage'], object=None))
        else:
            raise Exception('This type of ObjectProvider is not supported (%s)!' % str(provType))
        return

    def __init__(self, dbStorage):
        self.__dbStorage = dbStorage

    def getDBMapping(self):
        return self.__dbStorage


class PathObjectProvider(ObjectProvider):

    def __init__(self, dbPath, dataStorage):
        ObjectProvider.__init__(self, dataStorage)
        self._dbPath = dbPath

    def createRunner(self, driver):
        return driver.PathRunner(driver, self._dbPath)


class Getter:

    @classmethod
    def create(cls, graph, getter):
        getType = graph.value(subject=getter, predicate=RDF.type, object=None)
        if getType == ns_ourse['MethodGetter']:
            return MethodGetter(graph.value(subject=getter, predicate=ns_ourse['method'], object=None))
        elif getType == ns_ourse['ViewGetter']:
            return ViewGetter(graph.value(subject=getter, predicate=ns_ourse['view'], object=None))
        elif getType == ns_ourse['IdentityGetter']:
            return IdentityGetter()
        else:
            raise Exception('This type of Getter is not supported (%s)!' % str(getType))
        return


class IdentityGetter(Getter):

    def apply(self, object):
        return object


class ViewGetter(Getter):

    def __init__(self, view):
        self.__viewName = view

    def apply(self, object):
        moduleName = ('.').join(self.__viewName.split('.')[:-1])
        className = self.__viewName.split('.')[(-1)]
        clazz = getattr(__import__(moduleName.replace('.', '/'), globals(), locals(), ['']), className)
        obj = clazz(object).run()
        return clazz(object).run()


class MethodGetter(Getter):

    def __init__(self, method):
        self._method = method

    def apply(self, object):
        return getattr(object, self._method)()