# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_phonologies.py
# Compiled at: 2016-09-19 13:27:02
import logging, os, codecs, simplejson as json
from uuid import uuid4
from time import sleep
from nose.tools import nottest
from sqlalchemy.sql import desc
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import Phonology, PhonologyBackup
log = logging.getLogger(__name__)

class TestPhonologiesController(TestController):

    def __init__(self, *args, **kwargs):
        TestController.__init__(self, *args, **kwargs)
        self.test_phonology_script = h.normalize(codecs.open(self.test_phonology_script_path, 'r', 'utf8').read())
        self.test_malformed_phonology_script = h.normalize(codecs.open(self.test_malformed_phonology_script_path, 'r', 'utf8').read())
        self.test_phonology_no_phonology_script = h.normalize(codecs.open(self.test_phonology_no_phonology_script_path, 'r', 'utf8').read())
        self.test_medium_phonology_script = h.normalize(codecs.open(self.test_medium_phonology_script_path, 'r', 'utf8').read())
        self.test_large_phonology_script = h.normalize(codecs.open(self.test_large_phonology_script_path, 'r', 'utf8').read())
        self.test_phonology_testless_script = h.normalize(codecs.open(self.test_phonology_testless_script_path, 'r', 'utf8').read())

    def tearDown(self):
        TestController.tearDown(self, del_global_app_set=True, dirs_to_destroy=[
         'user', 'phonology'])

    @nottest
    def test_index(self):
        """Tests that GET /phonologies returns an array of all phonologies and that order_by and pagination parameters work correctly."""

        def create_phonology_from_index(index, parent, boundary):
            phonology = model.Phonology(parent, boundary=boundary)
            phonology.name = 'Phonology %d' % index
            phonology.description = 'A phonology with %d rules' % index
            phonology.script = '# After this comment, the script will begin.\n\n'
            return phonology

        phonologies_path = self.phonologies_path
        boundary = h.word_boundary_symbol
        phonologies = [ create_phonology_from_index(i, phonologies_path, boundary) for i in range(1, 101)
                      ]
        Session.add_all(phonologies)
        Session.commit()
        phonologies = h.get_phonologies(True)
        phonologies_count = len(phonologies)
        response = self.app.get(url('phonologies'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == phonologies_count
        assert resp[0]['name'] == 'Phonology 1'
        assert resp[0]['id'] == phonologies[0].id
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('phonologies'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['name'] == phonologies[46].name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Phonology', 'order_by_attribute': 'name', 'order_by_direction': 'desc'}
        response = self.app.get(url('phonologies'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted(phonologies, key=lambda p: p.name, reverse=True)
        assert [ p.id for p in result_set ] == [ p['id'] for p in resp ]
        assert response.content_type == 'application/json'
        params = {'order_by_model': 'Phonology', 'order_by_attribute': 'name', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('phonologies'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert result_set[46].name == resp['items'][0]['name']
        order_by_params = {'order_by_model': 'Phonology', 'order_by_attribute': 'name', 'order_by_direction': 'descending'}
        response = self.app.get(url('phonologies'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Phonologyist', 'order_by_attribute': 'nominal', 'order_by_direction': 'desc'}
        response = self.app.get(url('phonologies'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == phonologies[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('phonologies'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('phonologies'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /phonologies creates a new phonology
        or returns an appropriate error if the input is invalid.
        """
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_view, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        original_phonology_count = Session.query(Phonology).count()
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_phonology_count = Session.query(Phonology).count()
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        assert new_phonology_count == original_phonology_count + 1
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        assert 'phonology.script' in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_script
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': '# The rules will begin after this comment.\n\n'})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        phonology_count = new_phonology_count
        new_phonology_count = Session.query(Phonology).count()
        assert new_phonology_count == phonology_count
        assert resp['errors']['name'] == 'The submitted value for Phonology.name is not unique.'
        assert response.content_type == 'application/json'
        params = self.phonology_create_params.copy()
        params.update({'name': '', 
           'description': 'Covers a lot of the data.', 
           'script': '# The rules will begin after this comment.\n\n'})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        phonology_count = new_phonology_count
        new_phonology_count = Session.query(Phonology).count()
        assert new_phonology_count == phonology_count
        assert resp['errors']['name'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        params = self.phonology_create_params.copy()
        params.update({'name': None, 
           'description': 'Covers a lot of the data.', 
           'script': '# The rules will begin after this comment.\n\n'})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        phonology_count = new_phonology_count
        new_phonology_count = Session.query(Phonology).count()
        assert new_phonology_count == phonology_count
        assert resp['errors']['name'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology' * 200, 
           'description': 'Covers a lot of the data.', 
           'script': '# The rules will begin after this comment.\n\n'})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        phonology_count = new_phonology_count
        new_phonology_count = Session.query(Phonology).count()
        assert new_phonology_count == phonology_count
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_new(self):
        """Tests that GET /phonologies/new returns an empty JSON object."""
        response = self.app.get(url('new_phonology'), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp == {}
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /phonologies/id updates the phonology with id=id."""
        original_phonology_count = Session.query(Phonology).count()
        params = self.phonology_create_params.copy()
        original_script = '# The rules will begin after this comment.\n\n'
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': original_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_count = Session.query(Phonology).count()
        phonology_id = resp['id']
        original_datetime_modified = resp['datetime_modified']
        assert phonology_count == original_phonology_count + 1
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        sleep(1)
        new_script = 'define phonology o -> 0 || t "-" _ k "-";'
        orig_backup_count = Session.query(PhonologyBackup).count()
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.  Best yet!', 
           'script': new_script})
        params = json.dumps(params)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_backup_count = Session.query(PhonologyBackup).count()
        datetime_modified = resp['datetime_modified']
        new_phonology_count = Session.query(Phonology).count()
        assert phonology_count == new_phonology_count
        assert datetime_modified != original_datetime_modified
        assert resp['description'] == 'Covers a lot of the data.  Best yet!'
        assert resp['script'] == new_script
        assert response.content_type == 'application/json'
        assert orig_backup_count + 1 == new_backup_count
        backup = Session.query(PhonologyBackup).filter(PhonologyBackup.UUID == unicode(resp['UUID'])).order_by(desc(PhonologyBackup.id)).first()
        assert backup.datetime_modified.isoformat() == original_datetime_modified
        assert backup.script == original_script
        assert response.content_type == 'application/json'
        sleep(1)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        phonology_count = new_phonology_count
        new_phonology_count = Session.query(Phonology).count()
        our_phonology_datetime_modified = Session.query(Phonology).get(phonology_id).datetime_modified
        assert our_phonology_datetime_modified.isoformat() == datetime_modified
        assert phonology_count == new_phonology_count
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'

    @nottest
    def test_delete(self):
        """Tests that DELETE /phonologies/id deletes the phonology with id=id."""
        phonology_count = Session.query(Phonology).count()
        phonology_backup_count = Session.query(PhonologyBackup).count()
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_id = resp['id']
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        assert 'phonology.script' in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_script
        new_phonology_count = Session.query(Phonology).count()
        new_phonology_backup_count = Session.query(PhonologyBackup).count()
        assert new_phonology_count == phonology_count + 1
        assert new_phonology_backup_count == phonology_backup_count
        response = self.app.delete(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_count = new_phonology_count
        new_phonology_count = Session.query(Phonology).count()
        phonology_backup_count = new_phonology_backup_count
        new_phonology_backup_count = Session.query(PhonologyBackup).count()
        assert new_phonology_count == phonology_count - 1
        assert new_phonology_backup_count == phonology_backup_count + 1
        assert resp['id'] == phonology_id
        assert response.content_type == 'application/json'
        assert not os.path.exists(phonology_dir)
        assert resp['script'] == self.test_phonology_script
        deleted_phonology = Session.query(Phonology).get(phonology_id)
        assert deleted_phonology == None
        backed_up_phonology = Session.query(PhonologyBackup).filter(PhonologyBackup.UUID == unicode(resp['UUID'])).first()
        assert backed_up_phonology.name == resp['name']
        modifier = json.loads(unicode(backed_up_phonology.modifier))
        assert modifier['first_name'] == 'Admin'
        assert backed_up_phonology.datetime_entered.isoformat() == resp['datetime_entered']
        assert backed_up_phonology.UUID == resp['UUID']
        id = 9999999999999
        response = self.app.delete(url('phonology', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no phonology with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('phonology', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_show(self):
        """Tests that GET /phonologies/id returns the phonology with id=id or an appropriate error."""
        original_phonology_count = Session.query(Phonology).count()
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': '# The rules will begin after this comment.\n\n'})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_count = Session.query(Phonology).count()
        phonology_id = resp['id']
        assert phonology_count == original_phonology_count + 1
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        id = 100000000000
        response = self.app.get(url('phonology', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no phonology with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('phonology', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        assert resp['script'] == '# The rules will begin after this comment.\n\n'
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /phonologies/id/edit returns a JSON object of data necessary to edit the phonology with id=id.

        The JSON object is of the form {'phonology': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        original_phonology_count = Session.query(Phonology).count()
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': '# The rules will begin after this comment.\n\n'})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_count = Session.query(Phonology).count()
        phonology_id = resp['id']
        assert phonology_count == original_phonology_count + 1
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        response = self.app.get(url('edit_phonology', id=phonology_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_phonology', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no phonology with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_phonology', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['phonology']['name'] == 'Phonology'
        assert resp['data'] == {}
        assert response.content_type == 'application/json'

    @nottest
    def test_compile(self):
        """Tests that PUT /phonologies/id/compile compiles the foma script of the phonology with id.

        .. note::

            Phonology compilation is accomplished via a worker thread and
            requests to /phonologies/id/compile return immediately.  When the
            script compilation attempt has terminated, the values of the
            ``compile_attempt``, ``datetime_modified``, ``compile_succeeded``,
            ``compile_message`` and ``modifier`` attributes of the phonology are
            updated.  Therefore, the tests must poll ``GET /phonologies/id``
            in order to know when the compilation-tasked worker has finished.

        .. note::

            Depending on system resources, the following tests may fail.  A fast
            system may compile the large FST in under 30 seconds; a slow one may
            fail to compile the medium one in under 30.

        Backups

        """
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology1_id = resp['id']
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id)
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_script
        assert resp['modifier']['role'] == 'administrator'
        response = h.foma_installed(force_check=True) or self.app.put(url(controller='phonologies', action='compile', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib, status=400)
        resp = json.loads(response.body)
        if not resp['error'] == 'Foma and flookup are not installed.':
            raise AssertionError
            return
        response = self.app.get(url(controller='phonologies', action='servecompiled', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'Phonology %d has not been compiled yet.' % phonology1_id
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        while True:
            response = self.app.get(url('phonology', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology1_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology1_id)
            sleep(1)

        phonology_dir_contents = os.listdir(phonology_dir)
        assert resp['compile_succeeded'] == True
        assert resp['compile_message'] == 'Compilation process terminated successfully and new binary file was written.'
        assert phonology_binary_filename in phonology_dir_contents
        assert resp['modifier']['role'] == 'contributor'
        response = self.app.get(url(controller='phonologies', action='servecompiled', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        phonology_binary_path = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id, 'phonology.foma')
        foma_file = open(phonology_binary_path, 'rb')
        foma_file_content = foma_file.read()
        assert foma_file_content == response.body
        assert response.content_type == 'application/octet-stream'
        response = self.app.get(url(controller='phonologies', action='servecompiled', id=123456789), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no phonology with id 123456789'
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 2', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_malformed_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_id = resp['id']
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology 2'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_malformed_phonology_script
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        assert resp['id'] == phonology_id
        while True:
            response = self.app.get(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology_id)
            sleep(1)

        assert resp['compile_succeeded'] == False
        assert resp['compile_message'].startswith('Foma script is not a well-formed phonology')
        assert phonology_binary_filename not in os.listdir(phonology_dir)
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 3', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_phonology_no_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_id = resp['id']
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology 3'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_no_phonology_script
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        assert resp['id'] == phonology_id
        while True:
            response = self.app.get(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology_id)
            sleep(1)

        assert resp['compile_succeeded'] == False
        assert resp['compile_message'].startswith('Foma script is not a well-formed phonology')
        assert phonology_binary_filename not in os.listdir(phonology_dir)
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 4', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': ''})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_id = resp['id']
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology 4'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == ''
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        assert resp['id'] == phonology_id
        while True:
            response = self.app.get(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology_id)
            sleep(1)

        assert resp['compile_succeeded'] == False
        assert resp['compile_message'].startswith('Foma script is not a well-formed phonology')
        assert phonology_binary_filename not in os.listdir(phonology_dir)
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 5', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_medium_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_id = resp['id']
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology 5'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_medium_phonology_script
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        assert resp['id'] == phonology_id
        while True:
            response = self.app.get(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology_id)
            sleep(3)

        assert resp['compile_succeeded'] == True
        assert resp['compile_message'] == 'Compilation process terminated successfully and new binary file was written.'
        assert phonology_binary_filename in os.listdir(phonology_dir)
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 6', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_large_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % resp['id'])
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_id = resp['id']
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology 6'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_large_phonology_script
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        assert resp['id'] == phonology_id
        while True:
            response = self.app.get(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology_id)
            sleep(3)

        assert resp['compile_succeeded'] == False
        assert resp['compile_message'].startswith('Foma script is not a well-formed phonology')
        assert phonology_binary_filename not in os.listdir(phonology_dir)
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_binary_filename = 'phonology.foma'
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id)
        compile_attempt = resp['compile_attempt']
        while True:
            response = self.app.get(url('phonology', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology1_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology1_id)
            sleep(1)

        assert resp['compile_succeeded'] == True
        assert resp['compile_message'] == 'Compilation process terminated successfully and new binary file was written.'
        assert phonology_binary_filename in os.listdir(phonology_dir)

    @nottest
    def test_applydown(self):
        """Tests that ``GET /phonologies/id/applydown`` phonologizes input morpho-phonemic segmentations.

        """
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology1_id = resp['id']
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id)
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_script
        assert resp['modifier']['role'] == 'administrator'
        params = h.foma_installed(force_check=True) or json.dumps({'transcriptions': 'nit-wa'})
        response = self.app.put(url(controller='phonologies', action='applydown', id=phonology1_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        if not resp['error'] == 'Foma and flookup are not installed.':
            raise AssertionError
            return
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        while True:
            response = self.app.get(url('phonology', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology1_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology1_id)
            sleep(1)

        assert resp['compile_succeeded'] == True
        assert resp['compile_message'] == 'Compilation process terminated successfully and new binary file was written.'
        assert phonology_binary_filename in os.listdir(phonology_dir)
        assert resp['modifier']['role'] == 'contributor'
        params = json.dumps({'transcriptions': 'nit-wa'})
        response = self.app.put(url(controller='phonologies', action='applydown', id=phonology1_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_dir_path = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id)
        phonology_dir_contents = os.listdir(phonology_dir_path)
        assert resp['nit-wa'] == ['nita']
        assert not [ fn for fn in phonology_dir_contents if fn[:7] == 'inputs_' ]
        assert not [ fn for fn in phonology_dir_contents if fn[:8] == 'outputs_' ]
        assert not [ fn for fn in phonology_dir_contents if fn[:10] == 'applydown_' ]
        params = json.dumps({'transcriptions': 'nit-wa'})
        response = self.app.put(url('/phonologies/%d/phonologize' % phonology1_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['nit-wa'] == ['nita']
        tests = {'nit-waanIt-k-wa': [
                             'nitaanikka'], 
           'nit-waanIt-aa-wa': [
                              'nitaanistaawa'], 
           'nit-siksipawa': [
                           'nitssiksipawa'], 
           'nit-ssikópii': [
                           'nitsssikópii'], 
           'á-sínaaki-wa': [
                            'áísínaakiwa'], 
           'nikáá-ssikópii': [
                               'nikáíssikópii'], 
           "káta'-simi-wa": [
                            "kátai'simiwa"], 
           'áak-oto-apinnii-wa': [
                                 'áakotaapinniiwa',
                                 'áakotapinniiwa'], 
           'w-ínni': [
                     'ónni'], 
           'w-iihsíssi': [
                         'ohsíssi'], 
           'áak-Ipiima': [
                         'áaksipiima'], 
           "kitsí'powata-oaawa": [
                                 "kitsí'powatawaawa"], 
           "á-Io'kaa-wa": [
                          "áyo'kaawa"], 
           'yaatóó-t': [
                        'aatóót'], 
           'waaníí-t': [
                        'aaníít'], 
           "w-óko'si": [
                       "óko'si"], 
           "á-yo'kaa-o'pa": [
                            "áyo'kao'pa"], 
           'imitáá-iksi': [
                           'imitáíksi'], 
           "á-yo'kaa-yi-aawa": [
                               "áyo'kaayaawa"], 
           "á-ihpiyi-o'pa": [
                            "áíhpiyo'pa"], 
           'á-okstaki-yi-aawa': [
                                'áókstakiiyaawa',
                                'áókstakiyaawa'], 
           "á-okska'si-o'pa": [
                              "áókska'so'pa"], 
           'nit-Ioyi': [
                      'nitsoyi'], 
           "otokska'si-hsi": [
                            "otokska'ssi"], 
           "otá'po'taki-hsi": [
                              "otá'po'takssi"], 
           'pii-hsini': [
                       'pissini'], 
           'áak-yaatoowa': [
                           'áakaatoowa'], 
           'nit-waanii': [
                        'nitaanii'], 
           "kikáta'-waaniihpa": [
                                "kikáta'waaniihpa"], 
           'áíhpiyi-yináyi': [
                               'áíhpiiyináyi',
                               'áíhpiyiyináyi'], 
           "áókska'si-hpinnaan": [
                                  "áókska'sspinnaan"], 
           'nit-it-itsiniki': [
                             'nitsitsitsiniki'], 
           "á'-omai'taki-wa": [
                              "áó'mai'takiwa"], 
           "káta'-ookaawaatsi": [
                                'kátaookaawaatsi'], 
           "káta'-ottakiwaatsi": [
                                 'kátaoottakiwaatsi'], 
           "á'-isttohkohpiy'ssi": [
                                  "áíisttohkohpiy'ssi"], 
           "á'-o'tooyiniki": [
                             "áó'tooyiniki"], 
           "káta'-ohto'toowa": [
                               "kátao'ohto'toowa",
                               "kátaohto'toowa"], 
           'nit-ssksinoawa': [
                            'nitssksinoawa'], 
           "á-okska'siwa": [
                           "áókska'siwa"], 
           'atsikí-istsi': [
                           'atsikíístsi'], 
           'kakkóó-iksi': [
                           'kakkóíksi'], 
           'nit-ihpiyi': [
                        'nitsspiyi'], 
           'sa-oht-yi': [
                       'saohtsi'], 
           "nit-yo'kaa": [
                        "nitso'kaa"], 
           "nit-áak-yo'kaa": [
                             "nitáakso'kaa"], 
           'nit-áak-ooyi': [
                           'nitáaksoyi'], 
           'nit-ooyi': [
                      'nitsoyi'], 
           'ooyi': [
                  'iiyi'], 
           'nit-yooht-wa': [
                          'nitoohtowa'], 
           'nit-yooht-o-aa': [
                            'nitsííyoohtoaa'], 
           'nit-yáapi': [
                        'nitsaapi', 'nitsíaapi']}
        params = json.dumps({'transcriptions': tests.keys()})
        response = self.app.put(url(controller='phonologies', action='applydown', id=phonology1_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert set(resp.keys()) == set(tests.keys())
        assert bool(set(resp['áak-yaatoowa']) & set(tests['áak-yaatoowa']))
        params = json.dumps({'transcriptions': []})
        response = self.app.put(url(controller='phonologies', action='applydown', id=phonology1_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['transcriptions'] == 'Please enter a value'
        params = json.dumps({'transcriptions': ['nit-wa']})[:-2]
        response = self.app.put(url(controller='phonologies', action='applydown', id=phonology1_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp == h.JSONDecodeErrorResponse
        params = json.dumps({'transcriptions': 'nit-wa'})
        response = self.app.put(url(controller='phonologies', action='applydown', id=123456789), params, self.json_headers, self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no phonology with id 123456789'
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 2', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology2_id = resp['id']
        params = json.dumps({'transcriptions': 'nit-wa'})
        response = self.app.put(url(controller='phonologies', action='applydown', id=phonology2_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'Phonology %d has not been compiled yet.' % phonology2_id

    @nottest
    def test_runtests(self):
        """Tests that ``GET /phonologies/id/runtests`` runs the tests in the phonology's script."""
        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_phonology_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology1_id = resp['id']
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id)
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_script
        assert resp['modifier']['role'] == 'administrator'
        response = h.foma_installed(force_check=True) or self.app.get(url(controller='phonologies', action='runtests', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        if not resp['error'] == 'Foma and flookup are not installed.':
            raise AssertionError
            return
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        compile_succeeded = resp['compile_succeeded']
        compile_message = resp['compile_message']
        while True:
            response = self.app.get(url('phonology', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology1_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology1_id)
            sleep(1)

        assert resp['compile_succeeded'] == True
        assert resp['compile_message'] == 'Compilation process terminated successfully and new binary file was written.'
        assert phonology_binary_filename in os.listdir(phonology_dir)
        assert resp['modifier']['role'] == 'contributor'
        response = self.app.get(url(controller='phonologies', action='runtests', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp.keys()
        assert 'expected' in resp.values()[0] and 'actual' in resp.values()[0]
        correct = total = 0
        incorrect = []
        for t in resp:
            for e in resp[t]['expected']:
                if e in resp[t]['actual']:
                    correct = correct + 1
                else:
                    incorrect.append((t, e))
                total = total + 1

        log.debug('%d/%d phonology tests passed (%0.2f%s)' % (
         correct, total, 100 * (correct / float(total)), '%'))
        for t, e in incorrect:
            log.debug('%s expected to be %s but phonology returned %s' % (
             t, e, (', ').join(resp[t]['actual'])))

        params = self.phonology_create_params.copy()
        params.update({'name': 'Blackfoot Phonology 2', 
           'description': 'The phonological rules of Frantz (1997) as FSTs', 
           'script': self.test_phonology_testless_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology1_id = resp['id']
        phonology_dir = os.path.join(self.phonologies_path, 'phonology_%d' % phonology1_id)
        phonology_dir_contents = os.listdir(phonology_dir)
        phonology_binary_filename = 'phonology.foma'
        assert resp['name'] == 'Blackfoot Phonology 2'
        assert 'phonology.script' in phonology_dir_contents
        assert 'phonology.sh' in phonology_dir_contents
        assert phonology_binary_filename not in phonology_dir_contents
        assert response.content_type == 'application/json'
        assert resp['script'] == self.test_phonology_testless_script
        assert resp['modifier']['role'] == 'administrator'
        response = self.app.put(url(controller='phonologies', action='compile', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        compile_attempt = resp['compile_attempt']
        while True:
            response = self.app.get(url('phonology', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
            resp = json.loads(response.body)
            if compile_attempt != resp['compile_attempt']:
                log.debug('Compile attempt for phonology %d has terminated.' % phonology1_id)
                break
            else:
                log.debug('Waiting for phonology %d to compile ...' % phonology1_id)
            sleep(1)

        assert resp['compile_succeeded'] == True
        assert resp['compile_message'] == 'Compilation process terminated successfully and new binary file was written.'
        assert phonology_binary_filename in os.listdir(phonology_dir)
        assert resp['modifier']['role'] == 'contributor'
        response = self.app.get(url(controller='phonologies', action='runtests', id=phonology1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The script of phonology %d contains no tests.' % phonology1_id

    @nottest
    def test_history(self):
        """Tests that GET /phonologies/id/history returns the phonology with id=id and its previous incarnations.

        The JSON object returned is of the form
        {'phonology': phonology, 'previous_versions': [...]}.

        """
        users = h.get_users()
        contributor_id = [ u for u in users if u.role == 'contributor' ][0].id
        administrator_id = [ u for u in users if u.role == 'administrator' ][0].id
        original_phonology_count = Session.query(Phonology).count()
        params = self.phonology_create_params.copy()
        original_script = '# The rules will begin after this comment.\n\n'
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.', 
           'script': original_script})
        params = json.dumps(params)
        response = self.app.post(url('phonologies'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        phonology_count = Session.query(Phonology).count()
        phonology_id = resp['id']
        original_datetime_modified = resp['datetime_modified']
        assert phonology_count == original_phonology_count + 1
        assert resp['name'] == 'Phonology'
        assert resp['description'] == 'Covers a lot of the data.'
        sleep(1)
        new_script = 'define phonology o -> 0 || t "-" _ k "-";'
        orig_backup_count = Session.query(PhonologyBackup).count()
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers a lot of the data.  Best yet!', 
           'script': new_script})
        params = json.dumps(params)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_backup_count = Session.query(PhonologyBackup).count()
        first_update_datetime_modified = datetime_modified = resp['datetime_modified']
        new_phonology_count = Session.query(Phonology).count()
        assert phonology_count == new_phonology_count
        assert datetime_modified != original_datetime_modified
        assert resp['description'] == 'Covers a lot of the data.  Best yet!'
        assert resp['script'] == new_script
        assert response.content_type == 'application/json'
        assert orig_backup_count + 1 == new_backup_count
        backup = Session.query(PhonologyBackup).filter(PhonologyBackup.UUID == unicode(resp['UUID'])).order_by(desc(PhonologyBackup.id)).first()
        assert backup.datetime_modified.isoformat() == original_datetime_modified
        assert backup.script == original_script
        assert json.loads(backup.modifier)['first_name'] == 'Admin'
        assert response.content_type == 'application/json'
        sleep(1)
        newest_script = 'define phonology o -> 0 || k "-" _ k "-";'
        orig_backup_count = Session.query(PhonologyBackup).count()
        params = self.phonology_create_params.copy()
        params.update({'name': 'Phonology', 
           'description': 'Covers even more data.  Better than ever!', 
           'script': newest_script})
        params = json.dumps(params)
        response = self.app.put(url('phonology', id=phonology_id), params, self.json_headers, self.extra_environ_contrib)
        resp = json.loads(response.body)
        backup_count = new_backup_count
        new_backup_count = Session.query(PhonologyBackup).count()
        datetime_modified = resp['datetime_modified']
        new_phonology_count = Session.query(Phonology).count()
        assert phonology_count == new_phonology_count == 1
        assert datetime_modified != original_datetime_modified
        assert resp['description'] == 'Covers even more data.  Better than ever!'
        assert resp['script'] == newest_script
        assert resp['modifier']['id'] == contributor_id
        assert response.content_type == 'application/json'
        assert backup_count + 1 == new_backup_count
        backup = Session.query(PhonologyBackup).filter(PhonologyBackup.UUID == unicode(resp['UUID'])).order_by(desc(PhonologyBackup.id)).first()
        assert backup.datetime_modified.isoformat() == first_update_datetime_modified
        assert backup.script == new_script
        assert json.loads(backup.modifier)['first_name'] == 'Admin'
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        response = self.app.get(url(controller='phonologies', action='history', id=phonology_id), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert 'phonology' in resp
        assert 'previous_versions' in resp
        first_version = resp['previous_versions'][1]
        second_version = resp['previous_versions'][0]
        current_version = resp['phonology']
        assert first_version['name'] == 'Phonology'
        assert first_version['description'] == 'Covers a lot of the data.'
        assert first_version['enterer']['id'] == administrator_id
        assert first_version['modifier']['id'] == administrator_id
        assert first_version['datetime_modified'] <= second_version['datetime_modified']
        assert second_version['name'] == 'Phonology'
        assert second_version['description'] == 'Covers a lot of the data.  Best yet!'
        assert second_version['script'] == new_script
        assert second_version['enterer']['id'] == administrator_id
        assert second_version['modifier']['id'] == administrator_id
        assert second_version['datetime_modified'] <= current_version['datetime_modified']
        assert current_version['name'] == 'Phonology'
        assert current_version['description'] == 'Covers even more data.  Better than ever!'
        assert current_version['script'] == newest_script
        assert current_version['enterer']['id'] == administrator_id
        assert current_version['modifier']['id'] == contributor_id
        phonology_UUID = resp['phonology']['UUID']
        response = self.app.get(url(controller='phonologies', action='history', id=phonology_UUID), headers=self.json_headers, extra_environ=extra_environ)
        resp_UUID = json.loads(response.body)
        assert resp == resp_UUID
        bad_id = 103
        bad_UUID = str(uuid4())
        response = self.app.get(url(controller='phonologies', action='history', id=bad_id), headers=self.json_headers, extra_environ=extra_environ, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'No phonologies or phonology backups match %d' % bad_id
        response = self.app.get(url(controller='phonologies', action='history', id=bad_UUID), headers=self.json_headers, extra_environ=extra_environ, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'No phonologies or phonology backups match %s' % bad_UUID
        response = self.app.delete(url('phonology', id=phonology_id), headers=self.json_headers, extra_environ=extra_environ)
        response = self.app.get(url(controller='phonologies', action='history', id=phonology_UUID), headers=self.json_headers, extra_environ=extra_environ)
        by_UUID_resp = json.loads(response.body)
        assert by_UUID_resp['phonology'] == None
        assert len(by_UUID_resp['previous_versions']) == 3
        first_version = by_UUID_resp['previous_versions'][2]
        second_version = by_UUID_resp['previous_versions'][1]
        third_version = by_UUID_resp['previous_versions'][0]
        assert first_version['name'] == 'Phonology'
        assert first_version['description'] == 'Covers a lot of the data.'
        assert first_version['enterer']['id'] == administrator_id
        assert first_version['modifier']['id'] == administrator_id
        assert first_version['datetime_modified'] <= second_version['datetime_modified']
        assert second_version['name'] == 'Phonology'
        assert second_version['description'] == 'Covers a lot of the data.  Best yet!'
        assert second_version['script'] == new_script
        assert second_version['enterer']['id'] == administrator_id
        assert second_version['modifier']['id'] == administrator_id
        assert second_version['datetime_modified'] <= third_version['datetime_modified']
        assert third_version['name'] == 'Phonology'
        assert third_version['description'] == 'Covers even more data.  Better than ever!'
        assert third_version['script'] == newest_script
        assert third_version['enterer']['id'] == administrator_id
        assert third_version['modifier']['id'] == contributor_id
        response = self.app.get(url(controller='phonologies', action='history', id=phonology_id), headers=self.json_headers, extra_environ=extra_environ)
        by_phonology_id_resp = json.loads(response.body)
        assert by_phonology_id_resp == by_UUID_resp
        return