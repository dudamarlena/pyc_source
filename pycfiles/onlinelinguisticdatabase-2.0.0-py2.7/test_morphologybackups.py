# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_morphologybackups.py
# Compiled at: 2016-09-19 13:27:02
import logging, os, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model import Morphology
from onlinelinguisticdatabase.model.meta import Session
log = logging.getLogger(__name__)

class TestMorphologybackupsController(TestController):

    def __init__(self, *args, **kwargs):
        TestController.__init__(self, *args, **kwargs)

    def tearDown(self):
        TestController.tearDown(self, dirs_to_destroy=['morphology'])

    @nottest
    def test_index(self):
        """Tests that ``GET /morphologybackups`` behaves correctly.
        """
        view = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        contrib = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        admin = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'A description of the corpus'})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        params = self.morphology_create_params.copy()
        params.update({'name': 'Morphology', 
           'description': 'A description of this morphology.', 
           'script_type': 'lexc', 
           'rules_corpus': corpus_id, 
           'extract_morphemes_from_rules_corpus': True})
        params = json.dumps(params)
        response = self.app.post(url('morphologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        morphology_count = Session.query(Morphology).count()
        morphology_dir = os.path.join(self.morphologies_path, 'morphology_%d' % resp['id'])
        morphology_dir_contents = os.listdir(morphology_dir)
        morphology_id = resp['id']
        assert morphology_count == 1
        assert resp['name'] == 'Morphology'
        assert resp['description'] == 'A description of this morphology.'
        assert 'morphology_%d.script' % morphology_id not in morphology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script_type'] == 'lexc'
        assert resp['rules'] == ''
        assert resp['rules_generated'] == None
        assert resp['generate_attempt'] == None
        params = self.morphology_create_params.copy()
        params.update({'name': 'Morphology Renamed', 
           'description': 'A description of this morphology.', 
           'script_type': 'lexc', 
           'rules_corpus': corpus_id, 
           'extract_morphemes_from_rules_corpus': True})
        params = json.dumps(params)
        response = self.app.put(url('morphology', id=morphology_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        morphology_count = Session.query(model.Morphology).count()
        assert response.content_type == 'application/json'
        assert morphology_count == 1
        params = self.morphology_create_params.copy()
        params.update({'name': 'Morphology Renamed by Contributor', 
           'description': 'A description of this morphology.', 
           'script_type': 'lexc', 
           'rules_corpus': corpus_id, 
           'extract_morphemes_from_rules_corpus': True})
        params = json.dumps(params)
        response = self.app.put(url('morphology', id=morphology_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        morphology_count = Session.query(model.Morphology).count()
        assert morphology_count == 1
        response = self.app.get(url('morphologybackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert response.content_type == 'application/json'
        params = self.morphology_create_params.copy()
        params.update({'name': 'Morphology Updated', 
           'description': 'A description of this morphology.', 
           'script_type': 'lexc', 
           'rules_corpus': corpus_id, 
           'extract_morphemes_from_rules_corpus': True})
        params = json.dumps(params)
        response = self.app.put(url('morphology', id=morphology_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        morphology_count = Session.query(model.Morphology).count()
        assert morphology_count == 1
        response = self.app.get(url('morphologybackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        all_morphology_backups = resp
        assert len(resp) == 3
        paginator = {'items_per_page': 1, 'page': 2}
        response = self.app.get(url('morphologybackups'), paginator, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp['items']) == 1
        assert resp['items'][0]['name'] == all_morphology_backups[1]['name']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'MorphologyBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc'}
        response = self.app.get(url('morphologybackups'), order_by_params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        result_set = sorted(all_morphology_backups, key=lambda pb: pb['datetime_modified'], reverse=True)
        assert [ pb['id'] for pb in resp ] == [ pb['id'] for pb in result_set ]
        params = {'order_by_model': 'MorphologyBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('morphologybackups'), params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert result_set[2]['name'] == resp['items'][0]['name']
        response = self.app.get(url('morphologybackup', id=all_morphology_backups[0]['id']), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert resp['name'] == all_morphology_backups[0]['name']
        assert response.content_type == 'application/json'
        response = self.app.get(url('morphologybackup', id=100987), headers=self.json_headers, extra_environ=view, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no morphology backup with id 100987'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_morphologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.get(url('new_morphologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.post(url('morphologybackups'), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.put(url('morphologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.delete(url('morphologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        return