# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_rememberedforms.py
# Compiled at: 2016-09-19 13:27:02
import re
from time import sleep
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

def get_users():
    users = h.get_users()
    viewer = [ u for u in users if u.role == 'viewer' ][0]
    contributor = [ u for u in users if u.role == 'contributor' ][0]
    administrator = [ u for u in users if u.role == 'administrator' ][0]
    return (viewer, contributor, administrator)


def _create_test_models(n=100):
    _add_test_models_to_session('Tag', n, ['name'])
    _add_test_models_to_session('Speaker', n, ['first_name', 'last_name', 'dialect'])
    _add_test_models_to_session('Source', n, ['author_first_name', 'author_last_name',
     'title'])
    _add_test_models_to_session('ElicitationMethod', n, ['name'])
    _add_test_models_to_session('SyntacticCategory', n, ['name'])
    _add_test_models_to_session('File', n, ['name'])
    restricted_tag = h.generate_restricted_tag()
    Session.add(restricted_tag)
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
    viewer, contributor, administrator = get_users()
    restricted_tag = h.get_restricted_tag()
    for i in range(1, n + 1):
        f = model.Form()
        f.transcription = 'transcription %d' % i
        if i > 50:
            f.transcription = f.transcription.upper()
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
        if i > 65 and i < 86:
            fi = test_models['files'][(i - 1)]
            f.files.append(fi)
        if i > 50:
            f.elicitor = contributor
            f.tags.append(restricted_tag)
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


class TestRememberedformsController(TestController):
    """This test suite is modelled on the test_forms_search and test_oldcollections_search
    pattern, i.e., an initialize "test" runs first and a clean up one runs at the
    end.  Also, the update test should run before the show and search tests because
    the former creates the remembered forms for the latter two to retrieve.
    """
    n = 100

    def tearDown(self):
        pass

    @nottest
    def test_a_initialize(self):
        """Initialize the database for /rememberedforms tests."""
        h.clear_all_models()
        administrator = h.generate_default_administrator()
        contributor = h.generate_default_contributor()
        viewer = h.generate_default_viewer()
        Session.add_all([administrator, contributor, viewer])
        Session.commit()
        _create_test_data(self.n)
        self._add_SEARCH_to_web_test_valid_methods()
        viewer, contributor, administrator = get_users()
        application_settings = h.generate_default_application_settings()
        application_settings.unrestricted_users = [contributor]
        Session.add(application_settings)
        Session.commit()

    @nottest
    def test_b_update(self):
        """Tests that PUT /rememberedforms/id correctly updates the set of forms remembered by the user with id=id."""
        forms = sorted(json.loads(json.dumps(h.get_forms(), cls=h.JSONOLDEncoder)), key=lambda f: f['id'])
        viewer, contributor, administrator = get_users()
        viewer_id = viewer.id
        viewer_datetime_modified = viewer.datetime_modified
        contributor_id = contributor.id
        administrator_id = administrator.id
        sleep(1)
        params = json.dumps({'forms': [ f['id'] for f in forms ]})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_view_appset)
        resp = json.loads(response.body)
        viewer_remembered_forms = sorted(resp, key=lambda f: f['id'])
        result_set = [ f for f in forms if 'restricted' not in [ t['name'] for t in f['tags'] ] ]
        viewer, contributor, administrator = get_users()
        new_viewer_datetime_modified = viewer.datetime_modified
        assert new_viewer_datetime_modified != viewer_datetime_modified
        assert set([ f['id'] for f in result_set ]) == set([ f['id'] for f in resp ])
        assert response.content_type == 'application/json'
        params = json.dumps({'forms': []})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_contrib_appset, status=403)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'You are not authorized to access this resource.'
        user_forms = Session.query(model.UserForm).filter(model.UserForm.user_id == viewer_id).all()
        expected_new_user_form_ids = [ uf.id for uf in user_forms if uf.form_id != viewer_remembered_forms[(-1)]['id']
                                     ]
        params = json.dumps({'forms': [ f['id'] for f in viewer_remembered_forms ][:-1]})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_admin_appset)
        resp = json.loads(response.body)
        result_set = result_set[:-1]
        assert set([ f['id'] for f in result_set ]) == set([ f['id'] for f in resp ])
        assert response.content_type == 'application/json'
        user_forms = Session.query(model.UserForm).filter(model.UserForm.user_id == viewer_id).all()
        current_user_form_ids = sorted([ uf.id for uf in user_forms ])
        assert set(expected_new_user_form_ids) == set(current_user_form_ids)
        params = json.dumps({'forms': []})
        response = self.app.put(url(controller='rememberedforms', action='update', id=100896), params, self.json_headers, self.extra_environ_admin_appset, status=404)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'There is no user with id 100896'
        params = json.dumps({'forms': ['a', 1000000087654]})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_admin_appset, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['errors']['forms'] == ['Please enter an integer value',
         'There is no form with id 1000000087654.']
        params = json.dumps({'forms': []})[:-1]
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_admin_appset, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'JSON decode error: the parameters provided were not valid JSON.'
        params = json.dumps({'forms': []})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_admin_appset)
        resp = json.loads(response.body)
        viewer = Session.query(model.User).filter(model.User.role == 'viewer').first()
        assert response.content_type == 'application/json'
        assert viewer.remembered_forms == []
        assert resp == []
        params = json.dumps({'forms': []})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_view_appset, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        params = json.dumps({'forms': [ f['id'] for f in forms ]})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, status=401)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'Authentication is required to access this resource.'
        params = json.dumps({'forms': [ f['id'] for f in forms ]})
        response = self.app.put(url(controller='rememberedforms', action='update', id=viewer_id), params, self.json_headers, self.extra_environ_view_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        result_set = [ f for f in forms if 'restricted' not in [ t['name'] for t in f['tags'] ] ]
        assert set([ f['id'] for f in result_set ]) == set([ f['id'] for f in resp ])
        params = json.dumps({'forms': [ f['id'] for f in forms ]})
        response = self.app.put(url(controller='rememberedforms', action='update', id=contributor_id), params, self.json_headers, self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert set([ f['id'] for f in forms ]) == set([ f['id'] for f in resp ])
        odd_numbered_form_ids = [ f['id'] for f in forms if f['id'] % 2 != 0 ]
        params = json.dumps({'forms': odd_numbered_form_ids})
        response = self.app.put(url(controller='rememberedforms', action='update', id=contributor_id), params, self.json_headers, self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert set(odd_numbered_form_ids) == set([ f['id'] for f in resp ])
        form_ids_for_admin = [ f['id'] for f in forms if f['id'] % 2 != 0 and f['id'] > 25 ]
        params = json.dumps({'forms': form_ids_for_admin})
        response = self.app.put(url(controller='rememberedforms', action='update', id=administrator_id), params, self.json_headers, self.extra_environ_contrib_appset, status=403)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'You are not authorized to access this resource.'
        form_ids_for_admin = [ f['id'] for f in forms if f['id'] % 2 == 0 and f['id'] > 25 ]
        params = json.dumps({'forms': form_ids_for_admin})
        response = self.app.put(url(controller='rememberedforms', action='update', id=administrator_id), params, self.json_headers, self.extra_environ_admin_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert set(form_ids_for_admin) == set([ f['id'] for f in resp ])

    @nottest
    def test_c_show(self):
        """Tests that GET /rememberedforms/id returns an array of the forms remembered by the user with id=id."""
        forms = json.loads(json.dumps(h.get_forms(), cls=h.JSONOLDEncoder))
        viewer, contributor, administrator = get_users()
        viewer_id = viewer.id
        contributor_id = contributor.id
        administrator_id = administrator.id
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        result_set = [ f for f in forms if 'restricted' not in [ t['name'] for t in f['tags'] ] ]
        assert response.content_type == 'application/json'
        assert set([ f['id'] for f in result_set ]) == set([ f['id'] for f in resp ])
        paginator = {'items_per_page': 7, 'page': 3}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), paginator, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert len(resp['items']) == 7
        assert resp['items'][0]['transcription'] == result_set[14]['transcription']
        order_by_params = {'order_by_model': 'Form', 'order_by_attribute': 'transcription', 'order_by_direction': 'desc'}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        result_set_ordered = sorted(result_set, key=lambda f: f['transcription'], reverse=True)
        assert response.content_type == 'application/json'
        assert result_set_ordered == resp
        params = {'order_by_model': 'Form', 'order_by_attribute': 'transcription', 'order_by_direction': 'desc', 
           'items_per_page': 7, 'page': 3}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), params, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        assert len(resp['items']) == 7
        assert result_set_ordered[14]['transcription'] == resp['items'][0]['transcription']
        order_by_params = {'order_by_model': 'Form', 'order_by_attribute': 'transcription', 'order_by_direction': 'descending'}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        order_by_params = {'order_by_model': 'Formosa', 'order_by_attribute': 'transcrumption', 'order_by_direction': 'desc'}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        assert resp[0]['id'] == forms[0]['id']
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), paginator, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url(controller='rememberedforms', action='show', id=viewer_id), paginator, headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        response = self.app.get(url(controller='rememberedforms', action='show', id=contributor_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        result_set = [ f for f in forms if f['id'] % 2 != 0 ]
        assert response.content_type == 'application/json'
        assert set([ f['id'] for f in result_set ]) == set([ f['id'] for f in resp ])
        response = self.app.get(url(controller='rememberedforms', action='show', id=200987654), headers=self.json_headers, extra_environ=self.extra_environ_contrib_appset, status=404)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'There is no user with id 200987654'
        response = self.app.get(url(controller='rememberedforms', action='show', id=administrator_id), headers=self.json_headers, extra_environ=self.extra_environ_admin_appset)
        resp = json.loads(response.body)
        result_set = [ f for f in forms if f['id'] % 2 == 0 and f['id'] > 25 ]
        assert response.content_type == 'application/json'
        assert set([ f['id'] for f in result_set ]) == set([ f['id'] for f in resp ])

    @nottest
    def test_d_search(self):
        """Tests that SEARCH /rememberedforms/id returns an array of the forms remembered by the user with id=id that match the search criteria.

        Here we show the somewhat complex interplay of the unrestricted users, the
        restricted tag and the remembered_forms relation between users and forms.
        """
        forms = json.loads(json.dumps(h.get_forms(), cls=h.JSONOLDEncoder))
        mysql_engine = Model.__table_args__.get('mysql_engine')
        viewer, contributor, administrator = get_users()
        viewer_id = viewer.id
        contributor_id = contributor.id
        administrator_id = administrator.id
        viewer_remembered_forms = [ f for f in forms if 'restricted' not in [ t['name'] for t in f['tags'] ]
                                  ]
        contributor_remembered_forms = [ f for f in forms if f['id'] % 2 != 0 ]
        administrator_remembered_forms = [ f for f in forms if f['id'] % 2 == 0 and f['id'] > 25 ]
        RDBMSName = h.get_RDBMS_name(config_filename='test.ini')
        _today_timestamp = today_timestamp
        if RDBMSName == 'mysql' and mysql_engine == 'InnoDB':
            _today_timestamp = h.round_datetime(today_timestamp)
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
                                  'Form', 'datetime_modified', '=', today_timestamp.isoformat()],
                                 [
                                  'Form', 'date_elicited', '=', jan1.isoformat()]]]]]}})
        json_query_admin = json.dumps({'query': {'filter': [
                              'and',
                              [
                               [
                                'Translation', 'transcription', 'like', '%8%'],
                               [
                                'not', ['Form', 'morpheme_break', 'regex', '[18][5-7]']],
                               [
                                'or',
                                [
                                 [
                                  'Form', 'datetime_modified', '=', today_timestamp.isoformat()],
                                 [
                                  'Form', 'date_elicited', '=', jan1.isoformat()]]]]]}})
        result_set_viewer = [ f for f in viewer_remembered_forms if '1' in (' ').join([ g['transcription'] for g in f['translations'] ]) and not re.search('[18][5-7]', f['morpheme_break']) and (_today_timestamp.isoformat().split('.')[0] == f['datetime_modified'].split('.')[0] or f['date_elicited'] and jan1.isoformat() == f['date_elicited'])
                            ]
        result_set_contributor = [ f for f in contributor_remembered_forms if '1' in (' ').join([ g['transcription'] for g in f['translations'] ]) and not re.search('[18][5-7]', f['morpheme_break']) and (_today_timestamp.isoformat().split('.')[0] == f['datetime_modified'].split('.')[0] or f['date_elicited'] and jan1.isoformat() == f['date_elicited'])
                                 ]
        result_set_administrator = [ f for f in administrator_remembered_forms if '8' in (' ').join([ g['transcription'] for g in f['translations'] ]) and not re.search('[18][5-7]', f['morpheme_break']) and (_today_timestamp.isoformat().split('.')[0] == f['datetime_modified'].split('.')[0] or f['date_elicited'] and jan1.isoformat() == f['date_elicited'])
                                   ]
        response = self.app.post(url('/rememberedforms/%d/search' % viewer_id), json_query, self.json_headers, self.extra_environ_admin_appset)
        resp = json.loads(response.body)
        assert [ f['id'] for f in result_set_viewer ] == [ f['id'] for f in resp ]
        assert response.content_type == 'application/json'
        assert resp
        response = self.app.request(url('/rememberedforms/%d' % contributor_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        assert [ f['id'] for f in result_set_contributor ] == [ f['id'] for f in resp ]
        assert response.content_type == 'application/json'
        assert resp
        response = self.app.post(url('/rememberedforms/%d/search' % contributor_id), json_query, self.json_headers, self.extra_environ_view_appset)
        resp = json.loads(response.body)
        result_set = [ f for f in result_set_contributor if 'restricted' not in [ t['name'] for t in f['tags'] ]
                     ]
        assert [ f['id'] for f in result_set ] == [ f['id'] for f in resp ]
        assert response.content_type == 'application/json'
        assert resp
        response = self.app.request(url('/rememberedforms/%d' % administrator_id), method='SEARCH', body=json_query_admin, headers=self.json_headers, environ=self.extra_environ_view_appset)
        resp = json.loads(response.body)
        result_set = [ f for f in result_set_administrator if 'restricted' not in [ t['name'] for t in f['tags'] ]
                     ]
        assert [ f['id'] for f in result_set ] == [ f['id'] for f in resp ]
        assert response.content_type == 'application/json'
        response = self.app.post(url('/rememberedforms/%d/search' % administrator_id), json_query_admin, self.json_headers, self.extra_environ_contrib_appset)
        resp = json.loads(response.body)
        result_set = result_set_administrator
        assert [ f['id'] for f in result_set ] == [ f['id'] for f in resp ]
        assert response.content_type == 'application/json'
        assert resp
        response = self.app.request(url('/rememberedforms/%d' % administrator_id), method='SEARCH', body=json_query_admin, headers=self.json_headers, environ=self.extra_environ_admin_appset)
        resp = json.loads(response.body)
        result_set = result_set_administrator
        assert [ f['id'] for f in result_set ] == [ f['id'] for f in resp ]
        assert response.content_type == 'application/json'
        assert resp

    @nottest
    def test_e_cleanup(self):
        """Clean up the database after /rememberedforms tests."""
        h.clear_all_models()
        administrator = h.generate_default_administrator()
        contributor = h.generate_default_contributor()
        viewer = h.generate_default_viewer()
        Session.add_all([administrator, contributor, viewer])
        Session.commit()
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        self.app.get(url('forms'), extra_environ=extra_environ)