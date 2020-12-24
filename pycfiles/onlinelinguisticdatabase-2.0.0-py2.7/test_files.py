# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_files.py
# Compiled at: 2016-09-19 13:27:02
import datetime, logging, simplejson as json, os
from base64 import b64encode
from nose.tools import nottest
from mimetypes import guess_type
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        Image = None

log = logging.getLogger(__name__)

class TestFilesController(TestController):

    def tearDown(self):
        TestController.tearDown(self, del_global_app_set=True, dirs_to_clear=[
         'files_path', 'reduced_files_path'])

    @nottest
    def test_index(self):
        """Tests that GET /files returns a JSON array of files with expected values."""
        users = h.get_users()
        contributor_id = [ u for u in users if u.role == 'contributor' ][0].id
        restricted_tag = h.generate_restricted_tag()
        my_contributor = h.generate_default_user()
        my_contributor_first_name = 'Mycontributor'
        my_contributor.first_name = my_contributor_first_name
        Session.add_all([restricted_tag, my_contributor])
        Session.commit()
        my_contributor = Session.query(model.User).filter(model.User.first_name == my_contributor_first_name).first()
        my_contributor_id = my_contributor.id
        restricted_tag = h.get_restricted_tag()
        application_settings = h.generate_default_application_settings()
        application_settings.unrestricted_users = [my_contributor]
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_base64_encoded = b64encode(open(wav_file_path).read())
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_base64_encoded = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'test_restricted_file.wav', 
           'base64_encoded_file': wav_file_base64_encoded, 
           'tags': [
                  h.get_tags()[0].id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        restricted_file_id = resp['id']
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'test_unrestricted_file.jpg', 
           'base64_encoded_file': jpg_file_base64_encoded})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert resp[0]['filename'] == 'test_restricted_file.wav'
        assert resp[1]['filename'] == 'test_unrestricted_file.jpg'
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 1
        application_settings = h.get_application_settings()
        application_settings.unrestricted_users = []
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True, 
           'test.retain_application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 1
        restricted_file = Session.query(model.File).get(restricted_file_id)
        restricted_file.tags = []
        Session.add(restricted_file)
        Session.commit()
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        h.clear_all_models(['User', 'Tag', 'Language'])

        def create_file_from_index(index):
            file = model.File()
            file.filename = 'name_%d.jpg' % index
            return file

        files = [ create_file_from_index(i) for i in range(1, 101) ]
        Session.add_all(files)
        Session.commit()
        files = h.get_files()
        restricted_tag = h.get_restricted_tag()
        for file in files:
            if int(file.filename.split('_')[1].split('.')[0]) % 2 == 0:
                file.tags.append(restricted_tag)
            Session.add(file)

        Session.commit()
        files = h.get_files()
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[0]['filename'] == 'name_1.jpg'
        assert resp[0]['id'] == files[0].id
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('files'), paginator, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['filename'] == files[46].filename
        order_by_params = {'order_by_model': 'File', 'order_by_attribute': 'filename', 'order_by_direction': 'desc'}
        response = self.app.get(url('files'), order_by_params, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        result_set = sorted([ f.filename for f in files ], reverse=True)
        assert result_set == [ f['filename'] for f in resp ]
        assert response.content_type == 'application/json'
        params = {'order_by_model': 'File', 'order_by_attribute': 'filename', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('files'), params, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert result_set[46] == resp['items'][0]['filename']
        items_per_page = 7
        page = 7
        paginator = {'items_per_page': items_per_page, 'page': page}
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('files'), paginator, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp['items']) == items_per_page
        assert resp['items'][0]['filename'] == 'name_%d.jpg' % (items_per_page * (page - 1) * 2 + 1)
        order_by_params = {'order_by_model': 'File', 'order_by_attribute': 'filename', 'order_by_direction': 'descending'}
        response = self.app.get(url('files'), order_by_params, status=400, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        order_by_params = {'order_by_model': 'Fileage', 'order_by_attribute': 'nom', 'order_by_direction': 'desc'}
        response = self.app.get(url('files'), order_by_params, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert resp[0]['id'] == files[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('files'), paginator, headers=self.json_headers, extra_environ=extra_environ, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('files'), paginator, headers=self.json_headers, extra_environ=extra_environ, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /files correctly creates a new file."""
        params = '"a'
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'JSON decode error: the parameters provided were not valid JSON.'
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_size = os.path.getsize(wav_file_path)
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.wav', 
           'base64_encoded_file': b64encode(open(wav_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert resp['filename'] == 'old_test.wav'
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 1
        assert response.content_type == 'application/json'
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_size = os.path.getsize(jpg_file_path)
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        file_id = an_image_id = resp['id']
        assert resp['filename'] == 'old_test.jpg'
        assert resp['MIME_type'] == 'image/jpeg'
        assert resp['size'] == jpg_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 2
        tag1 = model.Tag()
        tag1.name = 'tag 1'
        tag2 = model.Tag()
        tag2.name = 'tag 2'
        restricted_tag = h.generate_restricted_tag()
        Session.add_all([tag1, tag2, restricted_tag])
        Session.commit()
        tag1_id = tag1.id
        tag2_id = tag2.id
        restricted_tag_id = restricted_tag.id
        params = self.form_create_params.copy()
        params.update({'transcription': 'test', 
           'translations': [{'transcription': 'test', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_id = resp['id']
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64, 
           'tags': [
                  tag1_id, tag2_id], 
           'forms': [
                   form_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert resp['filename'][:9] == 'old_test_'
        assert resp['MIME_type'] == 'image/jpeg'
        assert resp['size'] == jpg_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert sorted([ t['id'] for t in resp['tags'] ]) == sorted([tag1_id, tag2_id])
        assert resp['forms'][0]['transcription'] == 'test'
        assert file_count == 3
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_size = os.path.getsize(wav_file_path)
        params = self.file_create_params_base64.copy()
        params.update({'filename': '', 
           'base64_encoded_file': '', 
           'utterance_type': 'l' * 1000, 
           'date_elicited': '31/12/2012', 
           'speaker': 200})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert 'Value must be one of: None; Object Language Utterance; Metalanguage Utterance; Mixed Utterance' in resp['errors']['utterance_type']
        assert resp['errors']['speaker'] == 'There is no speaker with id 200.'
        assert resp['errors']['date_elicited'] == 'Please enter a month from 1 to 12'
        assert resp['errors']['filename'] == 'Please enter a value'
        assert resp['errors']['base64_encoded_file'] == 'Please enter a value'
        assert file_count == 3
        assert response.content_type == 'application/json'
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_size = os.path.getsize(wav_file_path)
        params = self.file_create_params_base64.copy()
        params.update({'filename': '“old tést”.wav', 
           'base64_encoded_file': b64encode(open(wav_file_path).read()), 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        a_wav_file_id = resp['id']
        file_count = Session.query(model.File).count()
        assert '“old_tést”.wav' in os.listdir(self.files_path)
        assert resp['filename'] == '“old_tést”.wav'
        assert resp['name'] == resp['filename']
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 4
        assert restricted_tag_id in [ t['id'] for t in resp['tags'] ]
        assert response.content_type == 'application/json'
        files_dir_list = os.listdir(self.files_path)
        html_file_path = os.path.join(self.test_files_path, 'illicit.html')
        html_file_base64 = b64encode(open(html_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'pretend_its_wav.wav', 
           'base64_encoded_file': html_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        new_files_dir_list = os.listdir(self.files_path)
        assert file_count == 4
        assert resp['errors'] == "The file extension does not match the file's true type (audio/x-wav vs. text/html, respectively)."
        assert files_dir_list == new_files_dir_list
        params = self.file_create_params_MPFD.copy()
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', wav_file_path)])
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert resp['filename'] in os.listdir(self.files_path)
        assert resp['filename'][:8] == 'old_test'
        assert resp['name'] == resp['filename']
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 5
        assert response.content_type == 'application/json'
        params = self.file_create_params_MPFD.copy()
        params.update({'filename': 'wavfile.wav', 
           'description': 'multipart/form-data', 
           'date_elicited': '12/03/2011', 
           'utterance_type': 'Mixed Utterance', 
           'tags-0': tag1_id, 
           'tags-1': tag2_id, 
           'forms-0': form_id})
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', wav_file_path)])
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert 'wavfile.wav' in os.listdir(self.files_path)
        assert resp['filename'] == 'wavfile.wav'
        assert resp['name'] == resp['filename']
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert sorted([ t['id'] for t in resp['tags'] ]) == sorted([tag1_id, tag2_id])
        assert resp['forms'][0]['id'] == form_id
        assert resp['utterance_type'] == 'Mixed Utterance'
        assert resp['description'] == 'multipart/form-data'
        assert resp['date_elicited'] == '2011-12-03'
        assert file_count == 6
        assert response.content_type == 'application/json'
        params = self.file_create_params_MPFD.copy()
        params.update({'filename': '../wavfile.wav'})
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', wav_file_path)])
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        binary_files_list = os.listdir(self.files_path)
        binary_files_list_count = len(binary_files_list)
        assert '..wavfile.wav' in binary_files_list
        assert resp['filename'] == '..wavfile.wav'
        assert resp['name'] == resp['filename']
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 7
        assert response.content_type == 'application/json'
        html_file_path = os.path.join(self.test_files_path, 'illicit.html')
        files_dir_list = os.listdir(self.files_path)
        params = self.file_create_params_MPFD.copy()
        params.update({'filename': 'pretend_its_wav.wav'})
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', html_file_path)], status=400)
        resp = json.loads(response.body)
        new_file_count = Session.query(model.File).count()
        new_files_dir_list = os.listdir(self.files_path)
        assert file_count == new_file_count
        assert resp['errors'] == "The file extension does not match the file's true type (audio/x-wav vs. text/html, respectively)."
        assert files_dir_list == new_files_dir_list
        html_file_path = os.path.join(self.test_files_path, 'illicit.wav')
        files_dir_list = new_files_dir_list
        params = self.file_create_params_MPFD.copy()
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', html_file_path)], status=400)
        resp = json.loads(response.body)
        new_file_count = Session.query(model.File).count()
        new_files_dir_list = os.listdir(self.files_path)
        assert file_count == new_file_count
        assert resp['errors'] == "The file extension does not match the file's true type (audio/x-wav vs. text/html, respectively)."
        assert files_dir_list == new_files_dir_list
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': a_wav_file_id, 
           'name': 'subinterval_x', 
           'start': 1.3, 
           'end': 2.6})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        new_binary_files_list = os.listdir(self.files_path)
        new_binary_files_list_count = len(new_binary_files_list)
        subinterval_referencing_id = resp['id']
        assert new_binary_files_list_count == binary_files_list_count
        assert '“old_tést”.wav' in new_binary_files_list
        assert 'subinterval_x' not in new_binary_files_list
        assert resp['filename'] == None
        assert resp['parent_file']['filename'] == '“old_tést”.wav'
        assert resp['name'] == 'subinterval_x'
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == None
        assert resp['parent_file']['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['start'] == 1.3
        assert type(resp['start']) is float
        assert resp['end'] == 2.6
        assert type(resp['end']) is float
        assert file_count == 8
        assert response.content_type == 'application/json'
        params = self.file_create_params_sub_ref.copy()
        params.update({'name': 'subinterval_x' * 200, 
           'start': 'a', 
           'end': None})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert file_count == 8
        assert resp['errors']['parent_file'] == 'An id corresponding to an existing audio or video file must be provided.'
        assert resp['errors']['start'] == 'Please enter a number'
        assert resp['errors']['end'] == 'Please enter a value'
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': a_wav_file_id, 
           'name': 'subinterval_y', 
           'start': 3.75, 
           'end': 4.999})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_contrib, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert file_count == 8
        assert resp['errors']['parent_file'] == 'You are not authorized to access the file with id %d.' % a_wav_file_id
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': a_wav_file_id, 
           'start': 3.75, 
           'end': 4.999})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert file_count == 9
        assert resp['parent_file']['id'] == a_wav_file_id
        assert 'restricted' not in [ t['name'] for t in resp['tags'] ]
        assert resp['name'] == resp['parent_file']['name']
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': an_image_id, 
           'name': 'subinterval_y', 
           'start': 3.75, 
           'end': 4.999})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert file_count == 9
        assert resp['errors']['parent_file'] == 'File %d is not an audio or a video file.' % an_image_id
        bad_id = 1000009252345345
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': bad_id, 
           'name': 'subinterval_y', 
           'start': 3.75, 
           'end': 4.999})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert file_count == 9
        assert resp['errors']['parent_file'] == 'There is no file with id %d.' % bad_id
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': subinterval_referencing_id, 
           'name': 'subinterval_y', 
           'start': 3.75, 
           'end': 4.999})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert file_count == 9
        assert resp['errors']['parent_file'] == 'The parent file cannot itself be a subinterval-referencing file.'
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': a_wav_file_id, 
           'name': 'subinterval_z', 
           'start': 1.3, 
           'end': 1.3})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert response.content_type == 'application/json'
        assert resp['errors'] == 'The start value must be less than the end value.'
        params = self.file_create_params_ext_host.copy()
        url_ = 'http://vimeo.com/54144270'
        params.update({'url': url_, 
           'name': 'externally hosted file', 
           'MIME_type': 'video/mpeg', 
           'description': "A large video file I didn't want to upload here."})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['description'] == "A large video file I didn't want to upload here."
        assert resp['url'] == url_
        params = self.file_create_params_ext_host.copy()
        url_ = 'http://vimeo/541442705414427054144270541442705414427054144270'
        params.update({'url': url_, 
           'name': 'invalid externally hosted file', 
           'MIME_type': 'video/gepm', 
           'description': 'A large video file, sadly invalid.'})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['MIME_type'] == 'The file upload failed because the file type video/gepm is not allowed.'
        resp['errors']['url'] == 'You must provide a full domain name (like vimeo.com)'
        params = self.file_create_params_ext_host.copy()
        params.update({'url': '', 
           'name': 'invalid externally hosted file' * 200, 
           'password': 'a87XS.1d9X837a001W2w3a87XS.1d9X837a001W2w3' * 200, 
           'description': 'A large video file, sadly invalid.'})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['url'] == 'Please enter a value'
        assert resp['errors']['password'] == 'Enter a value not more than 255 characters long'
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        params = self.file_create_params_ext_host.copy()
        url_ = 'http://vimeo.com/54144270'
        params.update({'url': url_, 
           'MIME_type': 'video/mpeg', 
           'description': "A large video file I didn't want to upload here."})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == ''
        return

    @nottest
    def test_relational_restrictions(self):
        """Tests that the restricted tag works correctly with respect to relational attributes of files.

        That is, tests that (a) file.forms does not return restricted forms to
        restricted users and (b) a restricted user cannot append a restricted
        form to file.forms."""
        admin = self.extra_environ_admin.copy()
        admin.update({'test.application_settings': True})
        contrib = self.extra_environ_contrib.copy()
        contrib.update({'test.application_settings': True})
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_size = os.path.getsize(wav_file_path)
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.wav', 
           'base64_encoded_file': b64encode(open(wav_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert resp['filename'] == 'old_test.wav'
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 1
        assert response.content_type == 'application/json'
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        restricted_tag_id = restricted_tag.id
        params = self.form_create_params.copy()
        params.update({'transcription': 'restricted', 
           'translations': [{'transcription': 'restricted', 'grammaticality': ''}], 'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        restricted_form_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'unrestricted', 
           'translations': [{'transcription': 'unrestricted', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        unrestricted_form_id = resp['id']
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_size = os.path.getsize(jpg_file_path)
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64, 
           'forms': [
                   restricted_form_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, contrib, status=400)
        resp = json.loads(response.body)
        assert 'You are not authorized to access the form with id %d.' % restricted_form_id in resp['errors']['forms']
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_size = os.path.getsize(jpg_file_path)
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64, 
           'forms': [
                   unrestricted_form_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        unrestricted_file_id = resp['id']
        assert resp['filename'] == 'old_test.jpg'
        assert resp['forms'][0]['transcription'] == 'unrestricted'
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64, 
           'forms': [
                   restricted_form_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        indirectly_restricted_file_id = resp['id']
        assert resp['filename'][:8] == 'old_test'
        assert resp['forms'][0]['transcription'] == 'restricted'
        assert 'restricted' in [ t['name'] for t in resp['tags'] ]
        response = self.app.get(url('files'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert indirectly_restricted_file_id not in [ f['id'] for f in resp ]
        unrestricted_file_params = self.file_create_params_base64.copy()
        unrestricted_file_params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(unrestricted_file_params)
        response = self.app.post(url('files'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        unrestricted_file_id = resp['id']
        assert resp['filename'][:8] == 'old_test'
        assert response.content_type == 'application/json'
        unrestricted_file_params.update({'forms': [restricted_form_id]})
        params = json.dumps(unrestricted_file_params)
        response = self.app.put(url('file', id=unrestricted_file_id), params, self.json_headers, contrib, status=400)
        resp = json.loads(response.body)
        assert 'You are not authorized to access the form with id %d.' % restricted_form_id in resp['errors']['forms']
        assert response.content_type == 'application/json'
        response = self.app.put(url('file', id=unrestricted_file_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        assert resp['id'] == unrestricted_file_id
        assert 'restricted' in [ t['name'] for t in resp['tags'] ]
        response = self.app.get(url('file', id=unrestricted_file_id), headers=self.json_headers, extra_environ=contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'

    @nottest
    def test_create_large(self):
        """Tests that POST /files correctly creates a large file.

        WARNING 1: long-running test.

        WARNING: 2: if a large file named old_test_long.wav does not exist in
        ``tests/data/files``, this test will pass vacuously.  I don't want to
        include such a large file in the code base so this file needs to be
        created if one wants this test to run.
        """
        file_count = new_file_count = Session.query(model.File).count()
        long_wav_filename = 'old_test_long.wav'
        long_wav_file_path = os.path.join(self.test_files_path, long_wav_filename)
        if os.path.exists(long_wav_file_path):
            long_wav_file_size = os.path.getsize(long_wav_file_path)
            params = self.file_create_params_base64.copy()
            params.update({'filename': long_wav_filename, 
               'base64_encoded_file': b64encode(open(long_wav_file_path).read())})
            params = json.dumps(params)
            response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
            resp = json.loads(response.body)
            new_file_count = Session.query(model.File).count()
            assert file_count == new_file_count
            assert resp['error'] == 'The request body is too large; use the multipart/form-data Content-Type when uploading files greater than 20MB.'
            assert response.content_type == 'application/json'
        medium_wav_filename = 'old_test_medium.wav'
        medium_wav_file_path = os.path.join(self.test_files_path, medium_wav_filename)
        if os.path.exists(medium_wav_file_path):
            old_reduced_dir_list = os.listdir(self.reduced_files_path)
            medium_wav_file_size = os.path.getsize(medium_wav_file_path)
            params = self.file_create_params_base64.copy()
            params.update({'filename': medium_wav_filename, 
               'base64_encoded_file': b64encode(open(medium_wav_file_path).read())})
            params = json.dumps(params)
            response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            file_count = new_file_count
            new_file_count = Session.query(model.File).count()
            new_reduced_dir_list = os.listdir(self.reduced_files_path)
            lossy_filename = '%s.%s' % (os.path.splitext(medium_wav_filename)[0],
             self.config.get('preferred_lossy_audio_format', 'ogg'))
            assert file_count + 1 == new_file_count
            assert resp['filename'] == medium_wav_filename
            assert resp['MIME_type'] == 'audio/x-wav'
            assert resp['size'] == medium_wav_file_size
            assert resp['enterer']['first_name'] == 'Admin'
            assert response.content_type == 'application/json'
            assert lossy_filename not in old_reduced_dir_list
            if self.create_reduced_size_file_copies and h.command_line_program_installed('ffmpeg'):
                assert resp['lossy_filename'] == lossy_filename
                assert lossy_filename in new_reduced_dir_list
            else:
                assert resp['lossy_filename'] == None
                assert lossy_filename not in new_reduced_dir_list
        if os.path.exists(long_wav_file_path):
            long_wav_file_size = os.path.getsize(long_wav_file_path)
            params = self.file_create_params_MPFD.copy()
            params.update({'filename': long_wav_filename})
            response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
             (
              'filedata', long_wav_file_path)])
            resp = json.loads(response.body)
            file_count = new_file_count
            new_file_count = Session.query(model.File).count()
            new_reduced_dir_list = os.listdir(self.reduced_files_path)
            lossy_filename = '%s.%s' % (os.path.splitext(long_wav_filename)[0],
             self.config.get('preferred_lossy_audio_format', 'ogg'))
            assert file_count + 1 == new_file_count
            assert resp['filename'] == long_wav_filename
            assert resp['MIME_type'] == 'audio/x-wav'
            assert resp['size'] == long_wav_file_size
            assert resp['enterer']['first_name'] == 'Admin'
            assert response.content_type == 'application/json'
            assert lossy_filename not in old_reduced_dir_list
            if self.create_reduced_size_file_copies and h.command_line_program_installed('ffmpeg'):
                assert resp['lossy_filename'] == lossy_filename
                assert lossy_filename in new_reduced_dir_list
            else:
                assert resp['lossy_filename'] == None
                assert lossy_filename not in new_reduced_dir_list
        return

    @nottest
    def test_new(self):
        """Tests that GET /file/new returns an appropriate JSON object for creating a new OLD file.

        The properties of the JSON object are 'tags', 'utterance_types',
        'speakers'and 'users' and their values are arrays/lists.
        """
        extra_environ = {'test.authentication.role': 'viewer'}
        response = self.app.get(url('new_file'), extra_environ=extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        application_settings = h.generate_default_application_settings()
        restricted_tag = h.generate_restricted_tag()
        speaker = h.generate_default_speaker()
        Session.add_all([application_settings, restricted_tag, speaker])
        Session.commit()
        data = {'tags': h.get_mini_dicts_getter('Tag')(), 
           'speakers': h.get_mini_dicts_getter('Speaker')(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'utterance_types': h.utterance_types, 
           'allowed_file_types': h.allowed_file_types}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        response = self.app.get(url('new_file'), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['tags'] == data['tags']
        assert resp['speakers'] == data['speakers']
        assert resp['users'] == data['users']
        assert resp['utterance_types'] == data['utterance_types']
        assert resp['allowed_file_types'] == data['allowed_file_types']
        assert response.content_type == 'application/json'
        params = {'speakers': 'anything can go here!', 
           'users': datetime.datetime.utcnow().isoformat(), 
           'tags': h.get_most_recent_modification_datetime('Tag').isoformat()}
        response = self.app.get(url('new_file'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['tags'] == []
        assert resp['speakers'] == data['speakers']
        assert resp['users'] == data['users']
        assert resp['utterance_types'] == data['utterance_types']
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /files/id correctly updates an existing file."""
        file_count = Session.query(model.File).count()
        restricted_tag = h.generate_restricted_tag()
        application_settings = h.generate_default_application_settings()
        Session.add_all([application_settings, restricted_tag])
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        restricted_tag_id = restricted_tag.id
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_size = os.path.getsize(wav_file_path)
        params = self.file_create_params_base64.copy()
        original_name = 'test_update_name.wav'
        params.update({'filename': original_name, 
           'tags': [
                  restricted_tag.id], 
           'description': 'description', 
           'base64_encoded_file': b64encode(open(wav_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        id = int(resp['id'])
        new_file_count = Session.query(model.File).count()
        assert resp['filename'] == original_name
        assert new_file_count == file_count + 1
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        params = self.file_create_params_base64.copy()
        params.update({'description': 'A file that has been updated.'})
        params = json.dumps(params)
        response = self.app.put(url('file', id=id), params, self.json_headers, extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        params = self.file_create_params_base64.copy()
        params.update({'description': 'A file that has been updated.'})
        params = json.dumps(params)
        response = self.app.put(url('file', id=id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_file_count = Session.query(model.File).count()
        assert resp['description'] == 'A file that has been updated.'
        assert resp['tags'] == []
        assert new_file_count == file_count + 1
        assert response.content_type == 'application/json'
        response = self.app.put(url('file', id=id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert 'the submitted data were not new' in resp['error']
        speaker = h.generate_default_speaker()
        tag1 = model.Tag()
        tag1.name = 'tag 1'
        tag2 = model.Tag()
        tag2.name = 'tag 2'
        Session.add_all([speaker, tag1, tag2])
        Session.commit()
        speaker = h.get_speakers()[0]
        tag1_id = tag1.id
        tag2_id = tag2.id
        speaker_id = speaker.id
        params = self.file_create_params_base64.copy()
        params.update({'speaker': speaker.id})
        params = json.dumps(params)
        response = self.app.put(url('file', id=id), params, self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['speaker']['first_name'] == speaker.first_name
        params = self.file_create_params_base64.copy()
        params.update({'tags': [tag1_id, tag2_id]})
        params = json.dumps(params)
        response = self.app.put(url('file', id=id), params, self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert sorted([ t['name'] for t in resp['tags'] ]) == ['tag 1', 'tag 2']
        params = self.file_create_params_MPFD.copy()
        params.update({'filename': 'multipart.wav'})
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', wav_file_path)])
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        plain_file_id = resp['id']
        assert resp['filename'] == 'multipart.wav'
        assert resp['filename'] in os.listdir(self.files_path)
        assert resp['name'] == resp['filename']
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['enterer']['first_name'] == 'Admin'
        assert response.content_type == 'application/json'
        params = self.file_create_params_base64.copy()
        params.update({'tags': [
                  tag1_id, tag2_id], 
           'description': 'plain updated', 
           'date_elicited': '01/01/2000', 
           'speaker': speaker_id, 
           'utterance_type': 'Metalanguage Utterance'})
        params = json.dumps(params)
        response = self.app.put(url('file', id=plain_file_id), params, self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert sorted([ t['name'] for t in resp['tags'] ]) == ['tag 1', 'tag 2']
        assert resp['description'] == 'plain updated'
        assert resp['speaker']['id'] == speaker_id
        assert resp['filename'] == resp['name'] == 'multipart.wav'
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['enterer']['first_name'] == 'Admin'
        assert response.content_type == 'application/json'
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': plain_file_id, 
           'name': 'anyname', 
           'start': 13.3, 
           'end': 26.89, 
           'tags': [
                  tag1_id], 
           'description': 'subinterval-referencing file', 
           'date_elicited': '01/01/2000', 
           'speaker': speaker_id, 
           'utterance_type': 'Object Language Utterance'})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_contrib)
        resp = json.loads(response.body)
        subinterval_referencing_id = resp['id']
        assert resp['filename'] == None
        assert resp['name'] == 'anyname'
        assert resp['parent_file']['filename'] == 'multipart.wav'
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == None
        assert resp['parent_file']['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Contributor'
        assert resp['start'] == 13.3
        assert type(resp['start']) is float
        assert resp['end'] == 26.89
        assert type(resp['end']) is float
        assert resp['tags'][0]['id'] == tag1_id
        assert response.content_type == 'application/json'
        params = self.file_create_params_base64.copy()
        params.update({'parent_file': plain_file_id, 
           'start': 13.3, 
           'end': 26.89, 
           'tags': [], 'description': 'abc to def', 
           'date_elicited': '01/01/2010', 
           'utterance_type': 'Metalanguage Utterance'})
        params = json.dumps(params)
        response = self.app.put(url('file', id=subinterval_referencing_id), params, self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp['parent_file']['id'] == plain_file_id
        assert resp['name'] == resp['parent_file']['name']
        assert resp['tags'] == []
        assert resp['description'] == 'abc to def'
        assert resp['speaker'] == None
        assert resp['MIME_type'] == 'audio/x-wav'
        assert response.content_type == 'application/json'
        response = self.app.put(url('file', id=subinterval_referencing_id), params, self.json_headers, extra_environ=self.extra_environ_contrib, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        params = self.file_create_params_base64.copy()
        params.update({'tags': [
                  tag1_id, tag2_id, restricted_tag_id], 
           'description': 'plain updated', 
           'date_elicited': '01/01/2000', 
           'speaker': speaker_id, 
           'utterance_type': 'Metalanguage Utterance'})
        params = json.dumps(params)
        response = self.app.put(url('file', id=plain_file_id), params, self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert 'restricted' in [ t['name'] for t in resp['tags'] ]
        SRFile = Session.query(model.File).get(subinterval_referencing_id)
        assert 'restricted' not in [ t.name for t in SRFile.tags ]
        url_ = 'http://vimeo.com/54144270'
        params = self.file_create_params_ext_host.copy()
        params.update({'url': url_, 
           'name': 'externally hosted file', 
           'MIME_type': 'video/mpeg', 
           'description': "A large video file I didn't want to upload here."})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['description'] == "A large video file I didn't want to upload here."
        assert resp['url'] == url_
        params = self.file_create_params_ext_host.copy()
        params.update({'url': url_, 
           'name': 'externally hosted file', 
           'password': 'abc', 
           'MIME_type': 'video/mpeg', 
           'description': "A large video file I didn't want to upload here.", 
           'date_elicited': '12/29/1987'})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['date_elicited'] == '1987-12-29'
        assert resp['password'] == 'abc'
        params = self.file_create_params_ext_host.copy()
        params.update({'url': 'abc', 
           'name': 'externally hosted file' * 200, 
           'MIME_type': 'zooboomafoo', 
           'description': "A large video file I didn't want to upload here.", 
           'date_elicited': '1987/12/29'})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['MIME_type'] == 'The file upload failed because the file type zooboomafoo is not allowed.'
        assert resp['errors']['url'] == 'You must provide a full domain name (like abc.com)'
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        assert resp['errors']['date_elicited'] == 'Please enter the date in the form mm/dd/yyyy'
        return

    @nottest
    def test_delete(self):
        """Tests that DELETE /files/id deletes the file with id=id and returns a JSON representation.

        If the id is invalid or unspecified, then JSON null or a 404 status code
        are returned, respectively.
        """
        application_settings = h.generate_default_application_settings()
        speaker = h.generate_default_speaker()
        my_contributor = h.generate_default_user()
        my_contributor.username = 'uniqueusername'
        tag = model.Tag()
        tag.name = 'default tag'
        Session.add_all([application_settings, speaker, my_contributor, tag])
        Session.commit()
        my_contributor = Session.query(model.User).filter(model.User.username == 'uniqueusername').first()
        my_contributor_id = my_contributor.id
        tag_id = tag.id
        speaker_id = speaker.id
        file_count = Session.query(model.File).count()
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'test_delete.jpg', 
           'base64_encoded_file': b64encode(open(jpg_file_path).read()), 
           'speaker': speaker_id, 
           'tags': [
                  tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        to_delete_id = resp['id']
        to_delete_name = resp['filename']
        assert resp['filename'] == 'test_delete.jpg'
        assert resp['tags'][0]['name'] == 'default tag'
        new_file_count = Session.query(model.File).count()
        assert new_file_count == file_count + 1
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        response = self.app.delete(url('file', id=to_delete_id), extra_environ=extra_environ, status=403)
        resp = json.loads(response.body)
        file_that_was_not_deleted = Session.query(model.File).get(to_delete_id)
        file_path = os.path.join(self.files_path, to_delete_name)
        assert os.path.exists(file_path)
        assert file_that_was_not_deleted is not None
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.delete(url('file', id=to_delete_id), extra_environ=extra_environ)
        resp = json.loads(response.body)
        new_file_count = Session.query(model.File).count()
        tag_of_deleted_file = Session.query(model.Tag).get(resp['tags'][0]['id'])
        speaker_of_deleted_file = Session.query(model.Speaker).get(resp['speaker']['id'])
        assert isinstance(tag_of_deleted_file, model.Tag)
        assert isinstance(speaker_of_deleted_file, model.Speaker)
        assert new_file_count == file_count
        file_that_was_deleted = Session.query(model.File).get(to_delete_id)
        file_path = os.path.join(self.files_path, to_delete_name)
        assert not os.path.exists(file_path)
        assert 'old_test.jpg' not in os.listdir(self.files_path)
        assert file_that_was_deleted is None
        assert resp['filename'] == 'test_delete.jpg'
        id = 9999999999999
        response = self.app.delete(url('file', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no file with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('file', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        params = self.file_create_params_base64.copy()
        params.update({'filename': '“tést delete”.jpg', 
           'base64_encoded_file': b64encode(open(jpg_file_path).read()), 
           'speaker': speaker_id, 
           'tags': [
                  tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        to_delete_id = resp['id']
        to_delete_name = resp['filename']
        assert resp['filename'] == '“tést_delete”.jpg'
        assert resp['tags'][0]['name'] == 'default tag'
        assert '“tést_delete”.jpg' in os.listdir(self.files_path)
        response = self.app.delete(url('file', id=to_delete_id), extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert '“tést_delete”.jpg' not in os.listdir(self.files_path)
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'parent.wav', 
           'base64_encoded_file': b64encode(open(wav_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        parent_id = resp['id']
        parent_filename = resp['filename']
        parent_lossy_filename = resp['lossy_filename']
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': parent_id, 
           'name': 'child', 
           'start': 1, 
           'end': 2})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        child_id = resp['id']
        assert resp['parent_file']['id'] == parent_id
        if not parent_filename in os.listdir(self.files_path):
            raise AssertionError
            assert self.create_reduced_size_file_copies and h.command_line_program_installed('ffmpeg') and parent_lossy_filename in os.listdir(self.reduced_files_path)
        response = self.app.delete(url('file', id=parent_id), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert parent_filename not in os.listdir(self.files_path)
        assert parent_lossy_filename not in os.listdir(self.reduced_files_path)
        assert resp['filename'] == 'parent.wav'
        parent = Session.query(model.File).get(parent_id)
        assert parent is None
        child = Session.query(model.File).get(child_id)
        assert child is not None
        assert child.parent_file is None
        response = self.app.delete(url('file', id=child_id), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'child'
        return

    @nottest
    def test_show(self):
        """Tests that GET /files/id returns a JSON file object, null or 404
        depending on whether the id is valid, invalid or unspecified,
        respectively.
        """
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_size = os.path.getsize(jpg_file_path)
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': b64encode(open(jpg_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        file_id = resp['id']
        assert resp['filename'] == 'old_test.jpg'
        assert resp['MIME_type'] == 'image/jpeg'
        assert resp['size'] == jpg_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert file_count == 1
        params = self.form_create_params.copy()
        params.update({'transcription': 'test', 
           'translations': [{'transcription': 'test', 'grammaticality': ''}], 'files': [
                   file_id]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert type(resp) == type({})
        assert resp['transcription'] == 'test'
        assert resp['translations'][0]['transcription'] == 'test'
        assert resp['morpheme_break_ids'] == None
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['files'][0]['filename'] == 'old_test.jpg'
        response = self.app.get(url('file', id=file_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['forms'][0]['transcription'] == 'test'
        assert resp['filename'] == 'old_test.jpg'
        assert response.content_type == 'application/json'
        id = 100000000000
        response = self.app.get(url('file', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no file with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('file', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        users = h.get_users()
        contributor_id = [ u for u in users if u.role == 'contributor' ][0].id
        restricted_tag = h.generate_restricted_tag()
        my_contributor = h.generate_default_user()
        my_contributor_first_name = 'Mycontributor'
        my_contributor.first_name = my_contributor_first_name
        my_contributor.username = 'uniqueusername'
        Session.add_all([restricted_tag, my_contributor])
        Session.commit()
        my_contributor = Session.query(model.User).filter(model.User.first_name == my_contributor_first_name).first()
        my_contributor_id = my_contributor.id
        application_settings = h.generate_default_application_settings()
        application_settings.unrestricted_users = [my_contributor]
        Session.add(application_settings)
        Session.commit()
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.wav', 
           'base64_encoded_file': b64encode(open(wav_file_path).read()), 
           'tags': [
                  h.get_tags()[0].id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        restricted_file_id = resp['id']
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        response = self.app.get(url('file', id=restricted_file_id), headers=self.json_headers, extra_environ=extra_environ)
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        response = self.app.get(url('file', id=restricted_file_id), headers=self.json_headers, extra_environ=extra_environ)
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.get(url('file', id=restricted_file_id), headers=self.json_headers, extra_environ=extra_environ)
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('file', id=restricted_file_id), headers=self.json_headers, extra_environ=extra_environ, status=403)
        application_settings = h.get_application_settings()
        application_settings.unrestricted_users = []
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.get(url('file', id=restricted_file_id), headers=self.json_headers, extra_environ=extra_environ, status=403)
        restricted_file = Session.query(model.File).get(restricted_file_id)
        restricted_file.tags = []
        Session.add(restricted_file)
        Session.commit()
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('file', id=restricted_file_id), headers=self.json_headers, extra_environ=extra_environ)
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_edit(self):
        """Tests that GET /files/id/edit returns a JSON object of data necessary to edit the file with id=id.

        The JSON object is of the form {'file': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        application_settings = h.generate_default_application_settings()
        restricted_tag = h.generate_restricted_tag()
        Session.add_all([restricted_tag, application_settings])
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        contributor = [ u for u in h.get_users() if u.role == 'contributor' ][0]
        contributor_id = contributor.id
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.wav', 
           'base64_encoded_file': b64encode(open(wav_file_path).read()), 
           'tags': [
                  restricted_tag.id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        restricted_file_id = resp['id']
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        response = self.app.get(url('edit_file', id=restricted_file_id), extra_environ=extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_file', id=restricted_file_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        id = 9876544
        response = self.app.get(url('edit_file', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no file with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_file', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        response = self.app.get(url('edit_file', id=restricted_file_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['file']['filename'] == 'old_test.wav'
        assert response.content_type == 'application/json'
        application_settings = h.generate_default_application_settings()
        speaker = h.generate_default_speaker()
        tag = model.Tag()
        tag.name = 'name'
        Session.add_all([application_settings, speaker, tag])
        Session.commit()
        data = {'tags': h.get_mini_dicts_getter('Tag')(), 
           'speakers': h.get_mini_dicts_getter('Speaker')(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'utterance_types': h.utterance_types, 
           'allowed_file_types': h.allowed_file_types}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        params = {'users': 'give me some users!', 
           'speakers': '', 
           'tags': datetime.datetime.utcnow().isoformat()}
        response = self.app.get(url('edit_file', id=restricted_file_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['data']['tags'] == data['tags']
        assert resp['data']['speakers'] == []
        assert resp['data']['users'] == data['users']
        assert resp['data']['utterance_types'] == data['utterance_types']
        assert response.content_type == 'application/json'
        params = {'speakers': 'True'}
        response = self.app.get(url('edit_file', id=id), params, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no file with id %s' % id in json.loads(response.body)['error']

    @nottest
    def test_serve(self):
        """Tests that GET /files/id/serve returns the file with name id from
        the permanent store, i.e., from onlinelinguisticdatabase/files/.
        """
        extra_environ_admin = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        extra_environ_contrib = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        restricted_tag_id = restricted_tag.id
        test_files_path = self.test_files_path
        wav_filename = 'old_test.wav'
        wav_file_path = os.path.join(test_files_path, wav_filename)
        wav_file_size = os.path.getsize(wav_file_path)
        wav_file_base64 = b64encode(open(wav_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': wav_filename, 
           'base64_encoded_file': wav_file_base64, 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ_admin)
        resp = json.loads(response.body)
        wav_filename = resp['filename']
        wav_file_id = resp['id']
        response = self.app.get(url(controller='files', action='serve', id=wav_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
        response_base64 = b64encode(response.body)
        assert wav_file_base64 == response_base64
        assert guess_type(wav_filename)[0] == response.headers['Content-Type']
        assert wav_file_size == int(response.headers['Content-Length'])
        response = self.app.get(url(controller='files', action='serve', id=wav_file_id), headers=self.json_headers, status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        response = self.app.get(url(controller='files', action='serve', id=wav_file_id), headers=self.json_headers, extra_environ=extra_environ_contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        params = self.file_create_params_ext_host.copy()
        url_ = 'http://vimeo.com/54144270'
        params.update({'url': url_, 
           'name': 'externally hosted file', 
           'MIME_type': 'video/mpeg', 
           'description': "A large video file I didn't want to upload here."})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        eh_file_id = resp['id']
        response = self.app.get(url(controller='files', action='serve', id=eh_file_id), headers=self.json_headers, extra_environ=extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The content of file %s is stored elsewhere at %s' % (eh_file_id, url_)
        assert response.content_type == 'application/json'
        params = self.file_create_params_sub_ref.copy()
        params.update({'parent_file': wav_file_id, 
           'name': 'subinterval_x', 
           'start': 1.3, 
           'end': 2.6})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        sr_file_id = resp['id']
        response = self.app.get(url(controller='files', action='serve', id=sr_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
        response_base64 = b64encode(response.body)
        assert wav_file_base64 == response_base64
        assert guess_type(wav_filename)[0] == response.headers['Content-Type']
        if self.create_reduced_size_file_copies and h.command_line_program_installed('ffmpeg'):
            response = self.app.get(url(controller='files', action='serve_reduced', id=wav_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
            response_base64 = b64encode(response.body)
            assert len(wav_file_base64) > len(response_base64)
            assert response.content_type == h.guess_type('x.%s' % self.preferred_lossy_audio_format)[0]
        else:
            response = self.app.get(url(controller='files', action='serve_reduced', id=wav_file_id), headers=self.json_headers, extra_environ=extra_environ_admin, status=404)
            resp = json.loads(response.body)
            assert resp['error'] == 'There is no size-reduced copy of file %s' % wav_file_id
            assert response.content_type == 'application/json'
        if self.create_reduced_size_file_copies and h.command_line_program_installed('ffmpeg'):
            response = self.app.get(url(controller='files', action='serve_reduced', id=sr_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
            sr_response_base64 = b64encode(response.body)
            assert len(wav_file_base64) > len(sr_response_base64)
            assert sr_response_base64 == response_base64
            assert response.content_type == h.guess_type('x.%s' % self.preferred_lossy_audio_format)[0]
        else:
            response = self.app.get(url(controller='files', action='serve_reduced', id=sr_file_id), headers=self.json_headers, extra_environ=extra_environ_admin, status=404)
            resp = json.loads(response.body)
            assert resp['error'] == 'There is no size-reduced copy of file %s' % sr_file_id
            assert response.content_type == 'application/json'
        jpg_filename = 'large_image.jpg'
        jpg_file_path = os.path.join(test_files_path, jpg_filename)
        jpg_file_size = os.path.getsize(jpg_file_path)
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': jpg_filename, 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ_admin)
        resp = json.loads(response.body)
        jpg_filename = resp['filename']
        jpg_file_id = resp['id']
        response = self.app.get(url(controller='files', action='serve', id=jpg_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
        response_base64 = b64encode(response.body)
        assert jpg_file_base64 == response_base64
        assert guess_type(jpg_filename)[0] == response.headers['Content-Type']
        assert jpg_file_size == int(response.headers['Content-Length'])
        if self.create_reduced_size_file_copies and Image:
            response = self.app.get(url(controller='files', action='serve_reduced', id=jpg_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
            response_base64 = b64encode(response.body)
            assert jpg_file_base64 > response_base64
            assert guess_type(jpg_filename)[0] == response.headers['Content-Type']
        else:
            response = self.app.get(url(controller='files', action='serve_reduced', id=jpg_file_id), headers=self.json_headers, extra_environ=extra_environ_admin, status=404)
            resp = json.loads(response.body)
            assert resp['error'] == 'There is no size-reduced copy of file %s' % jpg_file_id
        ogg_filename = 'old_test.ogg'
        ogg_file_path = os.path.join(test_files_path, ogg_filename)
        ogg_file_size = os.path.getsize(ogg_file_path)
        ogg_file_base64 = b64encode(open(ogg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': ogg_filename, 
           'base64_encoded_file': ogg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, extra_environ_admin)
        resp = json.loads(response.body)
        ogg_filename = resp['filename']
        ogg_file_id = resp['id']
        response = self.app.get(url(controller='files', action='serve', id=ogg_file_id), headers=self.json_headers, extra_environ=extra_environ_admin)
        response_base64 = b64encode(response.body)
        assert ogg_file_base64 == response_base64
        assert guess_type(ogg_filename)[0] == response.headers['Content-Type']
        assert ogg_file_size == int(response.headers['Content-Length'])
        response = self.app.get(url(controller='files', action='serve_reduced', id=ogg_file_id), headers=self.json_headers, extra_environ=extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no size-reduced copy of file %s' % ogg_file_id
        response = self.app.get(url(controller='files', action='serve', id=123456789012), headers=self.json_headers, extra_environ=extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no file with id 123456789012'

    @nottest
    def test_file_reduction(self):
        """Verifies that reduced-size copies of image and wav files are created in files/reduced_files
        and that the names of these reduced-size files is returned as the lossy_filename
        attribute.

        Note that this test will fail if create_reduced_size_file_copies is set
        to 0 in the config file.
        """

        def get_size(path):
            return os.stat(path).st_size

        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_size = os.path.getsize(jpg_file_path)
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = Session.query(model.File).count()
        assert resp['filename'] == 'old_test.jpg'
        assert resp['MIME_type'] == 'image/jpeg'
        assert resp['size'] == jpg_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['lossy_filename'] == None
        assert file_count == 1
        assert len(os.listdir(self.reduced_files_path)) == 0
        filename = 'large_image.jpg'
        jpg_file_path = os.path.join(self.test_files_path, filename)
        jpg_reduced_file_path = os.path.join(self.reduced_files_path, filename)
        jpg_file_base64 = b64encode(open(jpg_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': filename, 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_file_count = Session.query(model.File).count()
        assert new_file_count == file_count + 1
        assert resp['filename'] == filename
        assert resp['MIME_type'] == 'image/jpeg'
        assert resp['enterer']['first_name'] == 'Admin'
        if self.create_reduced_size_file_copies and Image:
            assert resp['lossy_filename'] == filename
            assert resp['lossy_filename'] in os.listdir(self.reduced_files_path)
            assert get_size(jpg_file_path) > get_size(jpg_reduced_file_path)
        else:
            assert resp['lossy_filename'] is None
            assert not os.path.isfile(jpg_reduced_file_path)
        filename = 'large_image.gif'
        gif_file_path = os.path.join(self.test_files_path, filename)
        gif_reduced_file_path = os.path.join(self.reduced_files_path, filename)
        gif_file_base64 = b64encode(open(gif_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': filename, 
           'base64_encoded_file': gif_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = new_file_count
        new_file_count = Session.query(model.File).count()
        assert new_file_count == file_count + 1
        assert resp['filename'] == filename
        assert resp['MIME_type'] == 'image/gif'
        assert resp['enterer']['first_name'] == 'Admin'
        if self.create_reduced_size_file_copies and Image:
            assert resp['lossy_filename'] == filename
            assert resp['lossy_filename'] in os.listdir(self.reduced_files_path)
            assert get_size(gif_file_path) > get_size(gif_reduced_file_path)
        else:
            assert resp['lossy_filename'] is None
            assert not os.path.isfile(gif_reduced_file_path)
        filename = 'large_image.png'
        png_file_path = os.path.join(self.test_files_path, filename)
        png_reduced_file_path = os.path.join(self.reduced_files_path, filename)
        params = self.file_create_params_MPFD.copy()
        params.update({'filename': filename})
        response = self.app.post(url('/files'), params, extra_environ=self.extra_environ_admin, upload_files=[
         (
          'filedata', png_file_path)])
        resp = json.loads(response.body)
        file_count = new_file_count
        new_file_count = Session.query(model.File).count()
        assert new_file_count == file_count + 1
        assert resp['filename'] == filename
        assert resp['MIME_type'] == 'image/png'
        assert resp['enterer']['first_name'] == 'Admin'
        if self.create_reduced_size_file_copies and Image:
            assert resp['lossy_filename'] == filename
            assert resp['lossy_filename'] in os.listdir(self.reduced_files_path)
            assert get_size(png_file_path) > get_size(png_reduced_file_path)
        else:
            assert resp['lossy_filename'] is None
            assert not os.path.isfile(png_reduced_file_path)
        format_ = self.preferred_lossy_audio_format
        filename = 'old_test.wav'
        lossy_filename = '%s.%s' % (os.path.splitext(filename)[0], format_)
        lossy_file_path = os.path.join(self.reduced_files_path, lossy_filename)
        wav_file_path = os.path.join(self.test_files_path, filename)
        wav_file_size = os.path.getsize(wav_file_path)
        wav_file_base64 = b64encode(open(wav_file_path).read())
        params = self.file_create_params_base64.copy()
        params.update({'filename': filename, 
           'base64_encoded_file': wav_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file_count = new_file_count
        new_file_count = Session.query(model.File).count()
        assert resp['filename'] == filename
        assert resp['MIME_type'] == 'audio/x-wav'
        assert resp['size'] == wav_file_size
        assert resp['enterer']['first_name'] == 'Admin'
        assert new_file_count == file_count + 1
        if self.create_reduced_size_file_copies and h.command_line_program_installed('ffmpeg'):
            assert resp['lossy_filename'] == lossy_filename
            assert resp['lossy_filename'] in os.listdir(self.reduced_files_path)
            assert get_size(wav_file_path) > get_size(lossy_file_path)
        else:
            assert resp['lossy_filename'] is None
            assert not os.path.isfile(lossy_file_path)
        return

    @nottest
    def test_new_search(self):
        """Tests that GET /files/new_search returns the search parameters for searching the files resource."""
        query_builder = SQLAQueryBuilder('File')
        response = self.app.get(url('/files/new_search'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['search_parameters'] == h.get_search_parameters(query_builder)