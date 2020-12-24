# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/djubby/configuration.py
# Compiled at: 2010-04-16 07:39:30
import os, logging
from django.conf import settings
from rdflib.Graph import ConjunctiveGraph
import rdf, ns

class Configuration:
    """Configuration using the Borg design pattern"""
    __shared_state = {'data': None, 'path': None, 'graph': None, 'endpoint': None}

    def __init__(self, path=None):
        self.__dict__ = self.__shared_state
        if self.data == None:
            if path == None:
                raise ValueError("djubby's configuration MUST be initialized a first time, read http://code.google.com/p/djubby/wiki/GettingStarted")
            else:
                self.path = os.path.abspath(path)
                logging.debug("Reading djubby's configuration from %s..." % self.path)
                if not os.path.exists(self.path):
                    raise ValueError("Not found a proper file at '%s' with a configuration for djubby. Please, provide a right path" % self.path)
                data = ConjunctiveGraph()
                data.bind('conf', ns.config)
                try:
                    data.load(path, format='n3')
                except Exception, e:
                    raise ValueError("Not found a proper N3 file at '%s' with a configuration for djubby. Please, provide a valid N3 file" % self.path)
                else:
                    self.data = data
                    try:
                        self.graph = self.get_value('sparqlDefaultGraph')
                        self.endpoint = self.get_value('sparqlEndpoint')
                    except Exception, e:
                        raise ValueError("Not found the graph not the endpoint that it's supposed djubby have to query. Please, provide a right donfiguration")
                    else:
                        logging.info('Using <%s> as default graph to query the endpoint <%s>' % (self.graph, self.endpoint))
                        self.__class__.__dict__['_Configuration__shared_state']['data'] = data
        return

    def get_values(self, prop):
        return rdf.get_values(self.data, predicate=ns.config[prop])

    def get_value(self, prop):
        return rdf.get_value(self.data, predicate=ns.config[prop])