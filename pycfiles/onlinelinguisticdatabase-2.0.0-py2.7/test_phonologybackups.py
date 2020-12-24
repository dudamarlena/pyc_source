# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_phonologybackups.py
# Compiled at: 2016-09-19 13:27:02
import logging, os, codecs, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model import Phonology
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)

class TestPhonologybackupsController(TestController):

    def __init__(self, *args, **kwargs):
        TestController.__init__(self, *args, **kwargs)
        self.test_phonology_script = h.normalize(codecs.open(self.test_phonology_script_path, 'r', 'utf8').read())

    def tearDown(self):
        TestController.tearDown(self, dirs_to_destroy=['phonology'])

    @nottest
    def test_index(self):
        """Tests that ``GET /phonologybackups`` behaves correctly.
        """
        view = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        contrib = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        admin = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_count = Session.query(Phonology).count()
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_id = resp['id']
        assert phonology_count == 1
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        assert 'phonology.script' in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_script
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology Renamed', 
           'description': 'Covers a lot of the data.', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        phonology_count = Session.query(model.Phonology).count()
        assert response.content_type == 'application/json'
        assert phonology_count == 1
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology Renamed by Contributor', 
           'description': 'Covers a lot of the data.', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        phonology_count = Session.query(model.Phonology).count()
        assert phonology_count == 1
        response = self.app.get(url('phonologybackups'), headers=self.json_headers, extra_environ=view)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert response.content_type == 'application/json'
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology Updated', 
           'description': 'Covers a lot of the data.', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        phonology_count = Session.query(model.Phonology).count()
        assert phonology_count == 1
        response = self.app.get(url('phonologybackups'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        all_phonology_backups = resp
        assert len(resp) == 3
        paginator = {'items_per_page': 1, 'page': 2}
        response = self.app.get(url('phonologybackups'), paginator, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert len(resp['items']) == 1
        assert resp['items'][0]['name'] == all_phonology_backups[1]['name']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'PhonologyBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc'}
        response = self.app.get(url('phonologybackups'), order_by_params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        result_set = sorted(all_phonology_backups, key=lambda pb: pb['datetime_modified'], reverse=True)
        assert [ pb['id'] for pb in resp ] == [ pb['id'] for pb in result_set ]
        params = {'order_by_model': 'PhonologyBackup', 'order_by_attribute': 'datetime_modified', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('phonologybackups'), params, headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert result_set[2]['name'] == resp['items'][0]['name']
        response = self.app.get(url('phonologybackup', id=all_phonology_backups[0]['id']), headers=self.json_headers, extra_environ=admin)
        resp = json.loads(response.body)
        assert resp['name'] == all_phonology_backups[0]['name']
        assert response.content_type == 'application/json'
        response = self.app.get(url('phonologybackup', id=100987), headers=self.json_headers, extra_environ=view, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no phonology backup with id 100987'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_phonologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.get(url('new_phonologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.post(url('phonologybackups'), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.put(url('phonologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        response = self.app.delete(url('phonologybackup', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'