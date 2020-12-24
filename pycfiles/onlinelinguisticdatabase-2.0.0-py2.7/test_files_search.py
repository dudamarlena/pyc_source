# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_files_search.py
# Compiled at: 2016-09-19 13:27:02
"""This module tests the file search functionality, i.e., requests to SEARCH
/files and POST /files/search.

NOTE: getting the non-standard http SEARCH method to work in the tests required
using the request method of TestController().app and specifying values for the
method, body, headers, and environ kwarg parameters.  WebTest prints a
WSGIWarning when unknown HTTP methods (e.g., SEARCH) are used.  To prevent
this, I altered the global valid_methods tuple of webtest.lint at runtime by
adding a 'SEARCH' method (see _add_SEARCH_to_web_test_valid_methods() below).
"""
import re, os
from base64 import encodestring
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

    def _create_test_models(self, n=20):
        self._add_test_models_to_session('Tag', n, ['name'])
        self._add_test_models_to_session('Speaker', n, ['first_name', 'last_name', 'dialect'])
        self._add_test_models_to_session('Form', n, ['transcription', 'datetime_entered', 'datetime_modified'])
        Session.commit()

    def _add_test_models_to_session(self, model_name, n, attrs):
        for i in range(1, n + 1):
            m = getattr(model, model_name)()
            for attr in attrs:
                if attr in 'datetime_modified, datetime_entered':
                    setattr(m, attr, datetime.now())
                else:
                    setattr(m, attr, '%s %s' % (attr, i))

            Session.add(m)

    def _get_test_models(self):
        default_models = {'tags': [ t.__dict__ for t in h.get_tags() ], 'forms': [ f.__dict__ for f in h.get_forms() ], 'speakers': [ s.__dict__ for s in h.get_speakers() ], 'users': [ u.__dict__ for u in h.get_users() ]}
        return default_models

    def _create_test_data(self, n=20):
        self._create_test_models(n)
        self._create_test_files(n)

    def _create_test_files(self, n=20):
        """Create n files with various properties.  A testing ground for searches!
        """
        test_models = self._get_test_models()
        ids = []
        for i in range(1, n + 1):
            jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
            jpg_base64 = encodestring(open(jpg_file_path).read())
            wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
            wav_base64 = encodestring(open(wav_file_path).read())
            params = self.file_create_params.copy()
            if i < 11:
                params.update({'base64_encoded_file': jpg_base64, 
                   'filename': 'name_%d.jpg' % i, 
                   'name': 'name_%d.jpg' % i, 
                   'tags': [
                          test_models['tags'][(i - 1)]['id']]})
            elif i < 21:
                params.update({'base64_encoded_file': jpg_base64, 
                   'filename': 'Name_%d.jpg' % i, 
                   'date_elicited': '%02d/%02d/%d' % (jan1.month, jan1.day, jan1.year)})
            elif i < 31:
                params.update({'base64_encoded_file': wav_base64, 
                   'filename': 'Name_%d.wav' % i, 
                   'date_elicited': '%02d/%02d/%d' % (jan1.month, jan1.day, jan1.year)})
            elif i < 41:
                params.update({'parent_file': ids[(-10)], 'start': 1, 'end': 2, 'name': 'Name_%d' % i})
            else:
                params.update({'name': 'Name_%d' % i, 'MIME_type': 'video/mpeg', 'url': 'http://vimeo.com/54144270'})
            if i in (36, 37):
                del params['name']
            if i in (13, 15):
                params.update({'date_elicited': '%02d/%02d/%d' % (jan3.month, jan3.day, jan3.year)})
            if i > 5 and i < 16:
                params.update({'forms': [
                           test_models['forms'][(i - 1)]['id']]})
            params = json.dumps(params)
            response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            ids.append(resp['id'])

    n = 50

    def tearDown(self):
        """Vacuous teardown prevents TestController's tearDown from destroying 
        data between test methods."""
        pass

    @nottest
    def test_a_initialize(self):
        """Tests POST /files/search: initialize database."""
        self._create_test_data(self.n)
        self._add_SEARCH_to_web_test_valid_methods()

    @nottest
    def test_search_b_equals(self):
        """Tests POST /files/search: equals."""
        json_query = json.dumps({'query': {'filter': ['File', 'name', '=', 'name_10.jpg']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['name'] == 'name_10.jpg'

    @nottest
    def test_search_c_not_equals(self):
        """Tests SEARCH /files: not equals."""
        json_query = json.dumps({'query': {'filter': ['not', ['File', 'name', '=', 'name_10.jpg']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == self.n - 1
        assert 'name_10.jpg' not in [ f['name'] for f in resp ]

    @nottest
    def test_search_d_like(self):
        """Tests POST /files/search: like."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'like', '%1%']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '1' in f['name'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'like', '%N%']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if 'N' in f['name'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['or',
                              [
                               [
                                'File', 'name', 'like', 'N%'],
                               [
                                'File', 'name', 'like', 'n%']]]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if 'N' in f['name'] or 'n' in f['name'] ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_e_not_like(self):
        """Tests SEARCH /files: not like."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['not', ['File', 'name', 'like', '%1%']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '1' not in f['name'] ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_f_regexp(self):
        """Tests POST /files/search: regular expression."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '[345]2']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if re.search('[345]2', f['name']) ]
        assert sorted([ f['name'] for f in resp ]) == sorted([ f['name'] for f in result_set ])
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '^N']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['name'][0] == 'N' ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '^[Nn]']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['name'][0] in ('N', 'n') ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '^[Nn]ame_1.jpg$']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['name'] in ('Name_1.jpg', 'name_1.jpg') ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '1{1,}']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if re.search('1{1,}', f['name']) ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '[123]{2,}']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if re.search('[123]{2,}', f['name']) ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'regex', '[123]{3,2}']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'

    @nottest
    def test_search_g_not_regexp(self):
        """Tests SEARCH /files: not regular expression."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['not', ['File', 'name', 'regexp', '[345]2']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if not re.search('[345]2', f['name']) ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_h_empty(self):
        """Tests POST /files/search: is NULL."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'description', '=', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['description'] is None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['not', ['File', 'description', '!=', None]]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_i_not_empty(self):
        """Tests SEARCH /files: is not NULL."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['not', ['File', 'description', '=', None]]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['description'] is not None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'description', '!=', None]}})
        response = self.app.request(url('files'), body=json_query, method='SEARCH', headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_j_invalid_json(self):
        """Tests POST /files/search: invalid JSON params."""
        json_query = json.dumps({'query': {'filter': ['not', ['File', 'description', '=', None]]}})
        json_query = json_query[:-1]
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'JSON decode error: the parameters provided were not valid JSON.'
        return

    @nottest
    def test_search_k_malformed_query(self):
        """Tests SEARCH /files: malformed query."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['NOT', ['File', 'id', '=', 10]]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': [
                              'not',
                              [
                               'File', 'name', '=', 'name_10.jpg'],
                              [
                               'File', 'name', '=', 'name_10.jpg'],
                              [
                               'File', 'name', '=', 'name_10.jpg']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['name'] != 'name_10.jpg' ]
        assert len(resp) == len(result_set)
        assert 'name 10' not in [ f['name'] for f in resp ]
        json_query = json.dumps({'query': {'filter': ['not']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': []}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': ['and']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        assert resp['errors']['IndexError'] == 'list index out of range'
        json_query = json.dumps({'query': {'filter': ['and', ['File', 'id', '=', '1099']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'TypeError' in resp['errors']
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': [[], 'a', 'a', 'a']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['TypeError'] == "unhashable type: 'list'"
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'filter': ['File', 'id', '=', 2]})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'
        json_query = json.dumps({'query': ['File', 'id', '=', 2]})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'

    @nottest
    def test_search_l_lexical_semantic_error(self):
        """Tests POST /files/search: lexical & semantic errors.

        These are when SQLAQueryBuilder.py raises a OLDSearchParseError because a
        relation is not permitted, e.g., 'contains', or not permitted for a
        given attribute.
        """
        json_query = json.dumps({'query': {'filter': ['File', 'name', 'contains', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'File.name.contains' in resp['errors']
        json_query = json.dumps({'query': {'filter': ['File', 'tags', '=', 'abcdefg']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        json_query = json.dumps({'query': {'filter': ['File', 'tags', 'regex', 'xyz']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        assert resp['errors']['File.tags.regex'] == 'The relation regex is not permitted for File.tags'
        json_query = json.dumps({'query': {'filter': ['File', 'tags', 'like', 'abc']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.tags.like'] == 'The relation like is not permitted for File.tags'
        json_query = json.dumps({'query': {'filter': ['File', 'tags', '__eq__', 'tag']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'InvalidRequestError' in resp['errors']
        return

    @nottest
    def test_search_m_conjunction(self):
        """Tests SEARCH /files: conjunction."""
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        models = self._get_test_models()
        files = [ f.get_dict() for f in h.get_files() ]
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'File', 'name', 'like', '%2%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '2' in f['name'] ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'File', 'name', 'like', '%2%'],
                               [
                                'File', 'name', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '2' in f['name'] and '1' in f['name'] ]
        assert len(resp) == len(result_set)
        assert sorted([ f['name'] for f in resp ]) == sorted([ f['name'] for f in result_set ])
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'elicitor', 'id', '=', contributor.id],
                               [
                                'File', 'speaker', 'id', '=', models['speakers'][3]['id']]]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '1' in f['name'] and f['elicitor'] and f['elicitor']['id'] == contributor.id and f['speaker'] and f['speaker']['id'] == models['speakers'][3]['id']
                     ]
        assert len(resp) == len(result_set)
        assert sorted([ f['name'] for f in resp ]) == sorted([ f['name'] for f in result_set ])
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'name', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '1' in f['name'] ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_n_disjunction(self):
        """Tests POST /files/search: disjunction."""
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        files = [ f.get_dict() for f in h.get_files() ]
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'File', 'name', 'like', '%2%']]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '2' in f['name'] ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'File', 'name', 'like', '%2%'],
                               [
                                'File', 'name', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '2' in f['name'] or '1' in f['name'] ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'File', 'name', 'like', '%2%'],
                               [
                                'File', 'name', 'like', '%1%'],
                               [
                                'File', 'elicitor', 'id', '=', contributor.id]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '2' in f['name'] or '1' in f['name'] or f['elicitor'] and f['elicitor']['id'] == contributor.id
                     ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_o_int(self):
        """Tests SEARCH /files: integer searches."""
        files = [ f.get_dict() for f in h.get_files() ]
        file_ids = [ f['id'] for f in files ]
        json_query = json.dumps({'query': {'filter': ['File', 'id', '=', file_ids[1]]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['id'] == file_ids[1]
        json_query = json.dumps({'query': {'filter': ['File', 'id', '<', str(file_ids[16])]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['id'] < file_ids[16] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'id', '>=', file_ids[9]]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['id'] >= file_ids[9] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'id', 'in', [file_ids[1], file_ids[3], file_ids[8], file_ids[19]]]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 4
        assert sorted([ f['id'] for f in resp ]) == [file_ids[1], file_ids[3], file_ids[8], file_ids[19]]
        json_query = json.dumps({'query': {'filter': ['File', 'id', 'in', None]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.id.in_'] == 'Invalid filter expression: File.id.in_(None)'
        json_query = json.dumps({'query': {'filter': ['File', 'id', 'in', 2]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.id.in_'] == 'Invalid filter expression: File.id.in_(2)'
        str_patt = '[12][12]'
        patt = re.compile(str_patt)
        expected_id_matches = [ f['id'] for f in files if patt.search(str(f['id'])) ]
        json_query = json.dumps({'query': {'filter': ['File', 'id', 'regex', str_patt]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_id_matches)
        assert sorted([ f['id'] for f in resp ]) == sorted(expected_id_matches)
        json_query = json.dumps({'query': {'filter': ['File', 'id', 'like', '%2%']}})
        expected_matches = [ i for i in file_ids if '2' in str(i) ]
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_matches)
        return

    @nottest
    def test_search_p_date(self):
        """Tests POST /files/search: date searches."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '=', jan1.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if isofy(f['date_elicited']) == jan1.isoformat() ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '=', jan3.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if isofy(f['date_elicited']) == jan3.isoformat() ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '!=', jan1.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if isofy(f['date_elicited']) is not None and isofy(f['date_elicited']) != jan1.isoformat()
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '!=', jan3.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if isofy(f['date_elicited']) is not None and isofy(f['date_elicited']) != jan3.isoformat()
                     ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [['File', 'date_elicited', '!=', jan1.isoformat()],
                               [
                                'File', 'date_elicited', '=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if isofy(f['date_elicited']) != jan1.isoformat() ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '<', jan1.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'] < jan1 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '<', jan3.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'] < jan3 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '<=', jan3.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'] <= jan3 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '>', jan1.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'] > jan2 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '>', '0001-01-01']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and isofy(f['date_elicited']) > '0001-01-01'
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '>=', jan1.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'] >= jan1 ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '=', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '__ne__', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_q_date_invalid(self):
        """Tests SEARCH /files: invalid date searches."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '=', '12-01-01']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 12-01-01'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', '=', '2012-01-32']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 2012-01-32'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', 'regex', '01']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 01'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', 'regex', '2012-01-01']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'].isoformat() == '2012-01-01'
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', 'like', '2012-01-01']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', 'in', '2012-01-02']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.date_elicited.in_'] == 'Invalid filter expression: File.date_elicited.in_(datetime.date(2012, 1, 2))'
        json_query = json.dumps({'query': {'filter': ['File', 'date_elicited', 'in', ['2012-01-01', '2012-01-03']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['date_elicited'] is not None and f['date_elicited'].isoformat() in ('2012-01-01',
                                                                                                                 '2012-01-03')
                     ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_r_datetime(self):
        """Tests POST /files/search: datetime searches."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '=', today_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] == today_timestamp ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '=', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] == yesterday_timestamp ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '!=', today_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] != today_timestamp ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '!=', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] != yesterday_timestamp ]
        assert len(resp) == len(result_set)
        query = {'query': {'filter': [
                              'or',
                              [['File', 'datetime_entered', '!=', today_timestamp.isoformat()],
                               [
                                'File', 'datetime_entered', '=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is None or f['datetime_entered'] != today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '<', today_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] < today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '<=', today_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] <= today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '>', today_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] > today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '>', '1901-01-01T09:08:07']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'].isoformat() > '1901-01-01T09:08:07'
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '>=', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] >= yesterday_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '=', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is None ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_entered', '__ne__', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None ]
        assert len(resp) == len(result_set)
        midnight_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        midnight_tomorrow = midnight_today + day_delta
        query = {'query': {'filter': [
                              'and',
                              [['File', 'datetime_entered', '>', midnight_today.isoformat()],
                               [
                                'File', 'datetime_entered', '<', midnight_tomorrow.isoformat()]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] > midnight_today and f['datetime_entered'] < midnight_tomorrow
                     ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_s_datetime_invalid(self):
        """Tests SEARCH /files: invalid datetime searches."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_modified', '=', '12-01-01T09']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 12-01-01T09'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_modified', '=', '2012-01-30T09:08:61']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 2012-01-30T09:08:61'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', '=', '2012-01-30T09:08:59.123456789123456789123456789']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', '=', '2012-01-30T09:08:59.']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        json_query = json.dumps({'query': {'filter': ['File', 'datetime_modified', 'regex', '01']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 01'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_entered', 'regex', today_timestamp.isoformat()]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] == today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', 'like', today_timestamp.isoformat()]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_entered'] is not None and f['datetime_entered'] == today_timestamp
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', 'in', today_timestamp.isoformat()]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.datetime_modified.in_'].startswith('Invalid filter expression: File.datetime_modified.in_')
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', 'in',
                              [
                               today_timestamp.isoformat(), yesterday_timestamp.isoformat()]]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['datetime_modified'] is not None and f['datetime_modified'] in (today_timestamp, yesterday_timestamp)
                     ]
        assert len(resp) == len(result_set)
        return

    @nottest
    def test_search_t_many_to_one(self):
        """Tests POST /files/search: searches on many-to-one attributes."""
        files = [ f.get_dict() for f in h.get_files() ]
        test_models = self._get_test_models()
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        json_query = json.dumps({'query': {'filter': ['File', 'enterer', 'id', '=', contributor.id]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['enterer']['id'] == contributor.id ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'speaker', 'id', '=', test_models['speakers'][0]['id']]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['speaker'] and f['speaker']['id'] == test_models['speakers'][0]['id']
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'speaker', 'id', 'in', [ s['id'] for s in test_models['speakers'] ]]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['speaker'] and f['speaker']['id'] in [ s['id'] for s in test_models['speakers'] ]
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'speaker', 'id', '<', 15]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['speaker'] and f['speaker']['id'] < 15
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'speaker', 'id', 'regex', '5']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['speaker'] and '5' in str(f['speaker']['id'])
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'speaker', 'id', 'regex', '[56]']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['speaker'] and re.search('[56]', str(f['speaker']['id']))
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'speaker', 'id', 'like', '%5%']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['speaker'] and '5' in str(f['speaker']['id'])
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'parent_file', 'filename', 'regex', '[13579]']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['parent_file'] and set(list('13579')) & set(list(f['parent_file']['filename']))
                     ]
        assert len(resp) == len(result_set)

    @nottest
    def test_search_v_many_to_many(self):
        """Tests POST /files/search: searches on many-to-many attributes, i.e., Tag, Form."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': ['Tag', 'name', '=', 'name_6.jpg']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if 'name_6.jpg' in [ t['name'] for t in f['tags'] ] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'tags', 'name', '=', 'name_6.jpg']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%transcription 6%']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if 'transcription 6' in ('').join([ fo['transcription'] for fo in f['forms'] ])
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', 'transcription [12]']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if re.search('transcription [12]', ('').join([ fo['transcription'] for fo in f['forms'] ]))
                     ]
        assert len(resp) == len(result_set)
        names = [
         'name 77', 'name 79', 'name 99']
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', 'in_', names]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if set(names) & set([ t['name'] for t in f['tags'] ]) ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', '<', 'name 2']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if [ t for t in f['tags'] if t['name'] < 'name 2' ] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_entered', '>', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if [ fo for fo in f['forms'] if fo['datetime_entered'] > yesterday_timestamp ] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_entered', '<', yesterday_timestamp.isoformat()]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if [ fo for fo in f['forms'] if fo['datetime_entered'] < yesterday_timestamp ] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'tags', '=', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if not f['tags'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'forms', '!=', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['forms'] ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': ['File', 'tags', 'like', None]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.tags.like'] == 'The relation like is not permitted for File.tags'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'forms', '=', 'form 2']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        return

    @nottest
    def test_search_w_in(self):
        """Tests SEARCH /files: searches using the in_ relation."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'in', ['name_1.jpg']]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if f['name'] in ('name_1.jpg', ) ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'in', 'name_1.jpg']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 0

    @nottest
    def test_search_x_complex(self):
        """Tests POST /files/search: complex searches."""
        files = [ f.get_dict() for f in h.get_files() ]
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Tag', 'name', 'like', '%1%'],
                               [
                                'not', ['File', 'name', 'regex', '[12][5-7]']],
                               [
                                'or',
                                [
                                 [
                                  'File', 'datetime_entered', '>', today_timestamp.isoformat()],
                                 [
                                  'File', 'date_elicited', '>', jan1.isoformat()]]]]]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '1' in (' ').join([ t['name'] for t in f['tags'] ]) and not re.search('[12][5-7]', f['name']) and (today_timestamp < f['datetime_entered'] or f['date_elicited'] and jan1 < f['date_elicited'])
                     ]
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
                                  'not', ['File', 'name', 'regex', patt]],
                                 [
                                  'File', 'date_elicited', '!=', None]]]]]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if '1' in (' ').join([ fo['transcription'] for fo in f['forms'] ]) or set([ t['name'] for t in f['tags'] ]) & set(tag_names) or not re.search(patt, f['name']) and f['date_elicited'] is not None
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'File', 'name', 'like', '%5%'],
                               [
                                'File', 'description', 'regex', '.'],
                               [
                                'not', ['Tag', 'name', 'like', '%6%']],
                               [
                                'or',
                                [
                                 [
                                  'File', 'datetime_entered', '<', today_timestamp.isoformat()],
                                 [
                                  'not', ['File', 'date_elicited', 'in', [jan1.isoformat(), jan3.isoformat()]]],
                                 [
                                  'and',
                                  [
                                   [
                                    'File', 'enterer', 'id', 'regex', '[135680]'],
                                   [
                                    'File', 'id', '<', 90]]]]],
                               [
                                'not', ['not', ['not', ['Tag', 'name', '=', 'name 7']]]]]]}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        return

    @nottest
    def test_search_y_paginator(self):
        """Tests SEARCH /files: paginator."""
        files = json.loads(json.dumps(h.get_files(), cls=h.JSONOLDEncoder))
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'like', '%N%']}, 
           'paginator': {'page': 2, 'items_per_page': 3}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in files if 'N' in f['name'] ]
        assert resp['paginator']['count'] == len(result_set)
        assert len(resp['items']) == 3
        assert resp['items'][0]['id'] == result_set[3]['id']
        assert resp['items'][(-1)]['id'] == result_set[5]['id']
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'like', '%N%']}, 
           'paginator': {'page': 0, 'items_per_page': 3}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'like', '%N%']}, 
           'paginator': {'pages': 0, 'items_per_page': 3}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len([ f for f in files if 'N' in f['name'] ])
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'like', '%N%']}, 
           'paginator': {'page': 2, 'items_per_page': 4, 'count': 750}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['paginator']['count'] == 750
        assert len(resp['items']) == 4
        assert resp['items'][0]['id'] == result_set[4]['id']
        assert resp['items'][(-1)]['id'] == result_set[7]['id']

    @nottest
    def test_search_z_order_by(self):
        """Tests POST /files/search: order by."""
        files = json.loads(json.dumps(h.get_files(), cls=h.JSONOLDEncoder))
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'File', 'name', 'asc']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(files)
        assert resp[(-1)]['name'] == 'name_9.jpg'
        assert resp[0]['name'] == 'name_1.jpg'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'File', 'name', 'desc']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(files)
        assert resp[(-1)]['name'] == 'name_1.jpg'
        assert resp[0]['name'] == 'name_9.jpg'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'File', 'name']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(files)
        assert resp[(-1)]['name'] == 'name_9.jpg'
        assert resp[0]['name'] == 'name_1.jpg'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'File', 'name', 'descending']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(files)
        assert resp[(-1)]['name'] == 'name_9.jpg'
        assert resp[0]['name'] == 'name_1.jpg'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'File']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'File', 'foo', 'desc']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['File.foo'] == 'Searching on File.foo is not permitted'
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]'], 
                     'order_by': [
                                'Foo', 'id', 'desc']}})
        response = self.app.post(url('/files/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Foo'] == 'Searching the File model by joining on the Foo model is not possible'
        assert resp['errors']['Foo.id'] == 'Searching on Foo.id is not permitted'
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'

    @nottest
    def test_search_za_restricted(self):
        """Tests SEARCH /files: restricted files."""
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        files = h.get_files()
        file_count = len(files)
        for file in files:
            if int(file.name.split('_')[(-1)].split('.')[0]) % 2 == 0:
                file.tags.append(restricted_tag)

        Session.commit()
        restricted_files = Session.query(model.File).filter(model.Tag.name == 'restricted').outerjoin(model.File.tags).all()
        restricted_file_count = len(restricted_files)
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == restricted_file_count
        assert 'restricted' not in [ x['name'] for x in reduce(list.__add__, [ f['tags'] for f in resp ]) ]
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]']}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == file_count
        assert 'restricted' in [ x['name'] for x in reduce(list.__add__, [ f['tags'] for f in resp ]) ]
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', '[nN]']}, 
           'paginator': {'page': 2, 'items_per_page': 3}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = [ f for f in files if int(f.name.split('_')[(-1)].split('.')[0]) % 2 != 0
                     ]
        assert resp['paginator']['count'] == restricted_file_count
        assert len(resp['items']) == 3
        assert resp['items'][0]['id'] == result_set[3].id

    @nottest
    def test_search_zb_file_type(self):
        """Tests SEARCH /files: get the different types of files."""
        json_query = json.dumps({'query': {'filter': ['File', 'filename', '!=', None]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 30
        json_query = json.dumps({'query': {'filter': ['File', 'parent_file', '!=', None]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 10
        json_query = json.dumps({'query': {'filter': ['File', 'url', '!=', None]}})
        response = self.app.request(url('files'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 10
        return

    @nottest
    def test_z_cleanup(self):
        """Tests POST /files/search: clean up the database."""
        h.clear_all_models()
        administrator = h.generate_default_administrator()
        contributor = h.generate_default_contributor()
        viewer = h.generate_default_viewer()
        Session.add_all([administrator, contributor, viewer])
        Session.commit()
        extra_environ = self.extra_environ_admin.copy()
        extra_environ['test.application_settings'] = True
        self.app.get(url('files'), extra_environ=extra_environ)
        h.clear_directory_of_files(self.files_path)
        h.clear_directory_of_files(self.reduced_files_path)