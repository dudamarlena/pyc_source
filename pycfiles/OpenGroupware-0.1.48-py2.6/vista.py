# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/vista/vista.py
# Compiled at: 2012-10-12 07:02:39
import json, datetime, time
from coils.core import *
from coils.net import PathObject, Protocol
from coils.core.omphalos import Render as Omphalos_Render

def omphalos_encode(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S')
    raise TypeError()


class VistaSearch(Protocol, PathObject):
    __pattern__ = 'vista'
    __namespace__ = None
    __xmlrpc__ = False

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)

    def get_name(self):
        return 'vista'

    def is_public(self):
        return False

    def do_HEAD(self):
        self.request.simple_response(200, data=None, mimetype=self.entity.get_mimetype(type_map=self._mime_type_map), headers={'etag': 'vista-search'})
        return

    def do_GET(self):
        include_archived = 'archived' in [ x.lower() for x in self.parameters ]
        if 'type' in self.parameters:
            entity_types = [ x.lower() for x in self.parameters['type'] ]
        else:
            entity_types = None
        search_limit = self.parameters.get('limit', None)
        if search_limit:
            search_limit = int(search_limit[0])
        else:
            search_limit = None
        if 'term' in self.parameters:
            keywords = [ x.lower().replace(' ', '\\ ') for x in self.parameters['term'] ]
        else:
            keywords = [
             self.context.login]
        detail_level = self.parameters.get('detail', None)
        if detail_level:
            detail_level = int(detail_level[0])
        else:
            detail_level = 2056
        start = time.time()
        results = self.context.run_command('vista::search', keywords=keywords, entity_types=entity_types, search_limit=0, include_archived=include_archived)
        end = time.time()
        self.context.send(None, 'coils.administrator/performance_log', {'lname': 'vista', 'oname': 'query', 
           'runtime': end - start, 
           'error': False})
        result_count = len(results)
        if len(results) > 100:
            results = results[:100]
        start = time.time()
        results = Omphalos_Render.Results(results, detail_level, self.context)
        results = json.dumps(results, default=omphalos_encode)
        end = time.time()
        self.context.send(None, 'coils.administrator/performance_log', {'lname': 'vista', 'oname': 'render', 
           'runtime': end - start, 
           'error': False})
        self.request.simple_response(200, mimetype='text/plain', headers={'X-OpenGroupware-Coils-Vista-Matches': str(result_count)}, data=results)
        return