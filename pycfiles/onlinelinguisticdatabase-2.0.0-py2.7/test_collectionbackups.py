# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_collectionbackups.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
log = logging.getLogger(__name__)

class TestCollectionbackupsController(TestController):

    def __init__(self, *args, **kwargs):
        TestController.__init__(self, *args, **kwargs)
        self._add_SEARCH_to_web_test_valid_methods()

    @nottest
    def test_index(self):
        """Tests that GET & SEARCH /collectionbackups behave correctly.
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
        contributor_id = [ u for u in users if u.role == 'contributor' ][0].id
        administrator_id = [ u for u in users if u.role == 'administrator' ][0].id
        view = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        contrib = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        admin = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Created by the Contributor', 
           'elicitor': contributor_id, 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, contrib)
        collection_count = Session.query(model.Collection).count()
        resp = json.loads(response.body)
        collection_id = resp['id']
        assert response.content_type == 'application/json'
        assert collection_count == 1
        params = self.collection_create_params.copy()
        params.update({'url': 'find/me/here', 
           'title': 'Updated by the Administrator', 
           'speaker': speaker_id, 
           'tags': tag_ids + [None, ''], 
           'enterer': administrator_id})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert response.content_type == 'application/json'
        assert collection_count == 1
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated by the Contributor', 
           'speaker': speaker_id, 
           'tags': tag_ids, 
           'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert collection_count == 1
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert response.content_type == 'application/json'
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp) == 2
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 0
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated and de-restricted by the Contributor', 
           'speaker': speaker_id, 
           'tags': [], 'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert collection_count == 1
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert len(resp) == 3
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp) == 3
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 0
        assert response.content_type == 'application/json'
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated by the Contributor *again*', 
           'speaker': speaker_id, 
           'tags': [], 'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert collection_count == 1
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert len(resp) == 4
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        all_collection_backups = resp
        assert len(resp) == 4
        response = self.app.get(url('collectionbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        unrestricted_collection_backup = resp[0]
        assert len(resp) == 1
        assert resp[0]['title'] == 'Updated and de-restricted by the Contributor'
        restricted_collection_backups = [ cb for cb in all_collection_backups if cb != unrestricted_collection_backup
                                        ]
        assert len(restricted_collection_backups) == 3
        paginator = {'items_per_page': 1, 'page': 2}
        response = self.app.get(url('collectionbackups'), paginator, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp['items']) == 1
        assert resp['items'][0]['title'] == all_collection_backups[1]['title']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'CollectionBackup', 'order_by_attribute': 'id', 
           'order_by_direction': 'desc'}
        response = self.app.get(url('collectionbackups'), order_by_params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        result_set = sorted(all_collection_backups, key=lambda cb: cb['id'], reverse=True)
        assert [ cb['id'] for cb in resp ] == [ cb['id'] for cb in result_set ]
        params = {'order_by_model': 'CollectionBackup', 'order_by_attribute': 'id', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('collectionbackups'), params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert result_set[2]['title'] == resp['items'][0]['title']
        response = self.app.get(url('collectionbackup', id=restricted_collection_backups[0]['id']), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert resp['title'] == restricted_collection_backups[0]['title']
        assert response.content_type == 'application/json'
        response = self.app.get(url('collectionbackup', id=restricted_collection_backups[0]['id']), headers=self.json_headers, extra_environ=view, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('collectionbackup', id=unrestricted_collection_backup['id']), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert resp['title'] == unrestricted_collection_backup['title']
        response = self.app.get(url('collectionbackup', id=100987), headers=self.json_headers, extra_environ=view, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no collection backup with id 100987'
        assert response.content_type == 'application/json'
        self._add_SEARCH_to_web_test_valid_methods()
        json_query = json.dumps({'query': {'filter': [
                              'CollectionBackup', 'title', 'like', '%Contributor%']}})
        response = self.app.post(url('/collectionbackups/search'), json_query, self.json_headers, admin)
        resp = json.loads(response.body)
        result_set = [ cb for cb in all_collection_backups if 'Contributor' in cb['title'] ]
        assert len(resp) == len(result_set) == 3
        assert set([ cb['id'] for cb in resp ]) == set([ cb['id'] for cb in result_set ])
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'CollectionBackup', 'title', 'like', '%Administrator%']}})
        response = self.app.request(url('collectionbackups'), method='SEARCH', body=json_query, headers=self.json_headers, environ=admin)
        resp = json.loads(response.body)
        result_set = [ cb for cb in all_collection_backups if 'Administrator' in cb['title'] ]
        assert len(resp) == len(result_set) == 1
        assert set([ cb['id'] for cb in resp ]) == set([ cb['id'] for cb in result_set ])
        json_query = json.dumps({'query': {'filter': [
                              'CollectionBackup', 'title', 'like', '%Contributor%']}})
        response = self.app.post(url('/collectionbackups/search'), json_query, self.json_headers, view)
        resp = json.loads(response.body)
        result_set = [ cb for cb in [unrestricted_collection_backup] if 'Contributor' in cb['title']
                     ]
        assert len(resp) == len(result_set) == 1
        assert set([ cb['id'] for cb in resp ]) == set([ cb['id'] for cb in result_set ])
        json_query = json.dumps({'query': {'filter': [
                              'CollectionBackup', 'title', 'like', '%Administrator%']}})
        response = self.app.request(url('collectionbackups'), method='SEARCH', body=json_query, headers=self.json_headers, environ=view)
        resp = json.loads(response.body)
        result_set = [ cb for cb in [unrestricted_collection_backup] if 'Administrator' in cb['title']
                     ]
        assert len(resp) == len(result_set) == 0
        response = self.app.get(url('edit_collectionbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.get(url('new_collectionbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.post(url('collectionbackups'), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.put(url('collectionbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.delete(url('collectionbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_new_search(self):
        """Tests that GET /collectionbackups/new_search returns the search parameters for searching the collection backups resource."""
        query_builder = SQLAQueryBuilder('CollectionBackup')
        response = self.app.get(url('/collectionbackups/new_search'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['search_parameters'] == h.get_search_parameters(query_builder)