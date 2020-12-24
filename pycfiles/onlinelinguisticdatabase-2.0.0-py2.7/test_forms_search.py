# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_forms_search.py
# Compiled at: 2016-09-19 13:27:02
"""This module tests the form search functionality, i.e., requests to SEARCH
/forms and POST /forms/search.

NOTE: getting the non-standard http SEARCH method to work in the tests required
using the request method of TestController().app and specifying values for the
method, body, headers, and environ kwarg parameters.  WebTest prints a
WSGIWarning when unknown HTTP methods (e.g., SEARCH) are used.  To prevent this,
I altered the global valid_methods tuple of webtest.lint at runtime by adding a
'SEARCH' method (see _add_SEARCH_to_web_test_valid_methods() below).
"""
import re, platform
from onlinelinguisticdatabase.tests import TestController, url
from nose.tools import nottest
import simplejson as json, logging
from datetime import date, datetime, timedelta
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session, Model
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)
today_timestamp = datetime.now()
day_delta = timedelta(1)
yesterday_timestamp = today_timestamp - day_delta
jan1 = date(2012, 1, 1)
jan2 = date(2012, 1, 2)
jan3 = date(2012, 1, 3)
jan4 = date(2012, 1, 4)
mysql_engine = Model.__table_args__.get('mysql_engine')

def get_timestamp_isoformat(timestamp):
    """Return the timestamp in ISO 8601 format, but also in the form that
    datetimes are stored in in the database. At present, this function is
    sensitive to the RDBMS and the MySQL engine type. It may also need to be
    made sensitive to the platform (i.e., Linux, vs. Mac, vs. Windows).

    """
    RDBMSName = h.get_RDBMS_name(config_filename='test.ini')
    mysql_engine = Model.__table_args__.get('mysql_engine')
    system = platform.system()
    if RDBMSName == 'mysql':
        if mysql_engine == 'InnoDB' or system == 'Darwin':
            return h.round_datetime(timestamp).isoformat()
        else:
            return timestamp.isoformat().split('.')[0]

    else:
        return timestamp.isoformat()


today_timestamp_iso = get_timestamp_isoformat(today_timestamp)
yesterday_timestamp_iso = get_timestamp_isoformat(yesterday_timestamp)

def _create_test_models(n=100):
    _add_test_models_to_session('Tag', n, ['name'])
    _add_test_models_to_session('Speaker', n, ['first_name', 'last_name', 'dialect'])
    _add_test_models_to_session('Source', n, ['author_first_name', 'author_last_name',
     'title'])
    _add_test_models_to_session('ElicitationMethod', n, ['name'])
    _add_test_models_to_session('SyntacticCategory', n, ['name'])
    _add_test_models_to_session('File', n, ['name'])
    Session.commit()


def _add_test_models_to_session(model_name, n, attrs):
    for i in range(1, n + 1):
        m = getattr(model, model_name)()
        for attr in attrs:
            setattr(m, attr, '%s %s' % (attr, i))

        Session.add(m)


def _get_test_models():
    default_models = {'tags': h.get_tags(), 
       'speakers': h.get_speakers(), 
       'sources': h.get_sources(), 
       'elicitation_methods': h.get_elicitation_methods(), 
       'syntactic_categories': h.get_syntactic_categories(), 
       'files': h.get_files()}
    return default_models


def _create_test_forms(n=100):
    """Create n forms with various properties.  A testing ground for searches!
    """
    test_models = _get_test_models()
    users = h.get_users()
    viewer = [ u for u in users if u.role == 'viewer' ][0]
    contributor = [ u for u in users if u.role == 'contributor' ][0]
    administrator = [ u for u in users if u.role == 'administrator' ][0]
    for i in range(1, n + 1):
        f = model.Form()
        f.transcription = 'transcription %d' % i
        if i > 50:
            f.transcription = f.transcription.upper()
            administrator.remembered_forms.append(f)
        f.morpheme_break = 'morpheme_break %d' % i
        f.morpheme_gloss = 'morpheme_gloss %d' % i
        f.comments = 'comments %d' % i
        f.speaker_comments = 'speaker_comments %d' % i
        f.morpheme_break_ids = '[[[]]]'
        f.morpheme_gloss_ids = '[[[]]]'
        tl = model.Translation()
        tl.transcription = 'translation %d' % i
        f.enterer = contributor
        f.syntactic_category = test_models['syntactic_categories'][(i - 1)]
        if i > 75:
            f.phonetic_transcription = 'phonetic_transcription %d' % i
            f.narrow_phonetic_transcription = 'narrow_phonetic_transcription %d' % i
            t = test_models['tags'][(i - 1)]
            f.tags.append(t)
            tl.grammaticality = '*'
            viewer.remembered_forms.append(f)
        if i > 65 and i < 86:
            fi = test_models['files'][(i - 1)]
            f.files.append(fi)
            contributor.remembered_forms.append(f)
        if i > 50:
            f.elicitor = contributor
            if i != 100:
                f.speaker = test_models['speakers'][0]
                f.datetime_modified = today_timestamp
                f.datetime_entered = today_timestamp
        else:
            f.elicitor = administrator
            f.speaker = test_models['speakers'][(-1)]
            f.datetime_modified = yesterday_timestamp
            f.datetime_entered = yesterday_timestamp
        if i < 26:
            f.elicitation_method = test_models['elicitation_methods'][0]
            f.date_elicited = jan1
        elif i < 51:
            f.elicitation_method = test_models['elicitation_methods'][24]
            f.date_elicited = jan2
        elif i < 76:
            f.elicitation_method = test_models['elicitation_methods'][49]
            f.date_elicited = jan3
        else:
            f.elicitation_method = test_models['elicitation_methods'][74]
            if i < 99:
                f.date_elicited = jan4
        if i > 41 and i < 53 or i in (86, 92, 3):
            f.source = test_models['sources'][i]
        if i != 87:
            f.translations.append(tl)
        if i == 79:
            tl = model.Translation()
            tl.transcription = 'translation %d the second' % i
            f.translations.append(tl)
            t = test_models['tags'][(i - 2)]
            f.tags.append(t)
        Session.add(f)

    Session.commit()


def _create_test_data(n=100):
    _create_test_models(n)
    _create_test_forms(n)


class TestFormsSearchController(TestController):
    n = 100

    def tearDown(self):
        pass

    @nottest
    def test_a_initialize(self):
        """Tests POST /forms/search: initialize database."""
        _create_test_data(self.n)
        self._add_SEARCH_to_web_test_valid_methods()

    @nottest
    def test_search_b_equals(self):
        """Tests POST /forms/search: equals."""
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', '=', 'transcription 10']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['transcription'] == 'transcription 10'
        assert response.content_type == 'application/json'

    @nottest
    def test_search_c_not_equals(self):
        """Tests SEARCH /forms: not equals."""
        json_query = json.dumps({'query': {'filter': ['not', ['Form', 'transcription', '=', 'transcription 10']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == self.n - 1
        assert 'transcription 10' not in [ f['transcription'] for f in resp ]

    @nottest
    def test_search_d_like(self):
        """Tests POST /forms/search: like."""
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'like', '%1%']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 20
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'like', '%T%']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50
        json_query = json.dumps({'query': {'filter': ['or',
                              [
                               [
                                'Form', 'transcription', 'like', 'T%'],
                               [
                                'Form', 'transcription', 'like', 't%']]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'like', 'T_A%']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50

    @nottest
    def test_search_e_not_like(self):
        """Tests SEARCH /forms: not like."""
        json_query = json.dumps({'query': {'filter': ['not', ['Form', 'transcription', 'like', '%1%']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 80

    @nottest
    def test_search_f_regexp(self):
        """Tests POST /forms/search: regular expression."""
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '[345]2']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert sorted([ f['transcription'] for f in resp ]) == [
         'TRANSCRIPTION 52', 'transcription 32', 'transcription 42']
        assert len(resp) == 3
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '^T']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '^[Tt]']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '^[Tt]ranscription 1.$']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 10
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '2{2,}']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '[123]{2,}']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 9
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '[123]{3,2}']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'

    @nottest
    def test_search_g_not_regexp(self):
        """Tests SEARCH /forms: not regular expression."""
        json_query = json.dumps({'query': {'filter': ['not', ['Form', 'transcription', 'regexp', '[345]2']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 97

    @nottest
    def test_search_h_empty(self):
        """Tests POST /forms/search: is NULL."""
        json_query = json.dumps({'query': {'filter': ['Form', 'narrow_phonetic_transcription', '=', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 75
        json_query = json.dumps({'query': {'filter': ['not', ['Form', 'narrow_phonetic_transcription', '!=', None]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 75
        return

    @nottest
    def test_search_i_not_empty(self):
        """Tests SEARCH /forms: is not NULL."""
        json_query = json.dumps({'query': {'filter': ['not', ['Form', 'narrow_phonetic_transcription', '=', None]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 25
        json_query = json.dumps({'query': {'filter': ['Form', 'narrow_phonetic_transcription', '!=', None]}})
        response = self.app.request(url('forms'), body=json_query, method='SEARCH', headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 25
        return

    @nottest
    def test_search_j_invalid_json(self):
        """Tests POST /forms/search: invalid JSON params."""
        json_query = json.dumps({'query': {'filter': ['not', ['Form', 'narrow_phonetic_transcription', '=', None]]}})
        json_query = json_query[:-1]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'JSON decode error: the parameters provided were not valid JSON.'
        return

    @nottest
    def test_search_k_malformed_query(self):
        """Tests SEARCH /forms: malformed query."""
        json_query = json.dumps({'query': {'filter': ['NOT', ['Form', 'id', '=', 10]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': [
                              'not',
                              [
                               'Form', 'transcription', '=', 'transcription 10'],
                              [
                               'Form', 'transcription', '=', 'transcription 10'],
                              [
                               'Form', 'transcription', '=', 'transcription 10']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        assert 'transcription 10' not in [ f['transcription'] for f in resp ]
        json_query = json.dumps({'query': {'filter': ['not']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': []}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': ['and']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        assert resp['errors']['IndexError'] == 'list index out of range'
        json_query = json.dumps({'query': {'filter': ['and', ['Form', 'id', '=', '1099']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'TypeError' in resp['errors']
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'query': {'filter': [[], 'a', 'a', 'a']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['TypeError'] == "unhashable type: 'list'"
        assert resp['errors']['Malformed OLD query error'] == 'The submitted query was malformed'
        json_query = json.dumps({'filter': ['Form', 'id', '=', 2]})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'
        json_query = json.dumps({'query': ['Form', 'id', '=', 2]})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The specified search parameters generated an invalid database query'

    @nottest
    def test_search_l_lexical_semantic_error(self):
        """Tests POST /forms/search: lexical & semantic errors.

        These are when SQLAQueryBuilder.py raises a OLDSearchParseError because a
        relation is not permitted, e.g., 'contains', or not permitted for a
        given attribute.
        """
        json_query = json.dumps({'query': {'filter': ['Form', 'transcription', 'contains', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'Form.transcription.contains' in resp['errors']
        json_query = json.dumps({'query': {'filter': ['Form', 'translations', '=', 'abcdefg']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        json_query = json.dumps({'query': {'filter': ['Form', 'tags', 'regex', 'xyz']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.tags.regex'] == 'The relation regex is not permitted for Form.tags'
        json_query = json.dumps({'query': {'filter': ['Form', 'translations', 'like', 'abc']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.translations.like'] == 'The relation like is not permitted for Form.translations'
        json_query = json.dumps({'query': {'filter': ['Form', 'tags', '__eq__', 'tag']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'InvalidRequestError' in resp['errors']
        return

    @nottest
    def test_search_m_conjunction(self):
        """Tests SEARCH /forms: conjunction."""
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        models = _get_test_models()
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Form', 'transcription', 'like', '%2%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 19
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Form', 'transcription', 'like', '%2%'],
                               [
                                'Form', 'transcription', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert sorted([ f['transcription'] for f in resp ]) == ['transcription 12', 'transcription 21']
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'elicitor', 'id', '=', contributor.id],
                               [
                                'Form', 'elicitation_method', 'id', '=', models['elicitation_methods'][49].id]]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 3
        assert sorted([ f['transcription'] for f in resp ]) == [
         'TRANSCRIPTION 51', 'TRANSCRIPTION 61', 'TRANSCRIPTION 71']
        query = {'query': {'filter': [
                              'and',
                              [
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'transcription', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 20

    @nottest
    def test_search_n_disjunction(self):
        """Tests POST /forms/search: disjunction."""
        users = h.get_users()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'Form', 'transcription', 'like', '%2%']]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 19
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'Form', 'transcription', 'like', '%2%'],
                               [
                                'Form', 'transcription', 'like', '%1%']]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 37
        query = {'query': {'filter': [
                              'or',
                              [
                               [
                                'Form', 'transcription', 'like', '%2%'],
                               [
                                'Form', 'transcription', 'like', '%1%'],
                               [
                                'Form', 'elicitor', 'id', '=', contributor.id]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 76
        assert response.content_type == 'application/json'

    @nottest
    def test_search_o_int(self):
        """Tests SEARCH /forms: integer searches."""
        forms = h.get_forms()
        form_ids = [ f.id for f in forms ]
        json_query = json.dumps({'query': {'filter': ['Form', 'id', '=', form_ids[1]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['id'] == form_ids[1]
        json_query = json.dumps({'query': {'filter': ['Form', 'id', '<', str(form_ids[16])]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 16
        json_query = json.dumps({'query': {'filter': ['Form', 'id', '>=', form_ids[97]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 3
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'id', 'in', [form_ids[12], form_ids[36], form_ids[28], form_ids[94]]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 4
        assert sorted([ f['id'] for f in resp ]) == [form_ids[12], form_ids[28], form_ids[36], form_ids[94]]
        json_query = json.dumps({'query': {'filter': ['Form', 'id', 'in', None]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.id.in_'] == 'Invalid filter expression: Form.id.in_(None)'
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': ['Form', 'id', 'in', 2]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.id.in_'] == 'Invalid filter expression: Form.id.in_(2)'
        assert response.content_type == 'application/json'
        str_patt = '[13][58]'
        patt = re.compile(str_patt)
        expected_id_matches = [ f.id for f in forms if patt.search(str(f.id)) ]
        json_query = json.dumps({'query': {'filter': ['Form', 'id', 'regex', '[13][58]']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_id_matches)
        assert sorted([ f['id'] for f in resp ]) == sorted(expected_id_matches)
        json_query = json.dumps({'query': {'filter': ['Form', 'id', 'like', '%2%']}})
        expected_matches = [ i for i in form_ids if '2' in str(i) ]
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_matches)
        return

    @nottest
    def test_search_p_date(self):
        """Tests POST /forms/search: date searches."""
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '=', jan1.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 25
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '=', jan4.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 23
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '!=', jan1.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 73
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '!=', jan4.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 75
        query = {'query': {'filter': [
                              'or',
                              [['Form', 'date_elicited', '!=', jan1.isoformat()],
                               [
                                'Form', 'date_elicited', '=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 75
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '<', jan1.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 0
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '<', jan3.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '<=', jan3.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 75
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '>', jan2.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 48
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '>', '0001-01-01']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 98
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '>=', jan2.isoformat()]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 73
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '=', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '__ne__', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 98
        return

    @nottest
    def test_search_q_date_invalid(self):
        """Tests SEARCH /forms: invalid date searches."""
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '=', '12-01-01']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 12-01-01'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', '=', '2012-01-32']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 2012-01-32'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', 'regex', '01']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['date 01'] == 'Date search parameters must be valid ISO 8601 date strings.'
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', 'regex', '2012-01-01']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 25
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', 'like', '2012-01-01']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 25
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', 'in', '2012-01-02']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.date_elicited.in_'] == 'Invalid filter expression: Form.date_elicited.in_(datetime.date(2012, 1, 2))'
        json_query = json.dumps({'query': {'filter': ['Form', 'date_elicited', 'in', ['2012-01-01', '2012-01-02']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50

    @nottest
    def test_search_r_datetime(self):
        """Tests POST /forms/search: datetime searches."""
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '=', today_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 49
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '=', yesterday_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '!=', today_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '!=', yesterday_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 49
        query = {'query': {'filter': [
                              'or',
                              [['Form', 'datetime_entered', '!=', today_timestamp_iso],
                               [
                                'Form', 'datetime_entered', '=', None]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 51
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '<', today_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 50
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_modified', '<=', today_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '>', today_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 0
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '>', '1901-01-01T09:08:07']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '>=', yesterday_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '=', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_entered', '__ne__', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        midnight_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        midnight_tomorrow = midnight_today + day_delta
        query = {'query': {'filter': [
                              'and',
                              [['Form', 'datetime_entered', '>', midnight_today.isoformat()],
                               [
                                'Form', 'datetime_entered', '<', midnight_tomorrow.isoformat()]]]}}
        json_query = json.dumps(query)
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 49
        return

    @nottest
    def test_search_s_datetime_invalid(self):
        """Tests SEARCH /forms: invalid datetime searches."""
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_modified', '=', '12-01-01T09']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 12-01-01T09'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_modified', '=', '2012-01-30T09:08:61']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 2012-01-30T09:08:61'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_modified', '=', '2012-01-30T09:08:59.123456789123456789123456789']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_modified', '=', '2012-01-30T09:08:59.']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        json_query = json.dumps({'query': {'filter': ['Form', 'datetime_modified', 'regex', '01']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['datetime 01'] == 'Datetime search parameters must be valid ISO 8601 datetime strings.'
        RDBMSName = h.get_RDBMS_name(config_filename='test.ini')
        if RDBMSName == 'mysql':
            if mysql_engine == 'InnoDB':
                _today_timestamp = h.round_datetime(today_timestamp).isoformat()
            else:
                _today_timestamp = today_timestamp.isoformat().split('.')[0]
        else:
            _today_timestamp = today_timestamp.isoformat()
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_modified', 'regex', _today_timestamp]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_modified', 'like', _today_timestamp]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_modified', 'in', today_timestamp_iso]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        error_prefix = 'Invalid filter expression: Form.datetime_modified.in_'
        received_error = resp['errors']['Form.datetime_modified.in_']
        assert received_error.startswith(error_prefix)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'datetime_modified', 'in',
                              [
                               today_timestamp_iso, yesterday_timestamp_iso]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99

    @nottest
    def test_search_t_many_to_one(self):
        """Tests POST /forms/search: searches on many-to-one attributes."""
        test_models = _get_test_models()
        users = h.get_users()
        forms = h.get_forms()
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        json_query = json.dumps({'query': {'filter': ['Form', 'enterer', 'id', '=', contributor.id]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'speaker', 'id', '=', test_models['speakers'][0].id]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 49
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'speaker', 'id', 'in', [ s.id for s in test_models['speakers'] ]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'elicitation_method', 'id', '<', 56]}})
        expected_forms = [ f for f in forms if f.elicitationmethod_id < 56 ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_forms)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'elicitation_method', 'name', 'regex', '5']}})
        expected_forms = [ f for f in forms if '5' in f.elicitation_method.name ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_forms)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'elicitation_method', 'id', 'regex', '[56]']}})
        expected_forms = [ f for f in forms if '5' in str(f.elicitationmethod_id) or '6' in str(f.elicitationmethod_id)
                         ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_forms)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'syntactic_category', 'name', 'like', '%5%']}})
        expected_forms = [ f for f in forms if '5' in f.syntactic_category.name ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len(expected_forms)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'syntactic_category', 'name', 'like', '%5%']}})
        expected_forms = [ f for f in forms if '5' in f.syntactic_category.name ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp
        assert len(resp) == len(expected_forms)
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': ['Form', 'source', '!=', None]}})
        expected_forms = [ f for f in forms if f.source ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp
        assert len(resp) == len(expected_forms)
        json_query = json.dumps({'query': {'filter': ['Form', 'source', '=', None]}})
        expected_forms = [ f for f in forms if not f.source ]
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp
        assert len(resp) == len(expected_forms)
        return

    @nottest
    def test_search_u_one_to_many(self):
        """Tests SEARCH /forms: searches on one-to-many attributes, viz. Translation."""
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'transcription', '=', 'translation 1']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'translations', 'transcription', '=', 'translation 1']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'grammaticality', '=', '*']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 24
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'transcription', 'like', '%1%']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 20
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'transcription', 'regex', '[13][25]']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 4
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'transcription', 'in_', ['translation 1', 'translation 2']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'transcription', '<', 'z']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': [
                              'Translation', 'datetime_modified', '>', yesterday_timestamp_iso]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'translations', '=', None]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'translations', '=', []]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'translations', '!=', None]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 99
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'translations', 'like', None]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.translations.like'] == 'The relation like is not permitted for Form.translations'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'translations', '=', 'translation 1']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Translation', 'transcription', '=', 'translation 79'],
                               [
                                'Translation', 'transcription', '=', 'translation 79 the second']]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Translation', 'grammaticality', '=', '*'],
                               [
                                'Translation', 'grammaticality', '=', None]]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Form', 'translations', 'grammaticality', '=', '*'],
                               [
                                'Form', 'translations', 'grammaticality', '=', None]]]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        return

    @nottest
    def test_search_v_many_to_many(self):
        """Tests POST /forms/search: searches on many-to-many attributes, i.e., Tag, File, Collection, User."""
        json_query = json.dumps({'query': {'filter': ['Tag', 'name', '=', 'name 76']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'like', '%name 6%']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 4
        json_query = json.dumps({'query': {'filter': [
                              'File', 'name', 'regex', 'name [67]']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 14
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'files', 'name', 'regex', 'name [67]']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 14
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', 'in_', ['name 77', 'name 79', 'name 99']]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 3
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', '<', 'name 8']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 5
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', '>', yesterday_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 20
        json_query = json.dumps({'query': {'filter': [
                              'File', 'datetime_modified', '<', yesterday_timestamp_iso]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 0
        json_query = json.dumps({'query': {'filter': ['Form', 'tags', '=', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 75
        json_query = json.dumps({'query': {'filter': ['Form', 'files', '!=', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 20
        json_query = json.dumps({'query': {'filter': ['Form', 'tags', 'like', None]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.tags.like'] == 'The relation like is not permitted for Form.tags'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'files', '=', 'file 80']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['InvalidRequestError'] == "Can't compare a collection to an object or collection; use contains() to test for membership."
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', 'in_', ['name 78', 'name 79']]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Tag', 'name', '=', 'name 78'],
                               [
                                'Tag', 'name', '=', 'name 79']]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'Tag', 'name', '=', 'name 78']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Tag', 'name', '=', 'name 78'],
                               [
                                'Tag', 'name', '=', 'name 79']]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        forms = h.get_forms()
        users = h.get_users()
        viewer_remembered_forms = [ f for f in forms if int(f.transcription.split(' ')[(-1)]) > 75
                                  ]
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        contributor_remembered_forms = [ f for f in forms if int(f.transcription.split(' ')[(-1)]) > 65 and int(f.transcription.split(' ')[(-1)]) < 86
                                       ]
        contributor_id = contributor.id
        administrator_remembered_forms = [ f for f in forms if int(f.transcription.split(' ')[(-1)]) > 50
                                         ]
        json_query = json.dumps({'query': {'filter': [
                              'Memorizer', 'role', 'in', ['administrator', 'viewer']]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = list(set(viewer_remembered_forms) | set(administrator_remembered_forms))
        assert set([ f['id'] for f in resp ]) == set([ f.id for f in result_set ])
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'memorizers', 'role', 'in', ['administrator', 'viewer']]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert set([ f['id'] for f in resp ]) == set([ f.id for f in result_set ])
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [['Memorizer', 'id', '=', contributor_id],
                               [
                                'Form', 'transcription', 'regex', '[13580]']]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in contributor_remembered_forms if re.search('[13580]', f.transcription)
                     ]
        assert set([ f['id'] for f in resp ]) == set([ f.id for f in result_set ])
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [['Form', 'memorizers', 'id', '=', contributor_id],
                               [
                                'Form', 'transcription', 'regex', '[13580]']]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert set([ f['id'] for f in resp ]) == set([ f.id for f in result_set ])
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': ['Memorizer', 'username', 'like', '%e%']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['errors']['Memorizer.username'] == 'Searching on Memorizer.username is not permitted'
        json_query = json.dumps({'query': {'filter': ['Form', 'memorizers', 'username', 'like', '%e%']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['errors']['User.username'] == 'Searching on User.username is not permitted'
        return

    @nottest
    def test_search_w_in(self):
        """Tests SEARCH /forms: searches using the in_ relation."""
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'in', ['transcription 1']]}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'in', 'transcription 1']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 0

    @nottest
    def test_search_x_complex(self):
        """Tests POST /forms/search: complex searches."""
        forms = json.loads(json.dumps(h.get_forms(), cls=h.JSONOLDEncoder))
        RDBMSName = h.get_RDBMS_name(config_filename='test.ini')
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Translation', 'transcription', 'like', '%1%'],
                               [
                                'not', ['Form', 'morpheme_break', 'regex', '[18][5-7]']],
                               [
                                'or',
                                [
                                 [
                                  'Form', 'datetime_modified', '=', today_timestamp_iso],
                                 [
                                  'Form', 'date_elicited', '=', jan1.isoformat()]]]]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        mysql_engine = Model.__table_args__.get('mysql_engine')
        if RDBMSName == 'mysql' and mysql_engine == 'InnoDB':
            _today_timestamp = h.round_datetime(today_timestamp)
        else:
            _today_timestamp = today_timestamp
        result_set = [ f for f in forms if '1' in (' ').join([ g['transcription'] for g in f['translations'] ]) and not re.search('[18][5-7]', f['morpheme_break']) and (_today_timestamp.isoformat().split('.')[0] == f['datetime_modified'].split('.')[0] or f['date_elicited'] and jan1.isoformat() == f['date_elicited'])
                     ]
        assert len(resp) == len(result_set)
        tag_names = [
         'name 2', 'name 4', 'name 88']
        patt = '([13579][02468])|([02468][13579])'
        json_query = json.dumps({'query': {'filter': [
                              'or',
                              [
                               [
                                'Translation', 'transcription', 'like', '%1%'],
                               [
                                'Tag', 'name', 'in', ['name 2', 'name 4', 'name 88']],
                               [
                                'and',
                                [
                                 [
                                  'not', ['File', 'name', 'regex', patt]],
                                 [
                                  'Form', 'date_elicited', '!=', None]]]]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in forms if '1' in (' ').join([ g['transcription'] for g in f['translations'] ]) or set([ t['name'] for t in f['tags'] ]) & set(tag_names) or f['files'] and not re.search(patt, (', ').join([ fi['name'] for fi in f['files'] ])) and f['date_elicited'] is not None
                     ]
        assert len(resp) == len(result_set)
        json_query = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Form', 'transcription', 'like', '%5%'],
                               [
                                'Form', 'morpheme_break', 'like', '%9%'],
                               [
                                'not', ['Translation', 'transcription', 'like', '%6%']],
                               [
                                'or',
                                [
                                 [
                                  'Form', 'datetime_entered', '<', today_timestamp_iso],
                                 [
                                  'Form', 'datetime_modified', '>', yesterday_timestamp_iso],
                                 [
                                  'not', ['Form', 'date_elicited', 'in', [jan1.isoformat(), jan3.isoformat()]]],
                                 [
                                  'and',
                                  [
                                   [
                                    'Form', 'enterer', 'id', 'regex', '[135680]'],
                                   [
                                    'Form', 'id', '<', 90]]]]],
                               [
                                'not', ['not', ['not', ['Tag', 'name', '=', 'name 7']]]]]]}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        return

    @nottest
    def test_search_y_paginator(self):
        """Tests SEARCH /forms: paginator."""
        forms = json.loads(json.dumps(h.get_forms(), cls=h.JSONOLDEncoder))
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%T%']}, 
           'paginator': {'page': 2, 'items_per_page': 10}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        result_set = [ f for f in forms if 'T' in f['transcription'] ]
        assert resp['paginator']['count'] == len(result_set)
        assert len(resp['items']) == 10
        assert resp['items'][0]['id'] == result_set[10]['id']
        assert resp['items'][(-1)]['id'] == result_set[19]['id']
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%T%']}, 
           'paginator': {'page': 0, 'items_per_page': 10}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%T%']}, 
           'paginator': {'pages': 0, 'items_per_page': 10}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == len([ f for f in forms if 'T' in f['transcription'] ])
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%T%']}, 
           'paginator': {'page': 2, 'items_per_page': 16, 'count': 750}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['paginator']['count'] == 750
        assert len(resp['items']) == 16
        assert resp['items'][0]['id'] == result_set[16]['id']
        assert resp['items'][(-1)]['id'] == result_set[31]['id']

    @nottest
    def test_search_z_order_by(self):
        """Tests POST /forms/search: order by."""
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Form', 'transcription', 'asc']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[(-1)]['transcription'] == 'TRANSCRIPTION 99'
        assert resp[0]['transcription'] == 'transcription 1'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Form', 'transcription', 'desc']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[(-1)]['transcription'] == 'transcription 1'
        assert resp[0]['transcription'] == 'TRANSCRIPTION 99'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Translation', 'transcription', 'asc']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[0]['translations'] == []
        assert resp[1]['translations'][0]['transcription'] == 'translation 1'
        assert resp[(-1)]['translations'][0]['transcription'] == 'translation 99'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Translation', 'transcription']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[0]['translations'] == []
        assert resp[1]['translations'][0]['transcription'] == 'translation 1'
        assert resp[(-1)]['translations'][0]['transcription'] == 'translation 99'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Translation', 'transcription', 'descending']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[0]['translations'] == []
        assert resp[1]['translations'][0]['transcription'] == 'translation 1'
        assert resp[(-1)]['translations'][0]['transcription'] == 'translation 99'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Translation']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Form', 'foo', 'desc']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.foo'] == 'Searching on Form.foo is not permitted'
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]'], 
                     'order_by': [
                                'Foo', 'id', 'desc']}})
        response = self.app.post(url('/forms/search'), json_query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Foo'] == 'Searching the Form model by joining on the Foo model is not possible'
        assert resp['errors']['Foo.id'] == 'Searching on Foo.id is not permitted'
        assert resp['errors']['OrderByError'] == 'The provided order by expression was invalid.'

    @nottest
    def test_search_za_restricted(self):
        """Tests SEARCH /forms: restricted forms."""
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        forms = h.get_forms()
        form_count = len(forms)
        for form in forms:
            if int(form.transcription.split(' ')[(-1)]) % 2 == 0:
                form.tags.append(restricted_tag)

        Session.commit()
        restricted_forms = Session.query(model.Form).filter(model.Tag.name == 'restricted').outerjoin(model.Form.tags).all()
        restricted_form_count = len(restricted_forms)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == restricted_form_count
        assert 'restricted' not in [ x['name'] for x in reduce(list.__add__, [ f['tags'] for f in resp ]) ]
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == form_count
        assert 'restricted' in [ x['name'] for x in reduce(list.__add__, [ f['tags'] for f in resp ]) ]
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regex', '[tT]']}, 
           'paginator': {'page': 3, 'items_per_page': 7}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = [ f for f in forms if int(f.transcription.split(' ')[(-1)]) % 2 != 0
                     ]
        assert resp['paginator']['count'] == restricted_form_count
        assert len(resp['items']) == 7
        assert resp['items'][0]['id'] == result_set[14].id

    @nottest
    def test_search_zb_like_escaping(self):
        """Tests SEARCH /forms: escaping special characters in LIKE queries.

        Note: these tests are RDBMS-specific: MySQL allows escaping of "_" and
        "%" in LIKE queries via the backslash.  In SQLite, on the other hand,
        the backslash only works if "ESCAPE ''" is specified after the LIKE
        pattern.  As far as I can tell, this is not supported in SQLAlchemy.
        Therefore, any OLD system using SQLite will not permit searching for "_"
        or "%" in LIKE queries (regexp will do the trick though...).
        """
        create_params = self.form_create_params
        RDBMSName = h.get_RDBMS_name(config_filename='test.ini')
        params = create_params.copy()
        params.update({'transcription': '_%', 
           'translations': [
                          {'transcription': 'LIKE, test or some junk', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        forms = Session.query(model.Form).all()
        forms_count = len(forms)
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%_%']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == forms_count
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%\\_%']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        if RDBMSName == 'mysql':
            assert len(resp) == 1
        else:
            assert len(resp) == 0
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regexp', '_']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == forms_count
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'like', '%\\%%']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        if RDBMSName == 'mysql':
            assert len(resp) == 1
        else:
            assert len(resp) == 0
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'Form', 'transcription', 'regexp', '%']}})
        response = self.app.request(url('forms'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert response.content_type == 'application/json'

    @nottest
    def test_z_cleanup(self):
        """Tests POST /forms/search: clean up the database."""
        users = h.get_users()
        viewer = [ u for u in users if u.role == 'viewer' ][0]
        contributor = [ u for u in users if u.role == 'contributor' ][0]
        administrator = [ u for u in users if u.role == 'administrator' ][0]
        viewer.remembered_forms = []
        contributor.remembered_forms = []
        administrator.remembered_forms = []
        Session.commit()
        h.clear_all_models()
        administrator = h.generate_default_administrator()
        contributor = h.generate_default_contributor()
        viewer = h.generate_default_viewer()
        Session.add_all([administrator, contributor, viewer])
        Session.commit()
        extra_environ = self.extra_environ_admin.copy()
        extra_environ['test.application_settings'] = True
        self.app.get(url('forms'), extra_environ=extra_environ)