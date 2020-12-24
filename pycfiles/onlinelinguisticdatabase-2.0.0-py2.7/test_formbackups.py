# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_formbackups.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
log = logging.getLogger(__name__)

class TestFormbackupsController(TestController):

    @nottest
    def test_index(self):
        """Tests that GET & SEARCH /formbackups behave correctly.
        """
        application_settings = h.generate_default_application_settings()
        source = h.generate_default_source()
        restricted_tag = h.generate_restricted_tag()
        file1 = h.generate_default_file()
        file1.name = 'file1'
        file2 = h.generate_default_file()
        file2.name = 'file2'
        speaker = h.generate_default_speaker()
        Session.add_all([application_settings, source, restricted_tag, file1,
         file2, speaker])
        Session.commit()
        speaker_id = speaker.id
        restricted_tag_id = restricted_tag.id
        tag_ids = [restricted_tag_id]
        file1_id = file1.id
        file2_id = file2.id
        file_ids = [file1_id, file2_id]
        users = h.get_users()
        administrator_id = [ u for u in users if u.role == 'administrator' ][0].id
        view = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        contrib = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        admin = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        params = self.form_create_params.copy()
        params.update({'transcription': 'Created by the Contributor', 
           'translations': [{'transcription': 'test', 'grammaticality': ''}], 'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, contrib)
        form_count = Session.query(model.Form).count()
        resp = json.loads(response.body)
        form_id = resp['id']
        assert form_count == 1
        params = self.form_create_params.copy()
        params.update({'translations': [{'transcription': 'test', 'grammaticality': ''}], 'transcription': 'Updated by the Administrator', 
           'speaker': speaker_id, 
           'tags': tag_ids + [None, ''], 
           'enterer': administrator_id})
        params = json.dumps(params)
        response = self.app.put(url('form', id=form_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        form_count = Session.query(model.Form).count()
        assert form_count == 1
        params = self.form_create_params.copy()
        params.update({'transcription': 'Updated by the Contributor', 
           'translations': [{'transcription': 'test', 'grammaticality': ''}], 'speaker': speaker_id, 
           'tags': tag_ids, 
           'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('form', id=form_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        form_count = Session.query(model.Form).count()
        assert form_count == 1
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert response.content_type == 'application/json'
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 0
        params = self.form_create_params.copy()
        params.update({'transcription': 'Updated and de-restricted by the Contributor', 
           'translations': [{'transcription': 'test', 'grammaticality': ''}], 'speaker': speaker_id, 
           'tags': [], 'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('form', id=form_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        form_count = Session.query(model.Form).count()
        assert form_count == 1
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert len(resp) == 3
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp) == 3
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 0
        params = self.form_create_params.copy()
        params.update({'transcription': 'Updated by the Contributor *again*', 
           'translations': [{'transcription': 'test', 'grammaticality': ''}], 'speaker': speaker_id, 
           'tags': [], 'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('form', id=form_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        form_count = Session.query(model.Form).count()
        assert form_count == 1
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert len(resp) == 4
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        all_form_backups = resp
        assert len(resp) == 4
        response = self.app.get(url('formbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        unrestricted_form_backup = resp[0]
        assert len(resp) == 1
        assert resp[0]['transcription'] == 'Updated and de-restricted by the Contributor'
        restricted_form_backups = [ cb for cb in all_form_backups if cb != unrestricted_form_backup
                                  ]
        assert len(restricted_form_backups) == 3
        paginator = {'items_per_page': 1, 'page': 2}
        response = self.app.get(url('formbackups'), paginator, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp['items']) == 1
        assert resp['items'][0]['transcription'] == all_form_backups[1]['transcription']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'FormBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc'}
        response = self.app.get(url('formbackups'), order_by_params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        result_set = sorted(all_form_backups, key=lambda cb: cb['datetime_modified'], reverse=True)
        assert [ cb['id'] for cb in resp ] == [ cb['id'] for cb in result_set ]
        params = {'order_by_model': 'FormBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('formbackups'), params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert result_set[2]['transcription'] == resp['items'][0]['transcription']
        response = self.app.get(url('formbackup', id=restricted_form_backups[0]['id']), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert resp['transcription'] == restricted_form_backups[0]['transcription']
        assert response.content_type == 'application/json'
        response = self.app.get(url('formbackup', id=restricted_form_backups[0]['id']), headers=self.json_headers, extra_environ=view, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('formbackup', id=unrestricted_form_backup['id']), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert resp['transcription'] == unrestricted_form_backup['transcription']
        response = self.app.get(url('formbackup', id=100987), headers=self.json_headers, extra_environ=view, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no form backup with id 100987'
        assert response.content_type == 'application/json'
        self._add_SEARCH_to_web_test_valid_methods()
        json_query = json.dumps({'query': {'filter': [
                              'FormBackup', 'transcription', 'like', '%Contributor%']}})
        response = self.app.post(url('/formbackups/search'), json_query, self.json_headers, admin)
        resp = json.loads(response.body)
        result_set = [ cb for cb in all_form_backups if 'Contributor' in cb['transcription'] ]
        assert len(resp) == len(result_set) == 3
        assert set([ cb['id'] for cb in resp ]) == set([ cb['id'] for cb in result_set ])
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'FormBackup', 'transcription', 'like', '%Administrator%']}})
        response = self.app.request(url('formbackups'), method='SEARCH', body=json_query, headers=self.json_headers, environ=admin)
        resp = json.loads(response.body)
        result_set = [ cb for cb in all_form_backups if 'Administrator' in cb['transcription'] ]
        assert len(resp) == len(result_set) == 1
        assert set([ cb['id'] for cb in resp ]) == set([ cb['id'] for cb in result_set ])
        json_query = json.dumps({'query': {'filter': [
                              'FormBackup', 'transcription', 'like', '%Contributor%']}})
        response = self.app.post(url('/formbackups/search'), json_query, self.json_headers, view)
        resp = json.loads(response.body)
        result_set = [ cb for cb in [unrestricted_form_backup] if 'Contributor' in cb['transcription']
                     ]
        assert len(resp) == len(result_set) == 1
        assert set([ cb['id'] for cb in resp ]) == set([ cb['id'] for cb in result_set ])
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'FormBackup', 'transcription', 'like', '%Administrator%']}})
        response = self.app.request(url('formbackups'), method='SEARCH', body=json_query, headers=self.json_headers, environ=view)
        resp = json.loads(response.body)
        result_set = [ cb for cb in [unrestricted_form_backup] if 'Administrator' in cb['transcription']
                     ]
        assert len(resp) == len(result_set) == 0
        response = self.app.get(url('edit_formbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.get(url('new_formbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.post(url('formbackups'), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.put(url('formbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.delete(url('formbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_new_search(self):
        """Tests that GET /formbackups/new_search returns the search parameters for searching the form backups resource."""
        query_builder = SQLAQueryBuilder('FormBackup')
        response = self.app.get(url('/formbackups/new_search'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['search_parameters'] == h.get_search_parameters(query_builder)