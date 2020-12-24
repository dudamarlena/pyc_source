# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_applicationsettings.py
# Compiled at: 2016-09-19 13:27:02
import datetime, logging, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
from onlinelinguisticdatabase.model import ApplicationSettings, User, Orthography
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)

def add_default_application_settings():
    """Add the default application settings to the database."""
    orthography1 = h.generate_default_orthography1()
    orthography2 = h.generate_default_orthography2()
    contributor = Session.query(User).filter(User.role == 'contributor').first()
    application_settings = h.generate_default_application_settings([orthography1, orthography2], [contributor])
    Session.add(application_settings)
    Session.commit()
    return application_settings


class TestApplicationsettingsController(TestController):

    @nottest
    def test_index(self):
        """Tests that GET /applicationsettings returns a JSON array of application settings objects."""
        application_settings = add_default_application_settings()
        response = self.app.get(url('applicationsettings'), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp) == 1
        assert resp[0]['object_language_name'] == application_settings.object_language_name
        assert resp[0]['storage_orthography']['name'] == application_settings.storage_orthography.name
        assert resp[0]['unrestricted_users'][0]['role'] == application_settings.unrestricted_users[0].role

    @nottest
    def test_create(self):
        """Tests that POST /applicationsettings correctly creates a new application settings."""
        orthography1 = h.generate_default_orthography1()
        orthography2 = h.generate_default_orthography2()
        Session.add_all([orthography1, orthography2])
        Session.commit()
        orthography2_id = orthography2.id
        orthography2_orthography = orthography2.orthography
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': 'test_create object language name', 
           'object_language_id': 'tco', 
           'metalanguage_name': 'test_create metalanguage name', 
           'metalanguage_id': 'tcm', 
           'orthographic_validation': 'Warning', 
           'narrow_phonetic_validation': 'Error', 
           'morpheme_break_is_orthographic': False, 
           'morpheme_delimiters': '-,+', 
           'punctuation': '!?.,;:-_', 
           'grammaticalities': '*,**,***,?,??,???,#,##,###', 
           'unrestricted_users': [
                                Session.query(User).filter(User.role == 'viewer').first().id], 
           'storage_orthography': orthography2_id, 
           'input_orthography': orthography2_id, 
           'output_orthography': orthography2_id})
        params = json.dumps(params)
        response = self.app.post(url('applicationsettings'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['object_language_name'] == 'test_create object language name'
        assert resp['morpheme_break_is_orthographic'] is False
        assert resp['storage_orthography']['orthography'] == orthography2_orthography
        assert resp['unrestricted_users'][0]['first_name'] == 'Viewer'
        assert 'password' not in resp['unrestricted_users'][0]
        assert response.content_type == 'application/json'
        response = self.app.post(url('applicationsettings'), params, self.json_headers, self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'You are not authorized to access this resource.'

    @nottest
    def test_create_invalid(self):
        """Tests that POST /applicationsettings responds with an appropriate error when invalid params are submitted in the request."""
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': '!' * 256, 
           'object_language_id': 'too long', 
           'orthographic_validation': 'No Way!', 
           'morpheme_break_is_orthographic': 'Truish', 
           'storage_orthography': 'accept me!'})
        params = json.dumps(params)
        response = self.app.post(url('applicationsettings'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['errors']['object_language_id'] == 'Enter a value not more than 3 characters long'
        assert resp['errors']['object_language_name'] == 'Enter a value not more than 255 characters long'
        assert 'Value must be one of: None; Warning; Error' in resp['errors']['orthographic_validation']
        assert "Value should be 'true' or 'false'" in resp['errors']['morpheme_break_is_orthographic']
        assert resp['errors']['storage_orthography'] == 'Please enter an integer value'

    @nottest
    def test_new(self):
        """Tests that GET /applicationsettings/new returns an appropriate JSON object for creating a new application settings object.

        The properties of the JSON object are 'languages', 'users' and
        'orthographies' and their values are arrays/lists.
        """
        orthography1 = h.generate_default_orthography1()
        orthography2 = h.generate_default_orthography2()
        Session.add_all([orthography1, orthography2])
        Session.commit()
        data = {'languages': h.get_languages(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'orthographies': h.get_mini_dicts_getter('Orthography')()}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        response = self.app.get(url('new_applicationsetting'), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['languages'] == data['languages']
        assert resp['users'] == data['users']
        assert resp['orthographies'] == data['orthographies']
        assert response.content_type == 'application/json'
        params = {'languages': '', 
           'users': 'anything can go here!', 
           'orthographies': datetime.datetime.utcnow().isoformat()}
        response = self.app.get(url('new_applicationsetting'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['languages'] == []
        assert resp['users'] == data['users']
        assert resp['orthographies'] == data['orthographies']

    @nottest
    def test_update(self):
        """Tests that PUT /applicationsettings/id correctly updates an existing application settings."""
        application_settings_count = Session.query(ApplicationSettings).count()
        contributor_id = Session.query(User).filter(User.role == 'contributor').first().id
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': 'test_update object language name', 
           'object_language_id': 'tuo', 
           'metalanguage_name': 'test_update metalanguage name', 
           'metalanguage_id': 'tum', 
           'orthographic_validation': 'None', 
           'narrow_phonetic_validation': 'Warning', 
           'morpheme_break_is_orthographic': True, 
           'morpheme_delimiters': '+', 
           'punctuation': '!.;:', 
           'grammaticalities': '*,**,?,??,#,##', 
           'unrestricted_users': [
                                contributor_id]})
        params = json.dumps(params)
        response = self.app.post(url('applicationsettings'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        id = int(resp['id'])
        new_application_settings_count = Session.query(ApplicationSettings).count()
        assert resp['object_language_name'] == 'test_update object language name'
        assert resp['unrestricted_users'][0]['role'] == 'contributor'
        assert new_application_settings_count == application_settings_count + 1
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': 'Updated!', 
           'unrestricted_users': [
                                2000, 5000], 
           'morpheme_delimiters': '-,='})
        params = json.dumps(params)
        response = self.app.put(url('applicationsetting', id=id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        application_settings_count = new_application_settings_count
        new_application_settings_count = Session.query(ApplicationSettings).count()
        assert resp['errors']['unrestricted_users'] == ['There is no user with id 2000.', 'There is no user with id 5000.']
        assert new_application_settings_count == application_settings_count
        assert response.content_type == 'application/json'
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': 'Updated!', 
           'unrestricted_users': [
                                contributor_id], 
           'morpheme_delimiters': '-,='})
        params = json.dumps(params)
        response = self.app.put(url('applicationsetting', id=id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        application_settings_count = new_application_settings_count
        new_application_settings_count = Session.query(ApplicationSettings).count()
        assert resp['object_language_name'] == 'Updated!'
        assert new_application_settings_count == application_settings_count
        assert response.content_type == 'application/json'
        response = self.app.put(url('applicationsetting', id=id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'the submitted data were not new' in resp['error']
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': 'Updated by a contrib!', 
           'unrestricted_users': [
                                contributor_id], 
           'morpheme_delimiters': '-,='})
        params = json.dumps(params)
        response = self.app.put(url('applicationsetting', id=id), params, self.json_headers, self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'You are not authorized to access this resource.'

    @nottest
    def test_delete(self):
        """Tests that DELETE /applicationsettings/id deletes the application settings with id=id and returns a JSON representation.

        If the id is invalid or unspecified, then JSON null or a 404 status code
        are returned, respectively.
        """
        application_settings_count = Session.query(ApplicationSettings).count()
        orthography1 = h.generate_default_orthography1()
        Session.add(orthography1)
        Session.commit()
        orthography1 = h.get_orthographies()[0]
        orthography1_id = orthography1.id
        orthography1 = Session.query(Orthography).get(orthography1_id)
        params = self.application_settings_create_params.copy()
        params.update({'object_language_name': 'test_delete object language name', 
           'object_language_id': 'tdo', 
           'metalanguage_name': 'test_delete metalanguage name', 
           'metalanguage_id': 'tdm', 
           'storage_orthography': orthography1_id, 
           'morpheme_delimiters': '-'})
        params = json.dumps(params)
        response = self.app.post(url('applicationsettings'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_application_settings_count = Session.query(ApplicationSettings).count()
        assert resp['object_language_name'] == 'test_delete object language name'
        assert new_application_settings_count == application_settings_count + 1
        response = self.app.delete(url('applicationsetting', id=resp['id']), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        new_application_settings_count = Session.query(ApplicationSettings).count()
        assert new_application_settings_count == application_settings_count
        assert response.content_type == 'application/json'
        assert resp['object_language_name'] == 'test_delete object language name'
        deleted_application_settings = Session.query(ApplicationSettings).get(resp['id'])
        assert deleted_application_settings == None
        id = 9999999999999
        response = self.app.delete(url('applicationsetting', id=id), extra_environ=self.extra_environ_admin, status=404)
        assert json.loads(response.body)['error'] == 'There is no application settings with id %s' % id
        assert response.content_type == 'application/json'
        response = self.app.delete(url('applicationsetting', id=''), status=404, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        response = self.app.post(url('applicationsettings'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        application_settings_count = new_application_settings_count
        new_application_settings_count = Session.query(ApplicationSettings).count()
        assert resp['object_language_name'] == 'test_delete object language name'
        assert new_application_settings_count == application_settings_count + 1
        response = self.app.delete(url('applicationsetting', id=resp['id']), headers=self.json_headers, extra_environ=self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'You are not authorized to access this resource.'
        return

    @nottest
    def test_show(self):
        """Tests that GET /applicationsettings/id returns the JSON application settings object with id=id
        or a 404 status code depending on whether the id is valid or
        invalid/unspecified, respectively.
        """
        id = 100000000000
        response = self.app.get(url('applicationsetting', id=id), extra_environ=self.extra_environ_admin, status=404)
        assert json.loads(response.body)['error'] == 'There is no application settings with id %s' % id
        assert response.content_type == 'application/json'
        response = self.app.get(url('applicationsetting', id=''), status=404, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        application_settings = add_default_application_settings()
        application_settings = h.get_application_settings()
        application_settings_id = application_settings.id
        response = self.app.get(url('applicationsetting', id=application_settings_id), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert type(resp) == type({})
        assert resp['object_language_name'] == application_settings.object_language_name
        assert resp['storage_orthography']['name'] == application_settings.storage_orthography.name

    @nottest
    def test_edit(self):
        """Tests that GET /applicationsettings/id/edit returns a JSON object for editing an existing application settings.

        The JSON object is of the form {application_settings: {...}, data: {...}}
        or {'error': '...'} (and a 404 status code) depending on whether the id
        is valid or invalid/unspecified, respectively.
        """
        response = self.app.get(url('edit_applicationsetting', id=100000000000), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 100000000000
        response = self.app.get(url('edit_applicationsetting', id=id), extra_environ=self.extra_environ_admin, status=404)
        assert json.loads(response.body)['error'] == 'There is no application settings with id %s' % id
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_applicationsetting', id=''), status=404, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        application_settings = add_default_application_settings()
        application_settings = h.get_application_settings()
        application_settings_id = application_settings.id
        response = self.app.get(url('edit_applicationsetting', id=application_settings_id), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert type(resp) == type({})
        assert resp['application_settings']['object_language_name'] == application_settings.object_language_name
        data = {'languages': h.get_languages(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'orthographies': h.get_mini_dicts_getter('Orthography')()}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        params = {'users': 'give me some users!', 
           'languages': '', 
           'orthographies': datetime.datetime.utcnow().isoformat()}
        response = self.app.get(url('edit_applicationsetting', id=application_settings_id), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['data']['users'] == data['users']
        assert resp['data']['languages'] == []
        assert resp['data']['orthographies'] == data['orthographies']
        params = {'users': 'True'}
        response = self.app.get(url('edit_applicationsetting', id=id), params, extra_environ=self.extra_environ_admin, status=404)
        assert json.loads(response.body)['error'] == 'There is no application settings with id %s' % id