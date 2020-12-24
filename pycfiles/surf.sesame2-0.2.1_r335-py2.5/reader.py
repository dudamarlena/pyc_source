# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sesame2/reader.py
# Compiled at: 2011-04-12 03:29:53
__author__ = 'Cosmin Basca'
from surf.util import json_to_rdflib
from surf.plugin.query_reader import RDFQueryReader
from allegro import Allegro

class ReaderPlugin(RDFQueryReader):

    def __init__(self, *args, **kwargs):
        RDFQueryReader.__init__(self, *args, **kwargs)
        self.__server = kwargs['server'] if 'server' in kwargs else 'localhost'
        self.__port = kwargs['port'] if 'port' in kwargs else 6789
        self.__root_path = kwargs['root_path'] if 'root_path' in kwargs else '/sesame'
        self.__repository_path = kwargs['repository_path'] if 'repository_path' in kwargs else ''
        self.__repository = kwargs['repository'] if 'repository' in kwargs else None
        self.__use_allegro_extensions = kwargs['use_allegro_extensions'] if 'use_allegro_extensions' in kwargs else False
        self.log.info('INIT: %s, %s, %s, %s' % (self.server,
         self.port,
         self.root_path,
         self.repository_path))
        if not self.repository:
            raise Exception('No <repository> argument supplied.')
        if self.__use_allegro_extensions:
            opened = self.get_allegro().open_repository(self.repository)
            self.log.info('ALLEGRO repository opened: %s' % opened)
        return

    server = property(lambda self: self.__server)
    port = property(lambda self: self.__port)
    root_path = property(lambda self: self.__root_path)
    repository_path = property(lambda self: self.__repository_path)
    repository = property(lambda self: self.__repository)
    use_allegro_extensions = property(lambda self: self.__use_allegro_extensions)

    def _to_table(self, result):
        return result

    def _ask(self, result):
        """
        returns the boolean value of a ASK query
        """
        return result

    def get_allegro(self):
        return Allegro(self.server, self.port, self.root_path, self.repository_path)

    def _execute(self, query):
        q_string = unicode(query)
        result = self.execute_sparql(q_string)
        if 'boolean' in result:
            return result['boolean']
        converted = []
        for binding in result['results']['bindings']:
            rdf_item = {}
            for (key, obj) in binding.items():
                try:
                    rdf_item[key] = json_to_rdflib(obj)
                except ValueError:
                    continue

            converted.append(rdf_item)

        return converted

    def execute_sparql(self, query, format='JSON'):
        try:
            self.log.debug(query)
            result = self.get_allegro().sparql_query(self.repository, query, infer=self.inference, format='sparql+json')
            if type(result) == bool:
                return {'head': {}, 'boolean': result}
            else:
                return result
        except Exception, e:
            self.log.exception('Exception on query')

    def close(self):
        pass