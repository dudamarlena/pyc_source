# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_morphemelanguagemodelbackups.py
# Compiled at: 2016-09-19 13:27:02
import logging, os, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model import MorphemeLanguageModel
from onlinelinguisticdatabase.model.meta import Session
log = logging.getLogger(__name__)

class TestMorphemelanguagemodelbackupsController(TestController):

    def __init__(self, *args, **kwargs):
        TestController.__init__(self, *args, **kwargs)

    def tearDown(self):
        TestController.tearDown(self, dirs_to_destroy=['morpheme_language_model'])

    @nottest
    def test_index(self):
        """Tests that ``GET /morphemelanguagemodelbackups`` behaves correctly.
        """
        view = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        contrib = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        admin = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        query = {'filter': ['Form', 'transcription', 'like', '%_%']}
        params = self.form_search_create_params.copy()
        params.update({'name': 'Find anything', 
           'search': query})
        params = json.dumps(params)
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        form_search_id = json.loads(response.body)['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus of sentences', 
           'form_search': form_search_id})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        corpus_id = json.loads(response.body)['id']
        name = 'Morpheme language model'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': name, 
           'corpus': corpus_id, 
           'toolkit': 'mitlm'})
        params = json.dumps(params)
        response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        morpheme_language_model_id = resp['id']
        assert resp['name'] == name
        assert resp['toolkit'] == 'mitlm'
        assert resp['order'] == 3
        assert resp['smoothing'] == ''
        assert resp['restricted'] == False
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': 'Morpheme language model renamed', 
           'corpus': corpus_id, 
           'toolkit': 'mitlm'})
        params = json.dumps(params)
        response = self.app.put(url('morphemelanguagemodel', id=morpheme_language_model_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        morpheme_language_model_count = Session.query(model.MorphemeLanguageModel).count()
        assert response.content_type == 'application/json'
        assert morpheme_language_model_count == 1
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': 'Morpheme language model renamed by contributor', 
           'corpus': corpus_id, 
           'toolkit': 'mitlm'})
        params = json.dumps(params)
        response = self.app.put(url('morphemelanguagemodel', id=morpheme_language_model_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        morpheme_language_model_count = Session.query(MorphemeLanguageModel).count()
        assert morpheme_language_model_count == 1
        response = self.app.get(url('morphemelanguagemodelbackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert response.content_type == 'application/json'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': 'Morpheme language model updated yet again', 
           'corpus': corpus_id, 
           'toolkit': 'mitlm'})
        params = json.dumps(params)
        response = self.app.put(url('morphemelanguagemodel', id=morpheme_language_model_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        morpheme_language_model_count = Session.query(model.MorphemeLanguageModel).count()
        assert morpheme_language_model_count == 1
        response = self.app.get(url('morphemelanguagemodelbackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        all_morpheme_language_model_backups = resp
        assert len(resp) == 3
        paginator = {'items_per_page': 1, 'page': 2}
        response = self.app.get(url('morphemelanguagemodelbackups'), paginator, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp['items']) == 1
        assert resp['items'][0]['name'] == all_morpheme_language_model_backups[1]['name']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'MorphemeLanguageModelBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc'}
        response = self.app.get(url('morphemelanguagemodelbackups'), order_by_params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        result_set = sorted(all_morpheme_language_model_backups, key=lambda pb: pb['datetime_modified'], reverse=True)
        assert [ pb['id'] for pb in resp ] == [ pb['id'] for pb in result_set ]
        params = {'order_by_model': 'MorphemeLanguageModelBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('morphemelanguagemodelbackups'), params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert result_set[2]['name'] == resp['items'][0]['name']
        response = self.app.get(url('morphemelanguagemodelbackup', id=all_morpheme_language_model_backups[0]['id']), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert resp['name'] == all_morpheme_language_model_backups[0]['name']
        assert response.content_type == 'application/json'
        response = self.app.get(url('morphemelanguagemodelbackup', id=100987), headers=self.json_headers, extra_environ=view, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no morpheme language model backup with id 100987'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_morphemelanguagemodelbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.get(url('new_morphemelanguagemodelbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.post(url('morphemelanguagemodelbackups'), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.put(url('morphemelanguagemodelbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.delete(url('morphemelanguagemodelbackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'