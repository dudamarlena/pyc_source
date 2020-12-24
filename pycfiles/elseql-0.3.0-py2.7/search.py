# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/elseql/search.py
# Compiled at: 2018-02-06 20:17:32
from __future__ import print_function
from requests.exceptions import ConnectionError
from parser import ElseParser, ElseParserException
import rawes, pprint
try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

DEFAULT_PORT = 'localhost:9200'

def _csval(v):
    if not v:
        return ''
    if not isinstance(v, basestring):
        return str(v)
    if v.isalnum():
        return v
    return '"%s"' % v.replace('"', '""')


def _csvline(l):
    try:
        return (',').join([ _csval(v).encode('utf-8') for v in l ])
    except UnicodeDecodeError:
        raise Exception('UnicodeDecodeError for %s' % l)


class ElseSearch(object):

    def __init__(self, port=None, debug=False):
        self.debug = debug
        self.print_query = False
        self.es = None
        self.mapping = None
        self.keywords = None
        self.host = None
        self.version = None
        self.v5 = None
        if port:
            try:
                self.es = rawes.Elastic(port, headers={'content-type': 'application/json'})
                self.get_mapping()
                self.get_version()
            except ConnectionError as err:
                print('init: cannot connect to', port)
                print(err)

        if not self.es:
            self.debug = True
        return

    def get_version(self):
        if not self.version:
            try:
                info = self.es.get('')
                self.version = info['version']['number']
                self.v5 = self.version[:2] >= '5.'
            except ConnectionError as err:
                print('mapping: cannot connect to', self.es.url)
                print(err)

        return self.version

    def get_mapping(self):
        if not self.mapping:
            try:
                self.mapping = self.es.get('_mapping')
                self.keywords = []
                self.host = self.es.url
            except ConnectionError as err:
                print('mapping: cannot connect to', self.es.url)
                print(err)

        return self.mapping

    def get_keywords(self):
        if self.keywords:
            return self.keywords
        keywords = ['facets', 'filter', 'query', 'exist', 'missing', 'script',
         'from', 'where', 'in', 'between', 'like', 'order by', 'limit', 'and', 'or', 'not']
        if not self.mapping:
            return sorted(keywords)

        def add_properties(plist, doc):
            if 'properties' in doc:
                props = doc['properties']
                for p in props:
                    plist.append(p)
                    add_properties(plist, props[p])

        keywords.extend(['_score', '_all'])
        for i in self.mapping:
            keywords.append(i)
            index = self.mapping[i]
            for t in index:
                keywords.append(t)
                document = index[t]
                if '_source' in document:
                    source = document['_source']
                    if 'enabled' not in source or source['enabled']:
                        keywords.append('_source')
                add_properties(keywords, document)

        self.keywords = sorted(set(keywords))
        return self.keywords

    def search(self, query, explain=False, validate=False):
        try:
            request = ElseParser.parse(query)
        except ElseParserException as err:
            print(err.pstr)
            print(' ' * err.loc + '^\n')
            print('ERROR:', err)
            return 1

        params = {}
        data_fields = None
        if request.query:
            data = {'query': {'query_string': {'query': str(request.query), 'default_operator': 'AND'}}}
        else:
            data = {'query': {'match_all': {}}}
        if explain:
            data['explain'] = True
        if request.filter:
            filter = request.filter
            if filter.name == 'query':
                data['filter'] = {'query': {'query_string': {'query': str(filter), 'default_operator': 'AND'}}}
            else:
                data['filter'] = {filter.name: {'field': str(filter)}}
        if request.facets:
            data['facets'] = dict((f, {'terms': {'field': f}}) for f in request.facets)
        if request.script:
            data['script_fields'] = {request.script[0]: {'script': request.script[1]}}
        if request.fields:
            fields = request.fields
            fields_k = '_source' if self.v5 else 'fields'
            if len(fields) == 1:
                if fields[0] == '*':
                    pass
                elif fields[0] == 'count(*)':
                    pass
                else:
                    data[fields_k] = [
                     fields[0]]
            else:
                data[fields_k] = [ x for x in fields ]
            data_fields = data.get(fields_k)
        if request.order:
            data['sort'] = [ {x[0]: x[1]} for x in request.order ]
        if request.limit:
            qfrom = None
            qsize = None
            if len(request.limit) > 1:
                qfrom = request.limit.pop(0)
            qsize = request.limit[0]
            if qfrom is None:
                data['size'] = qsize
            elif qfrom >= 0:
                data['from'] = qfrom
                data['size'] = qsize
            else:
                params.update({'search_type': 'scan', 'scroll': '10m', 'size': qsize})
        if validate:
            command = '/_validate/query'
            params.update({'pretty': 'true', 'explain': 'true'})
            if 'query' in data:
                q = data.pop('query')
                data.update(q)
        else:
            command = '/_search'
        if request.routing:
            command += '?routing=%s' % request.routing
        command_path = request.index.replace('.', '/') + command
        if self.debug:
            HTTPConnection.debuglevel = 1
            print()
            print('GET', command_path, params or '')
            print('  ', pprint.pformat(data))
            params.update({'pretty': 'true'})
        else:
            HTTPConnection.debuglevel = 0
        if self.print_query:
            print()
            print('; ', _csval(query))
            print()
        total = None
        print_fields = True
        do_query = True
        while self.es and do_query:
            try:
                result = self.es.get(command_path, params=params, data=data)
            except ConnectionError as err:
                print('cannot connect to', self.es.url)
                print(err)
                return

            if self.debug:
                print()
                print('RESPONSE:', pprint.pformat(result))
                print()
            if '_scroll_id' in result:
                params['scroll_id'] = result['_scroll_id']
                if 'search_type' in params:
                    params.pop('search_type')
                    command_path = '_search/scroll'
            else:
                do_query = False
            if 'valid' in result:
                if 'explanations' in result:
                    for e in result['explanations']:
                        print()
                        for k, v in e.iteritems():
                            print(k, ':', v)

                else:
                    print('valid:', result['valid'])
                return
            if 'error' in result:
                print('ERROR:', result['error'])
                return
            if 'shards' in result and 'failures' in result['_shards']:
                failures = result['_shards']['failures']
                for f in failures:
                    print('ERROR:', f['reason'])

                return
            if 'hits' in result:
                hits = result['hits']
                total = hits['total']
                if data_fields and not self.v5:
                    if print_fields:
                        print_fields = False
                        print(_csvline(data_fields))
                    for _ in hits['hits']:
                        result_fields = _['fields'] if 'fields' in _ else {}
                        print(_csvline([ _.get(x) or result_fields.get(x) for x in data_fields ]))

                else:
                    if hits['hits']:
                        if print_fields:
                            print_fields = False
                            print(_csvline(hits['hits'][0]['_source'].keys()))
                    else:
                        do_query = False
                    for _ in hits['hits']:
                        print(_csvline([ _csval(x) for x in _['_source'].values() ]))

            if 'facets' in result:
                for facet in result['facets']:
                    print()
                    print('%s,count' % _csval(facet))
                    for _ in result['facets'][facet]['terms']:
                        t = _['term']
                        c = _['count']
                        print('%s,%s' % (_csval(t), c))

            if do_query and self.debug:
                print()
                print('GET', command_path, params or '')
                print('  ', pprint.pformat(data))

        if total is not None:
            print()
            print('total: ', total)
        return