# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_orthographies.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from time import sleep
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import Orthography
log = logging.getLogger(__name__)

class TestOrthographiesController(TestController):

    @nottest
    def test_index(self):
        """Tests that GET /orthographies returns an array of all orthographies and that order_by and pagination parameters work correctly."""

        def create_orthography_from_index(index):
            orthography = model.Orthography()
            orthography.name = 'orthography%d' % index
            orthography.orthography = 'a, b, c, %d' % index
            orthography.initial_glottal_stops = False
            orthography.lowercase = True
            return orthography

        orthographies = [ create_orthography_from_index(i) for i in range(1, 101) ]
        Session.add_all(orthographies)
        Session.commit()
        orthographies = h.get_orthographies(True)
        orthographies_count = len(orthographies)
        response = self.app.get(url('orthographies'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == orthographies_count
        assert resp[0]['name'] == 'orthography1'
        assert resp[0]['id'] == orthographies[0].id
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('orthographies'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['name'] == orthographies[46].name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Orthography', 'order_by_attribute': 'name', 'order_by_direction': 'desc'}
        response = self.app.get(url('orthographies'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted([ o.name for o in orthographies ], reverse=True)
        assert result_set == [ o['name'] for o in resp ]
        params = {'order_by_model': 'Orthography', 'order_by_attribute': 'name', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('orthographies'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert result_set[46] == resp['items'][0]['name']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Orthography', 'order_by_attribute': 'name', 'order_by_direction': 'descending'}
        response = self.app.get(url('orthographies'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Orthographyist', 'order_by_attribute': 'nominal', 'order_by_direction': 'desc'}
        response = self.app.get(url('orthographies'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == orthographies[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('orthographies'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('orthographies'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /orthographies creates a new orthography
        or returns an appropriate error if the input is invalid.
        """
        original_orthography_count = Session.query(Orthography).count()
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography 1', 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_orthography_count = Session.query(Orthography).count()
        assert new_orthography_count == original_orthography_count + 1
        assert resp['name'] == 'orthography 1'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == False
        assert resp['initial_glottal_stops'] == True
        assert response.content_type == 'application/json'
        params = self.orthography_create_params.copy()
        params.update({'name': '', 'orthography': ''})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'Please enter a value'
        assert resp['errors']['orthography'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography' * 200, 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography 2', 
           'orthography': 'a, b, c', 
           'initial_glottal_stops': False, 
           'lowercase': True})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        orthography_count = new_orthography_count
        new_orthography_count = Session.query(Orthography).count()
        assert new_orthography_count == orthography_count + 1
        assert resp['name'] == 'orthography 2'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == True
        assert resp['initial_glottal_stops'] == False
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography 3', 
           'orthography': 'a, b, c', 
           'initial_glottal_stops': 'FALSE', 
           'lowercase': 'truE'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        orthography_count = new_orthography_count
        new_orthography_count = Session.query(Orthography).count()
        assert new_orthography_count == orthography_count + 1
        assert resp['name'] == 'orthography 3'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == True
        assert resp['initial_glottal_stops'] == False
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography 4', 
           'orthography': 'a, b, c', 
           'initial_glottal_stops': 'negative', 
           'lowercase': 'althaea'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['lowercase'] == "Value should be 'true' or 'false'"
        assert resp['errors']['initial_glottal_stops'] == "Value should be 'true' or 'false'"

    @nottest
    def test_new(self):
        """Tests that GET /orthographies/new returns an empty JSON object."""
        response = self.app.get(url('new_orthography'), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp == {}
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /orthographies/id updates the orthography with id=id."""
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        orthography_count = Session.query(Orthography).count()
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == False
        assert resp['initial_glottal_stops'] == True
        assert response.content_type == 'application/json'
        orthography_id = resp['id']
        original_datetime_modified = resp['datetime_modified']
        sleep(1)
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c, d'})
        params = json.dumps(params)
        response = self.app.put(url('orthography', id=orthography_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        datetime_modified = resp['datetime_modified']
        new_orthography_count = Session.query(Orthography).count()
        assert orthography_count == new_orthography_count
        assert datetime_modified != original_datetime_modified
        assert resp['orthography'] == 'a, b, c, d'
        assert response.content_type == 'application/json'
        sleep(1)
        response = self.app.put(url('orthography', id=orthography_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        orthography_count = new_orthography_count
        new_orthography_count = Session.query(Orthography).count()
        our_orthography_datetime_modified = Session.query(Orthography).get(orthography_id).datetime_modified
        assert our_orthography_datetime_modified.isoformat() == datetime_modified
        assert orthography_count == new_orthography_count
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'
        app_set = h.generate_default_application_settings()
        app_set.storage_orthography = Session.query(Orthography).get(orthography_id)
        Session.add(app_set)
        Session.commit()
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c, d, e'})
        params = json.dumps(params)
        response = self.app.put(url('orthography', id=orthography_id), params, self.json_headers, self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'Only administrators are permitted to update orthographies that are used in the active application settings.'
        assert response.content_type == 'application/json'
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c, d, e'})
        params = json.dumps(params)
        response = self.app.put(url('orthography', id=orthography_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c, d, e'
        assert response.content_type == 'application/json'
        app_set = h.get_application_settings()
        app_set.storage_orthography = None
        Session.commit()
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c, d, e, f'})
        params = json.dumps(params)
        response = self.app.put(url('orthography', id=orthography_id), params, self.json_headers, self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c, d, e, f'
        return

    @nottest
    def test_delete(self):
        """Tests that DELETE /orthographies/id deletes the orthography with id=id."""
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        orthography_count = Session.query(Orthography).count()
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == False
        assert resp['initial_glottal_stops'] == True
        orthography_id = resp['id']
        original_datetime_modified = resp['datetime_modified']
        response = self.app.delete(url('orthography', id=orthography_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        new_orthography_count = Session.query(Orthography).count()
        assert new_orthography_count == orthography_count - 1
        assert resp['id'] == orthography_id
        assert response.content_type == 'application/json'
        deleted_orthography = Session.query(Orthography).get(orthography_id)
        assert deleted_orthography == None
        id = 9999999999999
        response = self.app.delete(url('orthography', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no orthography with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('orthography', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        orthography_count = Session.query(Orthography).count()
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == False
        assert resp['initial_glottal_stops'] == True
        orthography_id = resp['id']
        app_set = h.generate_default_application_settings()
        app_set.storage_orthography = Session.query(Orthography).get(orthography_id)
        Session.add(app_set)
        Session.commit()
        response = self.app.delete(url('orthography', id=orthography_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'Only administrators are permitted to delete orthographies that are used in the active application settings.'
        assert response.content_type == 'application/json'
        app_set = h.get_application_settings()
        app_set.storage_orthography = None
        Session.commit()
        response = self.app.delete(url('orthography', id=orthography_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['orthography'] == 'a, b, c'
        return

    @nottest
    def test_show(self):
        """Tests that GET /orthographies/id returns the orthography with id=id or an appropriate error."""
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == False
        assert resp['initial_glottal_stops'] == True
        orthography_id = resp['id']
        id = 100000000000
        response = self.app.get(url('orthography', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no orthography with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('orthography', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('orthography', id=orthography_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c'
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /orthographies/id/edit returns a JSON object of data necessary to edit the orthography with id=id.

        The JSON object is of the form {'orthography': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        params = self.orthography_create_params.copy()
        params.update({'name': 'orthography', 'orthography': 'a, b, c'})
        params = json.dumps(params)
        response = self.app.post(url('orthographies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'orthography'
        assert resp['orthography'] == 'a, b, c'
        assert resp['lowercase'] == False
        assert resp['initial_glottal_stops'] == True
        orthography_id = resp['id']
        response = self.app.get(url('edit_orthography', id=orthography_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_orthography', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no orthography with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_orthography', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        response = self.app.get(url('edit_orthography', id=orthography_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['orthography']['name'] == 'orthography'
        assert resp['orthography']['orthography'] == 'a, b, c'
        assert resp['data'] == {}
        assert response.content_type == 'application/json'