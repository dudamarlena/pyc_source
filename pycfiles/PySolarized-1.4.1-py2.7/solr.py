# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pysolarized/solr.py
# Compiled at: 2014-05-26 17:22:08
from __future__ import unicode_literals
import json, logging
from httpcache import CachingHTTPAdapter
import itertools, requests
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

SOLR_ADD_BATCH = 200
logger = logging.getLogger(b'pysolarized')

def _get_url(base, path):
    return (b'/').join(s.strip(b'/') for s in itertools.chain([base, path]))


class SolrResults:

    def __init__(self):
        self.query_time = None
        self.results_count = None
        self.start_index = None
        self.documents = []
        self.facets = {}
        self.highlights = {}
        return


class SolrException(BaseException):
    pass


class Solr(object):

    def __init__(self, endpoints, default_endpoint=None, http_cache=True):
        if not endpoints:
            logger.warning(b'Faulty Solr configuration, SOLR will not be available!')
            return
        else:
            self.endpoints = None
            self.default_endpoint = None
            self._shards = None
            self._add_batch = list()
            self.req_session = requests.Session()
            if http_cache:
                self.req_session.mount(b'http://', CachingHTTPAdapter())
                self.req_session.mount(b'https://', CachingHTTPAdapter())
            if self._is_string(endpoints):
                self.endpoints = {b'default': endpoints}
                self.default_endpoint = b'default'
            else:
                self.endpoints = endpoints
                if default_endpoint:
                    self.default_endpoint = default_endpoint
                else:
                    self.default_endpoint = endpoints[0]
            return

    def _is_string(self, obj):
        try:
            return isinstance(obj, basestring)
        except NameError:
            return isinstance(obj, str)

    def _send_solr_command(self, core_url, json_command):
        """
        Sends JSON string to Solr instance
        """
        url = _get_url(core_url, b'update')
        try:
            response = self.req_session.post(url, data=json_command, headers={b'Content-Type': b'application/json'})
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(b'Failed to send update to Solr endpoint [%s]: %s', core_url, e, exc_info=True)
            raise SolrException(b'Failed to send command to Solr [%s]: %s' % (core_url, e))

        return True

    def _send_solr_query(self, request_url, query):
        try:
            response = self.req_session.post(request_url, data=query)
            response.raise_for_status()
            results = response.json()
        except requests.RequestException as e:
            logger.error(b'Failed to connect to Solr server: %s!', e, exc_info=True)
            return

        return results

    def add(self, documents, boost=None):
        """
        Adds documents to Solr index
        documents - Single item or list of items to add
        """
        if not isinstance(documents, list):
            documents = [
             documents]
        documents = [ {b'doc': d} for d in documents ]
        if boost:
            for d in documents:
                d[b'boost'] = boost

        self._add_batch.extend(documents)
        if len(self._add_batch) > SOLR_ADD_BATCH:
            self._addFlushBatch()

    def _addFlushBatch(self):
        """
        Sends all waiting documents to Solr
        """
        if len(self._add_batch) > 0:
            language_batches = {}
            for lang in self.endpoints:
                document_jsons = [ b'"add":' + json.dumps(data) for data in self._add_batch if data[b'doc'].get(b'language', self.default_endpoint) == lang or lang == self.default_endpoint and not self.endpoints.has_key(data[b'doc'].get(b'language', None))
                                 ]
                command_json = b'{' + (b',').join(document_jsons) + b'}'
                language_batches[lang] = command_json

            for lang in language_batches:
                self._send_solr_command(self.endpoints[lang], language_batches[lang])
                self._add_batch = []

        return

    def deleteAll(self):
        """
        Deletes whole Solr index. Use with care.
        """
        for core in self.endpoints:
            self._send_solr_command(self.endpoints[core], b'{"delete": { "query" : "*:*"}}')

    def delete(self, id):
        """
        Deletes document with ID on all Solr cores
        """
        for core in self.endpoints:
            self._send_solr_command(self.endpoints[core], b'{"delete" : { "id" : "%s"}}' % (id,))

    def commit(self):
        """
        Flushes all pending changes and commits Solr changes
        """
        self._addFlushBatch()
        for core in self.endpoints:
            self._send_solr_command(self.endpoints[core], b'{ "commit":{} }')

    def optimize(self):
        for core in self.endpoints:
            self._send_solr_command(self.endpoints[core], b'{ "optimize": {} }')

    def _get_shards(self):
        """
        Returns comma separated list of configured Solr cores
        """
        if self._shards is None:
            endpoints = []
            for endpoint in self.endpoints:
                url = urlparse.urlparse(self.endpoints[endpoint])
                endpoints.append((b'/').join([url.netloc, url.path]))

            self._shards = (b',').join(endpoints)
        return self._shards

    def _parse_response(self, results):
        """
        Parses result dictionary into a SolrResults object
        """
        dict_response = results.get(b'response')
        result_obj = SolrResults()
        result_obj.query_time = results.get(b'responseHeader').get(b'QTime', None)
        result_obj.results_count = dict_response.get(b'numFound', 0)
        result_obj.start_index = dict_response.get(b'start', 0)
        for doc in dict_response.get(b'docs', []):
            result_obj.documents.append(doc)

        if b'facet_counts' in results:
            facet_types = [
             b'facet_fields', b'facet_dates', b'facet_ranges', b'facet_queries']
            for type in facet_types:
                assert type in results.get(b'facet_counts')
                items = results.get(b'facet_counts').get(type)
                for field, values in items.items():
                    result_obj.facets[field] = []
                    if type == b'facet_ranges':
                        if b'counts' not in values:
                            continue
                        for facet, value in values[b'counts'].items():
                            result_obj.facets[field].append((facet, value))

                        if b'before' in values:
                            result_obj.facets[field].append((b'before', values[b'before']))
                        if b'after' in values:
                            result_obj.facets[field].append((b'after', values[b'after']))
                    else:
                        for facet, value in values.items():
                            if type == b'facet_dates' and (facet == b'gap' or facet == b'between' or facet == b'start' or facet == b'end'):
                                continue
                            result_obj.facets[field].append((facet, value))

        if b'highlighting' in results:
            for key, value in results.get(b'highlighting').items():
                result_obj.highlights[key] = value

        return result_obj

    def query(self, query, filters=None, columns=None, sort=None, start=0, rows=30):
        """
        Queries Solr and returns results

        query - Text query to search for
        filters - dictionary of filters to apply when searching in form of { "field":"filter_value" }
        columns - columns to return, list of strings
        sort - list of fields to sort on in format of ["field asc", "field desc", ... ]
        start - start number of first result (used in pagination)
        rows - number of rows to return (used for pagination, defaults to 30)
        """
        if not columns:
            columns = [
             b'*', b'score']
        fields = {b'q': query, b'json.nl': b'map', 
           b'fl': (b',').join(columns), 
           b'start': str(start), 
           b'rows': str(rows), 
           b'wt': b'json'}
        if len(self.endpoints) > 1:
            fields[b'shards'] = self._get_shards()
        if filters is not None:
            filter_list = []
            for filter_field, value in filters.items():
                filter_list.append(b'%s:%s' % (filter_field, value))

            fields[b'fq'] = (b' AND ').join(filter_list)
        if sort is not None:
            fields[b'sort'] = (b',').join(sort)
        assert self.default_endpoint in self.endpoints
        request_url = _get_url(self.endpoints[self.default_endpoint], b'select')
        results = self._send_solr_query(request_url, fields)
        if not results:
            return
        else:
            if not b'responseHeader' in results:
                raise AssertionError
                results.get(b'responseHeader').get(b'status') == 0 or logger.error(b'Server error while retrieving results: %s', results)
                return
            assert b'response' in results
            result_obj = self._parse_response(results)
            return result_obj

    def more_like_this(self, query, fields, columns=None, start=0, rows=30):
        """
        Retrieves "more like this" results for a passed query document

        query - query for a document on which to base similar documents
        fields - fields on which to base similarity estimation (either comma delimited string or a list)
        columns - columns to return (list of strings)
        start - start number for first result (used in pagination)
        rows - number of rows to return (used for pagination, defaults to 30)
        """
        if isinstance(fields, basestring):
            mlt_fields = fields
        else:
            mlt_fields = (b',').join(fields)
        if columns is None:
            columns = [
             b'*', b'score']
        fields = {b'q': query, b'json.nl': b'map', 
           b'mlt.fl': mlt_fields, 
           b'fl': (b',').join(columns), 
           b'start': str(start), 
           b'rows': str(rows), 
           b'wt': b'json'}
        if len(self.endpoints) > 1:
            fields[b'shards'] = self._get_shards()
        assert self.default_endpoint in self.endpoints
        request_url = _get_url(self.endpoints[self.default_endpoint], b'mlt')
        results = self._send_solr_query(request_url, fields)
        if not results:
            return
        else:
            if not b'responseHeader' in results:
                raise AssertionError
                results.get(b'responseHeader').get(b'status') == 0 or logger.error(b'Server error while retrieving results: %s', results)
                return
            assert b'response' in results
            result_obj = self._parse_response(results)
            return result_obj