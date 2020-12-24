# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_oldcollections_search.py
# Compiled at: 2016-09-19 13:27:02
"""This module tests the collection search functionality, i.e., requests to SEARCH
/collections and POST /collections/search.

NOTE: getting the non-standard http SEARCH method to work in the tests required
using the request method of TestController().app and specifying values for the
method, body, headers, and environ kwarg parameters.  WebTest prints a
WSGIWarning when unknown HTTP methods (e.g., SEARCH) are used.  To prevent this,
I altered the global valid_methods tuple of webtest.lint at runtime by adding a
'SEARCH' method (see _add_SEARCH_to_web_test_valid_methods() below).
"""
import re
from onlinelinguisticdatabase.tests import TestController, url
from nose.tools import nottest
import simplejson as json, logging
from datetime import date, datetime, timedelta
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)
today_timestamp = datetime.now()
day_delta = timedelta(1)
yesterday_timestamp = today_timestamp - day_delta
jan1 = date(2012, 1, 1)
jan2 = date(2012, 1, 2)
jan3 = date(2012, 1, 3)
jan4 = date(2012, 1, 4)

def isofy(date):
    try:
        return date.isoformat()
    except AttributeError:
        return date


class TestFormsSearchController(TestController):
    md_contents = ('\n').join([
     'Chapter',
     '=======',
     '',
     'Section',
     '-------',
     '',
     '* Item 1',
     '* Item 2',
     '',
     'Section containing forms',
     '------------------------',
     ''])
    rst_contents = ('\n').join([
     'Chapter',
     '=======',
     '',
     'Section',
     '-------',
     '',
     '- Item 1',
     '- Item 2',
     '',
     'Section containing forms',
     '------------------------',
     ''])

    def _create_test_models(self, n=20):
        self._add_test_models_to_session('Tag', n, ['name'])
        self._add_test_models_to_session('Speaker', n, ['first_name', 'last_name', 'dialect'])
        self._add_test_models_to_session('Source', n, ['author_first_name', 'author_last_name', 'title', 'year'])
        self._add_test_models_to_session('Form', n, ['transcription', 'datetime_entered', 'datetime_modified'])
        self._add_test_models_to_session('File', n, ['name', 'datetime_entered', 'datetime_modified'])
        Session.commit()

    def _add_test_models_to_session(self, model_name, n, attrs):
        for i in range(1, n + 1):
            m = getattr(model, model_name)()
            for attr in attrs:
                if attr in 'datetime_modified, datetime_entered':
                    setattr(m, attr, datetime.now())
                elif attr == 'year':
                    setattr(m, attr, 2000)
                else:
                    setattr(m, attr, '%s %s' % (attr, i))

            Session.add(m)

    def _get_test_models(self):
        return {'tags': [ t.__dict__ for t in h.get_tags() ], 'forms': [ f.__dict__ for f in h.get_forms() ], 'files': [ f.__dict__ for f in h.get_files() ], 'sources': [ s.__dict__ for s in h.get_sources() ], 'speakers': [ s.__dict__ for s in h.get_speakers() ], 'users': [ u.__dict__ for u in h.get_users() ]}

    def _create_test_data(self, n=20):
        self._create_test_models(n)
        self._create_test_collections(n)

    def _create_test_collections(self, n=20):
        """Create n collections  with various properties.  A testing ground for searches!
        """
        test_models = self._get_test_models()
        tags = dict([ (t['name'], t) for t in test_models['tags'] ])
        contributor = [ u for u in test_models['users'] if u['role'] == 'contributor' ][0]
        for i in range(1, n + 1):
            params = self.collection_create_params.copy()
            params.update({'speaker': test_models['speakers'][(i - 1)]['id']})
            if i > 10:
                params.update({'title': 'Collection %d' % i, 
                   'date_elicited': '%02d/%02d/%d' % (jan1.month, jan1.day, jan1.year)})
            else:
                params.update({'title': 'collection %d' % i, 
                   'tags': [
                          tags[('name %d' % i)]['id']]})
            if i in (13, 15):
                params.update({'date_elicited': '%02d/%02d/%d' % (jan3.month, jan3.day, jan3.year), 
                   'elicitor': contributor['id']})
            if i > 5 and i < 16:
                params.update({'files': [
                           test_models['files'][(i - 1)]['id']], 
                   'markup_language': 'Markdown', 
                   'contents': '%s\nform[%d]\n' % (self.md_contents, test_models['forms'][(i - 1)]['id'])})
            else:
                params.update({'files': [
                           test_models['files'][0]['id']], 
                   'markup_language': 'reStructuredText', 
                   'contents': '%s\nform[%d]\n' % (self.rst_contents, test_models['forms'][(i - 1)]['id'])})
            params = json.dumps(params)
            self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin)

    n = 20

    def tearDown(self):
        pass

    @nottest
    def test_a_initialize(self):
        """Tests POST /collections/search: initialize database."""
        h.clear_all_models(['Language', 'User'])
        self._create_test_data(self.n)
        self._add_SEARCH_to_web_test_valid_methods()

    @nottest
    def test_search_b_equals(self):
        """Tests POST /collections/search: equals."""
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', '=', 'Collection 13']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['title'] == 'Collection 13'

    @nottest
    def test_search_c_not_equals(self):
        """Tests SEARCH /collections: not equals."""
        json_query = json.dumps({'query': {'filter': ['not', ['Collection', 'title', '=', 'collection 10']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == self.n - 1
        assert 'Collection 10' not in [ c['title'] for c in resp ]

    @nottest
    def test_search_d_like(self):
        """Tests POST /collections/search: like."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'like', '%1%']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '1' in c['title'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'like', '%C%']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if 'C' in c['title'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['or',
                              [
                               [
                                'Collection', 'title', 'like', 'C%'],
                               [
                                'Collection', 'title', 'like', 'c%']]]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if 'C' in c['title'] or 'c' in c['title'] ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_e_not_like(self):
        """Tests SEARCH /collections: not like."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['not', ['Collection', 'title', 'like', '%1%']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '1' not in c['title'] ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_f_regexp(self):
        """Tests POST /collections/search: regular expression."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '[345]2']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if re.search('[345]2', c['title']) ]
        assert sorted([ c['title'] for c in resp ]) == sorted([ c['title'] for c in result_set ])
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '^C']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['title'][0] == 'C' ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '^[Cc]']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['title'][0] in ('C', 'c') ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '^[Cc]ollection 1$']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['title'] in ('Collection 1', 'collection 1') ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '1{1,}']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if re.search('1{1,}', c['title']) ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '[123]{2,}']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if re.search('[123]{2,}', c['title']) ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'regex', '[123]{3,2}']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'

    @nottest
    def test_search_g_not_regexp(self):
        """Tests SEARCH /collections: not regular expression."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['not', ['Collection', 'title', 'regexp', '[345]2']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if not re.search('[345]2', c['title']) ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_h_empty(self):
        """Tests POST /collections/search: is NULL."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'description', '=', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['description'] is None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['not', ['Collection', 'description', '!=', None]]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_i_not_empty(self):
        """Tests SEARCH /collections: is not NULL."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['not', ['Collection', 'description', '=', None]]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['description'] is not None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'description', '!=', None]}})
        response = self.app.request(url('collections'), body=json_query, method='SEARCH', headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_j_invalid_json(self):
        """Tests POST /collections/search: invalid JSON params."""
        json_query = json.dumps({'query': {'filter': ['not', ['Collection', 'description', '=', None]]}})
        json_query = json_query[:-1]
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'JSON decode error: the parameters provided were not valid JSON.'
        return

    @nottest
    def test_search_k_malformed_query(self):
        """Tests SEARCH /collections: malformed query."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['NOT', ['Collection', 'id', '=', 10]]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': [
                              'not',
                              [
                               'Collection', 'title', '=', 'Collection 10'],
                              [
                               'Collection', 'title', '=', 'Collection 10'],
                              [
                               'Collection', 'title', '=', 'Collection 10']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['title'] != 'Collection 10' ]
        assert len(resp) == len(result_set)
        assert 'Collection 10' not in [ c['title'] for c in resp ]
        json_query = json.dumps({'query': {'filter': ['not']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': []}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': ['and']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        assert resp['errors']['IndexError'] == 'list index out of range'
        json_query = json.dumps({'query': {'filter': ['and', ['Collection', 'id', '=', '1099']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'TypeError' in resp['errors']
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': [[], 'a', 'a', 'a']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['TypeError'] == "unhashable type: 'list'"
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'filter': ['Collection', 'id', '=', 2]})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'
        json_query = json.dumps({'query': ['Collection', 'id', '=', 2]})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'

    @nottest
    def test_search_l_lexical_semantic_error(self):
        """Tests POST /collections/search: lexical & semantic errors.

        These are when SQLAQueryBuilder.py raises a OLDSearchParseError because a
        relation is not permitted, e.g., 'contains', or not permitted for a
        given attribute.
        """
        json_query = json.dumps({'query': {'filter': ['Collection', 'title', 'contains', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'Collection.title.contains' in resp['errors']
        json_query = json.dumps({'query': {'filter': ['Collection', 'tags', '=', 'abcdefg']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        json_query = json.dumps({'query': {'filter': ['Collection', 'tags', 'regex', 'xyz']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        assert resp['errors']['Collection.tags.regex'] == 'The relation regex is not permitted for Collection.tags'
        json_query = json.dumps({'query': {'filter': ['Collection', 'tags', 'like', 'abc']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Collection.tags.like'] == 'The relation like is not permitted for Collection.tags'
        json_query = json.dumps({'query': {'filter': ['Collection', 'tags', '__eq__', 'tag']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'InvalidRequestError' in resp['errors']
        return

    @nottest
    def test_search_m_conjunction(self):
        """Tests SEARCH /collections: conjunction."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Collection', 'title', 'like', '%2%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '2' in c['title'] ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Collection', 'title', 'like', '%2%'],
                               [
                                'Collection', 'title', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '2' in c['title'] and '1' in c['title'] ]
        assert len(resp) == len(result_set)
        assert sorted([ c['title'] for c in resp ]) == sorted([ c['title'] for c in result_set ])
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'elicitor', '=', None],
                               [
                                'Collection', 'speaker', '!=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '1' in c['title'] and c['elicitor'] is None and c['speaker'] is not None
                     ]
        assert resp
        assert len(resp) == len(result_set)
        assert sorted([ c['title'] for c in resp ]) == sorted([ c['title'] for c in result_set ])
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'title', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '1' in c['title'] ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_n_disjunction(self):
        """Tests POST /collections/search: disjunction."""
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'Collection', 'title', 'like', '%2%']]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '2' in c['title'] ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'Collection', 'title', 'like', '%2%'],
                               [
                                'Collection', 'title', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '2' in c['title'] or '1' in c['title'] ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'Collection', 'title', 'like', '%2%'],
                               [
                                'Collection', 'title', 'like', '%1%'],
                               [
                                'Collection', 'elicitor', 'id', '=', contributor.id]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '2' in c['title'] or '1' in c['title'] or c['elicitor'] and c['elicitor']['id'] == contributor.id
                     ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_o_int(self):
        """Tests SEARCH /collections: integer searches."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        collection_ids = [ c['id'] for c in collections ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', '=', collection_ids[1]]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['id'] == collection_ids[1]
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', '<', str(collection_ids[16])]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['id'] < collection_ids[16] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', '>=', collection_ids[9]]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['id'] >= collection_ids[9] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'id', 'in', [collection_ids[1], collection_ids[3], collection_ids[8], collection_ids[19]]]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 4
        assert sorted([ c['id'] for c in resp ]) == [collection_ids[1], collection_ids[3], collection_ids[8], collection_ids[19]]
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', 'in', None]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Collection.id.in_'] == 'Invalid filter expression: Collection.id.in_(None)'
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', 'in', 2]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Collection.id.in_'] == 'Invalid filter expression: Collection.id.in_(2)'
        str_patt = '[12][12]'
        patt = re.compile(str_patt)
        expected_id_matches = [ c['id'] for c in collections if patt.search(str(c['id'])) ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', 'regex', str_patt]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_id_matches)
        assert sorted([ c['id'] for c in resp ]) == sorted(expected_id_matches)
        json_query = json.dumps({'query': {'filter': ['Collection', 'id', 'like', '%2%']}})
        expected_matches = [ i for i in collection_ids if '2' in str(i) ]
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_matches)
        return

    @nottest
    def test_search_p_date(self):
        """Tests POST /collections/search: date searches."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '=', jan1.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if isofy(c['date_elicited']) == jan1.isoformat() ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '=', jan3.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if isofy(c['date_elicited']) == jan3.isoformat() ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '!=', jan1.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if isofy(c['date_elicited']) is not None and isofy(c['date_elicited']) != jan1.isoformat()
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '!=', jan3.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if isofy(c['date_elicited']) is not None and isofy(c['date_elicited']) != jan3.isoformat()
                     ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [['Collection', 'date_elicited', '!=', jan1.isoformat()],
                               [
                                'Collection', 'date_elicited', '=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if isofy(c['date_elicited']) != jan1.isoformat() ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '<', jan1.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'] < jan1 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '<', jan3.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'] < jan3 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '<=', jan3.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'] <= jan3 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '>', jan1.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'] > jan2 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '>', '0001-01-01']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and isofy(c['date_elicited']) > '0001-01-01'
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '>=', jan1.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'] >= jan1 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '=', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '__ne__', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_q_date_invalid(self):
        """Tests SEARCH /collections: invalid date searches."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '=', '12-01-01']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 12-01-01'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', '=', '2012-01-32']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 2012-01-32'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', 'regex', '01']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 01'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', 'regex', '2012-01-01']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'].isoformat() == '2012-01-01'
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', 'like', '2012-01-01']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', 'in', '2012-01-02']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Collection.date_elicited.in_'] == 'Invalid filter expression: Collection.date_elicited.in_(datetime.date(2012, 1, 2))'
        json_query = json.dumps({'query': {'filter': ['Collection', 'date_elicited', 'in', ['2012-01-01', '2012-01-03']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['date_elicited'] is not None and c['date_elicited'].isoformat() in ('2012-01-01',
                                                                                                                       '2012-01-03')
                     ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_r_datetime(self):
        """Tests POST /collections/search: datetime searches."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '=', today_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] == today_timestamp ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '=', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] == yesterday_timestamp ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '!=', today_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] != today_timestamp ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '!=', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] != yesterday_timestamp ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [['Collection', 'datetime_entered', '!=', today_timestamp.isoformat()],
                               [
                                'Collection', 'datetime_entered', '=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is None or c['datetime_entered'] != today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '<', today_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] < today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '<=', today_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] <= today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '>', today_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] > today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '>', '1901-01-01T09:08:07']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'].isoformat() > '1901-01-01T09:08:07'
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '>=', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] >= yesterday_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '=', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_entered', '__ne__', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None ]
        assert len(resp) == len(result_set)
        midnight_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        midnight_tomorrow = midnight_today + day_delta
        query = {'query': {'filter': [
                              'and',
                              [['Collection', 'datetime_entered', '>', midnight_today.isoformat()],
                               [
                                'Collection', 'datetime_entered', '<', midnight_tomorrow.isoformat()]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] > midnight_today and c['datetime_entered'] < midnight_tomorrow
                     ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_s_datetime_invalid(self):
        """Tests SEARCH /collections: invalid datetime searches."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_modified', '=', '12-01-01T09']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 12-01-01T09'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_modified', '=', '2012-01-30T09:08:61']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 2012-01-30T09:08:61'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'datetime_modified', '=', '2012-01-30T09:08:59.123456789123456789123456789']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'datetime_modified', '=', '2012-01-30T09:08:59.']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        json_query = json.dumps({'query': {'filter': ['Collection', 'datetime_modified', 'regex', '01']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 01'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'datetime_entered', 'regex', today_timestamp.isoformat()]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] == today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'datetime_modified', 'like', today_timestamp.isoformat()]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_entered'] is not None and c['datetime_entered'] == today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'datetime_modified', 'in', today_timestamp.isoformat()]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Collection.datetime_modified.in_'].startswith('Invalid filter expression: Collection.datetime_modified.in_')
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'datetime_modified', 'in',
                              [
                               today_timestamp.isoformat(), yesterday_timestamp.isoformat()]]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['datetime_modified'] is not None and c['datetime_modified'] in (today_timestamp, yesterday_timestamp)
                     ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_t_many_to_one(self):
        """Tests POST /collections/search: searches on many-to-one attributes."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        test_models = self._get_test_models()
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        json_query = json.dumps({'query': {'filter': ['Collection', 'enterer', 'id', '=', contributor.id]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['enterer']['id'] == contributor.id ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'speaker', 'id', '=', test_models['speakers'][0]['id']]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['speaker'] and c['speaker']['id'] == test_models['speakers'][0]['id']
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'speaker', 'id', 'in', [ s['id'] for s in test_models['speakers'] ]]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['speaker'] and c['speaker']['id'] in [ s['id'] for s in test_models['speakers'] ]
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'speaker', 'id', '<', 15]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['speaker'] and c['speaker']['id'] < 15
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'speaker', 'id', 'regex', '5']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['speaker'] and '5' in str(c['speaker']['id'])
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'speaker', 'id', 'regex', '[56]']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['speaker'] and re.search('[56]', str(c['speaker']['id']))
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'speaker', 'id', 'like', '%5%']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['speaker'] and '5' in str(c['speaker']['id'])
                     ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_v_many_to_many(self):
        """Tests POST /collections/search: searches on many-to-many attributes, i.e., Tag, Form, File."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': ['Tag', 'name', '=', 'name 6']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if 'name 6' in [ t['name'] for t in c['tags'] ] ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%transcription 6%']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if 'transcription 6' in ('').join([ fo['transcription'] for fo in c['forms'] ])
                     ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'like', '%name 9%']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if 'name 6' in ('').join([ fi['name'] for fi in c['files'] ])
                     ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', 'transcription [12]']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if re.search('transcription [12]', ('').join([ fo['transcription'] for fo in c['forms'] ]))
                     ]
        assert resp
        assert len(resp) == len(result_set)
        names = [
         'name 17', 'name 19', 'name 9']
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', 'in_', names]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if set(names) & set([ t['name'] for t in c['tags'] ]) ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', '<', 'name 2']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if [ t for t in c['tags'] if t['name'] < 'name 2' ] ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_entered', '>', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if [ fo for fo in c['forms'] if fo['datetime_entered'] > yesterday_timestamp ] ]
        assert resp
        assert len(resp) == len(result_set)
        files = Session.query(model.File).all()
        files = dict([ (f.id, f) for f in files ])
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', '>', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if [ fi for fi in c['files'] if files[fi['id']].datetime_entered > yesterday_timestamp ] ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'tags', '=', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if not c['tags'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'forms', '!=', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['forms'] ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['Collection', 'tags', 'like', None]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp
        assert resp['errors']['Collection.tags.like'] == 'The relation like is not permitted for Collection.tags'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'forms', '=', 'form 2']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        return

    @nottest
    def test_search_w_in(self):
        """Tests SEARCH /collections: searches using the in_ relation."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'in', ['collection 1', 'Collection 11']]}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if c['title'] in ('collection 1', 'Collection 11') ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'in', 'Collection 1']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 0

    @nottest
    def test_search_x_complex(self):
        """Tests POST /collections/search: complex searches."""
        collections = [ c.get_full_dict() for c in h.get_collections() ]
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Tag', 'name', 'like', '%1%'],
                               [
                                'not', ['Collection', 'title', 'regex', '[12][5-7]']],
                               [
                                'or',
                                [
                                 [
                                  'Collection', 'datetime_entered', '>', today_timestamp.isoformat()],
                                 [
                                  'Collection', 'date_elicited', '=', jan1.isoformat()]]]]]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '1' in (' ').join([ t['name'] for t in c['tags'] ]) and not re.search('[12][5-7]', c['title']) and (today_timestamp < c['datetime_entered'] or c['date_elicited'] and jan1 < c['date_elicited'])
                     ]
        assert resp
        assert len(resp) == len(result_set)
        tag_names = [
         'name 2', 'name 4', 'name 8']
        patt = '([13579][02468])|([02468][13579])'
        json_query = json.dumps({'query': {'filter': [
                              'or',
                              [
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Tag', 'name', 'in', tag_names],
                               [
                                'and',
                                [
                                 [
                                  'not', ['Collection', 'title', 'regex', patt]],
                                 [
                                  'Collection', 'date_elicited', '!=', None]]]]]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if '1' in (' ').join([ fo['transcription'] for fo in c['forms'] ]) or set([ t['name'] for t in c['tags'] ]) & set(tag_names) or not re.search(patt, c['title']) and c['date_elicited'] is not None
                     ]
        assert resp
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Collection', 'title', 'like', '%5%'],
                               [
                                'Collection', 'description', 'regex', '.'],
                               [
                                'not', ['Tag', 'name', 'like', '%6%']],
                               [
                                'or',
                                [
                                 [
                                  'Collection', 'datetime_entered', '<', today_timestamp.isoformat()],
                                 [
                                  'not', ['Collection', 'date_elicited', 'in', [jan1.isoformat(), jan3.isoformat()]]],
                                 [
                                  'and',
                                  [
                                   [
                                    'Collection', 'enterer', 'id', 'regex', '[135680]'],
                                   [
                                    'Collection', 'id', '<', 90]]]]],
                               [
                                'not', ['not', ['not', ['Tag', 'name', '=', 'name 7']]]]]]}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        return

    @nottest
    def test_search_y_paginator(self):
        """Tests SEARCH /collections: paginator."""
        collections = json.loads(json.dumps(h.get_collections(), cls=h.JSONOLDEncoder))
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'like', '%C%']}, 
           'paginator': {'page': 2, 'items_per_page': 3}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if 'C' in c['title'] ]
        assert resp['paginator']['count'] == len(result_set)
        assert len(resp['items']) == 3
        assert resp['items'][0]['id'] == result_set[3]['id']
        assert resp['items'][(-1)]['id'] == result_set[5]['id']
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'like', '%C%']}, 
           'paginator': {'page': 0, 'items_per_page': 3}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'like', '%C%']}, 
           'paginator': {'pages': 0, 'items_per_page': 3}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len([ c for c in collections if 'C' in c['title'] ])
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'like', '%C%']}, 
           'paginator': {'page': 2, 'items_per_page': 4, 'count': 750}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['paginator']['count'] == 750
        assert len(resp['items']) == 4
        assert resp['items'][0]['id'] == result_set[4]['id']
        assert resp['items'][(-1)]['id'] == result_set[7]['id']

    @nottest
    def test_search_z_order_by(self):
        """Tests POST /collections/search: order by."""
        collections = json.loads(json.dumps(h.get_collections(), cls=h.JSONOLDEncoder))
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[cC]'], 
                     'order_by': [
                                'Collection', 'title', 'asc']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(collections)
        assert resp[(-1)]['title'] == 'collection 9'
        assert resp[0]['title'] == 'collection 1'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[nN]'], 
                     'order_by': [
                                'Collection', 'title', 'desc']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(collections)
        assert resp[(-1)]['title'] == 'collection 1'
        assert resp[0]['title'] == 'collection 9'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[nN]'], 
                     'order_by': [
                                'Collection', 'title']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(collections)
        assert resp[(-1)]['title'] == 'collection 9'
        assert resp[0]['title'] == 'collection 1'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[nN]'], 
                     'order_by': [
                                'Collection', 'title', 'descending']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(collections)
        assert resp[(-1)]['title'] == 'collection 9'
        assert resp[0]['title'] == 'collection 1'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[nN]'], 
                     'order_by': [
                                'Collection']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[nN]'], 
                     'order_by': [
                                'Collection', 'foo', 'desc']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Collection.foo'] == 'Searching on Collection.foo is not permitted'
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[nN]'], 
                     'order_by': [
                                'Foo', 'id', 'desc']}})
        response = self.app.post(url('/collections/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Foo'] == 'Searching the Collection model by joining on the Foo model is not possible'
        assert resp['errors']['Foo.id'] == 'Searching on Foo.id is not permitted'
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'

    @nottest
    def test_search_za_restricted(self):
        """Tests SEARCH /collections: restricted collections."""
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        collections = h.get_collections()
        collection_count = len(collections)
        for collection in collections:
            if int(collection.title.split(' ')[(-1)]) % 2 == 0:
                collection.tags.append(restricted_tag)

        Session.commit()
        restricted_collections = Session.query(model.Collection).filter(model.Tag.name == 'restricted').outerjoin(model.Collection.tags).all()
        restricted_collection_count = len(restricted_collections)
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[cC]']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == restricted_collection_count
        assert 'restricted' not in [ x['name'] for x in reduce(list.__add__, [ c['tags'] for c in resp ]) ]
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[cC]']}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == collection_count
        assert 'restricted' in [ x['name'] for x in reduce(list.__add__, [ c['tags'] for c in resp ]) ]
        json_query = json.dumps({'query': {'filter': [
                              'Collection', 'title', 'regex', '[cC]']}, 
           'paginator': {'page': 2, 'items_per_page': 3}})
        response = self.app.request(url('collections'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = [ c for c in collections if int(c.title.split(' ')[(-1)]) % 2 != 0
                     ]
        assert resp['paginator']['count'] == restricted_collection_count
        assert len(resp['items']) == 3
        assert resp['items'][0]['id'] == result_set[3].id

    @nottest
    def test_z_cleanup(self):
        """Tests POST /collections/search: clean up the database."""
        h.clear_all_models()
        administrator = h.generate_default_administrator(config=self.config)
        contributor = h.generate_default_contributor(config=self.config)
        viewer = h.generate_default_viewer(config=self.config)
        Session.add_all([administrator, contributor, viewer])
        Session.commit()
        extra_environ = self.extra_environ_admin.copy()
        extra_environ['test.application_settings'] = True
        self.app.get(url('collections'), extra_environ=extra_environ)
        h.clear_directory_of_files(self.files_path)