# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_oldcollections.py
# Compiled at: 2016-09-19 13:27:02
import datetime, logging, os, simplejson as json
from time import sleep
from nose.tools import nottest
from base64 import encodestring
from sqlalchemy.sql import desc
from uuid import uuid4
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)

class TestOldcollectionsController(TestController):

    def tearDown(self):
        TestController.tearDown(self, dirs_to_clear=['reduced_files_path', 'files_path'], del_global_app_set=True)

    @nottest
    def test_index(self):
        """Tests that GET /collections returns a JSON array of collections with expected values."""
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
        params = self.collection_create_params.copy()
        params.update({'title': 'Restricted Collection', 
           'tags': [
                  h.get_tags()[0].id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        restricted_collection_id = resp['id']
        params = self.collection_create_params.copy()
        params.update({'title': 'Unrestricted Collection'})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        assert resp[0]['title'] == 'Restricted Collection'
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 1
        application_settings = h.get_application_settings()
        application_settings.unrestricted_users = []
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True, 
           'test.retain_application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 1
        restricted_collection = Session.query(model.Collection).get(restricted_collection_id)
        restricted_collection.tags = []
        Session.add(restricted_collection)
        Session.commit()
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 2
        h.clear_all_models(['User', 'Tag', 'Language'])

        def create_collection_from_index(index):
            collection = model.Collection()
            collection.title = 'title %d' % index
            return collection

        collections = [ create_collection_from_index(i) for i in range(1, 101) ]
        Session.add_all(collections)
        Session.commit()
        collections = h.get_models_by_name('Collection', True)
        restricted_tag = h.get_restricted_tag()
        for collection in collections:
            if int(collection.title.split(' ')[1]) % 2 == 0:
                collection.tags.append(restricted_tag)
            Session.add(collection)

        Session.commit()
        collections = h.get_models_by_name('Collection', True)
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp) == 100
        assert resp[0]['title'] == 'title 1'
        assert resp[0]['id'] == collections[0].id
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('collections'), paginator, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['title'] == collections[46].title
        order_by_params = {'order_by_model': 'Collection', 'order_by_attribute': 'title', 'order_by_direction': 'desc'}
        response = self.app.get(url('collections'), order_by_params, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        result_set = sorted([ c.title for c in collections ], reverse=True)
        assert result_set == [ f['title'] for f in resp ]
        params = {'order_by_model': 'Collection', 'order_by_attribute': 'title', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('collections'), params, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert result_set[46] == resp['items'][0]['title']
        assert response.content_type == 'application/json'
        items_per_page = 7
        page = 7
        paginator = {'items_per_page': items_per_page, 'page': page}
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('collections'), paginator, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp['items']) == items_per_page
        assert resp['items'][0]['title'] == 'title %d' % (items_per_page * (page - 1) * 2 + 1)
        order_by_params = {'order_by_model': 'Collection', 'order_by_attribute': 'title', 'order_by_direction': 'descending'}
        response = self.app.get(url('collections'), order_by_params, status=400, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        order_by_params = {'order_by_model': 'Collectionissimo', 'order_by_attribute': 'tutelage', 'order_by_direction': 'desc'}
        response = self.app.get(url('collections'), order_by_params, headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert resp[0]['id'] == collections[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('collections'), paginator, headers=self.json_headers, extra_environ=extra_environ, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('collections'), paginator, headers=self.json_headers, extra_environ=extra_environ, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'

    @nottest
    def test_create(self):
        """Tests that POST /collections correctly creates a new collection."""
        params = '"a'
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'JSON decode error: the parameters provided were not valid JSON.'
        tag1 = model.Tag()
        tag2 = model.Tag()
        restricted_tag = h.generate_restricted_tag()
        tag1.name = 'tag 1'
        tag2.name = 'tag 2'
        Session.add_all([tag1, tag2, restricted_tag])
        Session.commit()
        tag1_id = tag1.id
        tag2_id = tag2.id
        restricted_tag_id = restricted_tag.id
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        params = self.file_create_params.copy()
        params.update({'filename': 'old_test.wav', 
           'base64_encoded_file': encodestring(open(wav_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file1_id = resp['id']
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_base64 = encodestring(open(jpg_file_path).read())
        params = self.file_create_params.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file2_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'transcription 1', 
           'translations': [{'transcription': 'translation 1', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form1_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'transcription 2', 
           'translations': [{'transcription': 'translation 2', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form2_id = resp['id']
        md_contents1 = ('\n').join([
         '### Chapter 1',
         '',
         '#### Section 1',
         '',
         '* Item 1',
         '* Item 2',
         '',
         '#### Section 2',
         '',
         'form[%d]' % form1_id,
         'form[%d]' % form2_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'Chapter 1', 
           'markup_language': 'Markdown', 
           'contents': md_contents1, 
           'files': [
                   file1_id, file2_id], 
           'tags': [
                  tag1_id, tag2_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        collection1_id = resp['id']
        collection_count = Session.query(model.Collection).count()
        assert type(resp) == type({})
        assert resp['title'] == 'Chapter 1'
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['html'] == h.markup_language_to_func['Markdown'](md_contents1)
        assert sorted([ f['id'] for f in resp['files'] ]) == sorted([file1_id, file2_id])
        assert sorted([ t['id'] for t in resp['tags'] ]) == sorted([tag1_id, tag2_id])
        assert sorted([ f['id'] for f in resp['forms'] ]) == sorted([form1_id, form2_id])
        assert collection_count == 1
        assert response.content_type == 'application/json'
        params = self.form_create_params.copy()
        params.update({'transcription': 'transcription 3', 
           'translations': [{'transcription': 'translation 3', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form3_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'transcription 4', 
           'translations': [{'transcription': 'translation 4', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form4_id = resp['id']
        md_contents2 = ('\n').join([
         '## Book 1',
         '',
         'collection[%d]' % collection1_id,
         '',
         '### Chapter 2',
         '',
         'form[%d]' % form3_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'Book 1', 
           'markup_language': 'Markdown', 
           'contents': md_contents2})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        collection2_id = resp['id']
        collection_count = Session.query(model.Collection).count()
        collection2_contents_unpacked = md_contents2.replace('collection[%d]' % collection1_id, md_contents1)
        assert type(resp) == type({})
        assert resp['title'] == 'Book 1'
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['contents_unpacked'] == collection2_contents_unpacked
        assert resp['html'] == h.markup_language_to_func['Markdown'](collection2_contents_unpacked)
        assert resp['files'] == []
        assert resp['tags'] == []
        assert sorted([ f['id'] for f in resp['forms'] ]) == sorted([form1_id, form2_id, form3_id])
        assert collection_count == 2
        assert response.content_type == 'application/json'
        md_contents3 = ('\n').join([
         '# Title',
         '',
         'collection(%d)' % collection2_id,
         '',
         '## Book 2',
         '',
         '### Chapter 3',
         '',
         'form[%d]' % form4_id])
        params3 = self.collection_create_params.copy()
        params3.update({'title': 'Novel', 
           'markup_language': 'Markdown', 
           'contents': md_contents3})
        params3 = json.dumps(params3)
        response = self.app.post(url('collections'), params3, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        collection3_id = resp['id']
        collection_count = Session.query(model.Collection).count()
        collection3_contents_unpacked = md_contents3.replace('collection(%d)' % collection2_id, collection2_contents_unpacked)
        assert type(resp) == type({})
        assert resp['title'] == 'Novel'
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['contents_unpacked'] == collection3_contents_unpacked
        assert resp['html'] == h.markup_language_to_func['Markdown'](collection3_contents_unpacked)
        assert resp['files'] == []
        assert resp['tags'] == []
        assert sorted([ f['id'] for f in resp['forms'] ]) == sorted([form1_id, form2_id, form3_id, form4_id])
        assert collection_count == 3
        assert response.content_type == 'application/json'
        response = self.app.put(url('collection', id=collection3_id), params3, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        collection2 = Session.query(model.Collection).get(collection2_id)
        collection2_form_ids = [ f.id for f in collection2.forms ]
        collection2_datetime_modified = collection2.datetime_modified
        collection2_HTML = collection2.html
        collection2_backups_count = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection2_id).count()
        collection3 = Session.query(model.Collection).get(collection3_id)
        collection3_form_ids = [ f.id for f in collection3.forms ]
        collection3_datetime_modified = collection3.datetime_modified
        collection3_HTML = collection3.html
        collection3_backups_count = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection3_id).count()
        sleep(1)
        md_contents1 = ('\n').join([
         '### Chapter 1',
         '',
         '#### Section 1',
         '',
         '* Item 1',
         '* Item 2',
         '',
         '#### Section 2',
         '',
         'form[%d]' % form2_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'Chapter 1', 
           'markup_language': 'Markdown', 
           'contents': md_contents1, 
           'files': [
                   file1_id, file2_id], 
           'tags': [
                  tag1_id, tag2_id, restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection1_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_collection2 = Session.query(model.Collection).get(collection2_id)
        new_collection2_form_ids = [ f.id for f in new_collection2.forms ]
        new_collection2_datetime_modified = new_collection2.datetime_modified
        new_collection2_HTML = new_collection2.html
        new_collection2_contents = new_collection2.contents
        new_collection2_backups = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection2_id).all()
        new_collection2_backups_count = len(new_collection2_backups)
        new_collection3 = Session.query(model.Collection).get(collection3_id)
        new_collection3_form_ids = [ f.id for f in new_collection3.forms ]
        new_collection3_datetime_modified = new_collection3.datetime_modified
        new_collection3_HTML = new_collection3.html
        new_collection3_backups = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection3_id).all()
        new_collection3_backups_count = len(new_collection3_backups)
        assert form1_id not in [ f['id'] for f in resp['forms'] ]
        assert sorted(collection2_form_ids) != sorted(new_collection2_form_ids)
        assert form1_id in collection2_form_ids
        assert form1_id not in new_collection2_form_ids
        assert collection2_datetime_modified != new_collection2_datetime_modified
        assert collection2_HTML != new_collection2_HTML
        assert sorted(collection3_form_ids) != sorted(new_collection3_form_ids)
        assert form1_id in collection3_form_ids
        assert form1_id not in new_collection3_form_ids
        assert collection3_datetime_modified != new_collection3_datetime_modified
        assert collection3_HTML != new_collection3_HTML
        assert new_collection2_backups_count == collection2_backups_count + 1
        assert new_collection3_backups_count == collection3_backups_count + 1
        assert form1_id not in [ f.id for f in new_collection2.forms ]
        assert form1_id in json.loads(new_collection2_backups[0].forms)
        assert form1_id not in [ f.id for f in new_collection3.forms ]
        assert form1_id in json.loads(new_collection3_backups[0].forms)
        response = self.app.put(url('collection', id=collection3_id), params3, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        response = self.app.delete(url('collection', id=collection1_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        old_collection2_contents = new_collection2_contents
        new_collection2 = Session.query(model.Collection).get(collection2_id)
        new_collection2_contents = new_collection2.contents
        collection1_ref = 'collection[%d]' % collection1_id
        old_collection2_backups_count = new_collection2_backups_count
        new_collection2_backups = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection2_id).order_by(desc(model.CollectionBackup.id)).all()
        new_collection2_backups_count = len(new_collection2_backups)
        assert collection1_ref in old_collection2_contents
        assert collection1_ref not in new_collection2_contents
        assert new_collection2_backups_count == old_collection2_backups_count + 1
        assert collection1_ref in new_collection2_backups[0].contents
        params3 = json.loads(params3)
        params3.update({'title': 'A Great Novel'})
        params3 = json.dumps(params3)
        response = self.app.put(url('collection', id=collection3_id), params3, self.json_headers, self.extra_environ_admin)
        collection2 = Session.query(model.Collection).get(collection2_id)
        collection3 = Session.query(model.Collection).get(collection3_id)
        collection2_contents = collection2.contents
        collection2_HTML = collection2.html
        collection2_forms = [ f.id for f in collection2.forms ]
        collection3_forms = [ f.id for f in collection3.forms ]
        collection3_contents_unpacked = collection3.contents_unpacked
        collection3_HTML = collection3.html
        collection2_backups_count = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection2_id).count()
        collection3_backups_count = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection3_id).count()
        response = self.app.delete(url('form', id=form3_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        new_collection2 = Session.query(model.Collection).get(collection2_id)
        new_collection3 = Session.query(model.Collection).get(collection3_id)
        new_collection2_contents = new_collection2.contents
        new_collection2_forms = [ f.id for f in new_collection2.forms ]
        new_collection2_HTML = new_collection2.html
        new_collection3_forms = [ f.id for f in new_collection3.forms ]
        new_collection3_contents_unpacked = new_collection3.contents_unpacked
        new_collection3_HTML = new_collection3.html
        new_collection2_backups_count = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection2_id).count()
        new_collection3_backups_count = Session.query(model.CollectionBackup).filter(model.CollectionBackup.collection_id == collection3_id).count()
        assert 'form[%d]' % form3_id in collection2_contents
        assert 'form[%d]' % form3_id in collection2_HTML
        assert 'form[%d]' % form3_id in collection3_contents_unpacked
        assert 'form[%d]' % form3_id in collection3_HTML
        assert 'form[%d]' % form3_id not in new_collection2_contents
        assert 'form[%d]' % form3_id not in new_collection2_HTML
        assert 'form[%d]' % form3_id not in new_collection3_contents_unpacked
        assert 'form[%d]' % form3_id not in new_collection3_HTML
        assert form3_id in collection2_forms
        assert form3_id in collection3_forms
        assert form3_id not in new_collection2_forms
        assert form3_id not in new_collection3_forms
        assert new_collection2_backups_count == collection2_backups_count + 1
        assert new_collection3_backups_count == collection3_backups_count + 1

    @nottest
    def test_create_invalid(self):
        """Tests that POST /collections with invalid input returns an appropriate error."""
        collection_count = Session.query(model.Collection).count()
        params = self.collection_create_params.copy()
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        assert resp['errors']['title'] == 'Please enter a value'
        assert new_collection_count == collection_count
        params = self.collection_create_params.copy()
        params.update({'title': 'test create invalid title' * 100, 
           'url': 'test_create_invalid_url' * 100})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        too_long_error = 'Enter a value not more than 255 characters long'
        assert resp['errors']['title'] == too_long_error
        assert resp['errors']['url'] == 'The input is not valid'
        assert new_collection_count == collection_count
        assert response.content_type == 'application/json'
        application_settings = h.generate_default_application_settings()
        Session.add(application_settings)
        Session.commit()
        extra_environ = self.extra_environ_admin.copy()
        extra_environ['test.application_settings'] = True
        bad_URL = 'bad&url'
        bad_markup_language = 'rtf'
        bad_collection_type = 'novella'
        params = self.collection_create_params.copy()
        params.update({'title': 'test create invalid title', 
           'url': bad_URL, 
           'markup_language': bad_markup_language, 
           'type': bad_collection_type})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ=extra_environ, status=400)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        assert resp['errors']['url'] == 'The input is not valid'
        assert resp['errors']['markup_language'] == "Value must be one of: Markdown; reStructuredText (not u'rtf')"
        assert resp['errors']['type'] == "Value must be one of: story; elicitation; paper; discourse; other (not u'novella')"
        assert new_collection_count == collection_count
        assert response.content_type == 'application/json'
        params = self.collection_create_params.copy()
        params.update({'title': 'test create valid title', 
           'url': 'good-url/really', 
           'markup_language': 'reStructuredText', 
           'type': 'paper'})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        assert resp['url'] == 'good-url/really'
        assert resp['type'] == 'paper'
        assert resp['markup_language'] == 'reStructuredText'
        assert new_collection_count == collection_count + 1
        bad_id = 109
        bad_int = 'abc'
        params = self.collection_create_params.copy()
        params.update({'title': 'test create invalid title', 
           'speaker': bad_id, 
           'elicitor': bad_int, 
           'source': bad_int})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ=extra_environ, status=400)
        resp = json.loads(response.body)
        collection_count = new_collection_count
        new_collection_count = Session.query(model.Collection).count()
        assert resp['errors']['speaker'] == 'There is no speaker with id %d.' % bad_id
        assert resp['errors']['elicitor'] == 'Please enter an integer value'
        assert resp['errors']['source'] == 'Please enter an integer value'
        assert new_collection_count == collection_count
        assert response.content_type == 'application/json'
        speaker = h.generate_default_speaker()
        source = h.generate_default_source()
        Session.add_all([speaker, source])
        Session.commit()
        contributor = Session.query(model.User).filter(model.User.role == 'contributor').first()
        params = self.collection_create_params.copy()
        params.update({'title': 'test create title', 
           'speaker': h.get_speakers()[0].id, 
           'elicitor': contributor.id, 
           'source': h.get_sources()[0].id})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        assert resp['source']['year'] == source.year
        assert resp['speaker']['first_name'] == speaker.first_name
        assert resp['elicitor']['first_name'] == contributor.first_name
        assert new_collection_count == collection_count + 1

    @nottest
    def test_relational_restrictions(self):
        """Tests that the restricted tag works correctly with respect to relational attributes of collections.

        That is, tests that (a) users are not able to access restricted forms or
        files via collection.forms and collection.files respectively since
        collections associated to restricted forms or files are automatically
        tagged as restricted; and (b) a restricted user cannot append a restricted
        form or file to a collection."""
        admin = self.extra_environ_admin.copy()
        admin.update({'test.application_settings': True})
        contrib = self.extra_environ_contrib.copy()
        contrib.update({'test.application_settings': True})
        params = self.collection_create_params.copy()
        original_title = 'test_update_title'
        params.update({'title': original_title})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert resp['title'] == original_title
        assert collection_count == 1
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        restricted_tag_id = restricted_tag.id
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        wav_file_base64 = encodestring(open(wav_file_path).read())
        params = self.file_create_params.copy()
        params.update({'filename': 'restricted_file.wav', 
           'base64_encoded_file': wav_file_base64, 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        restricted_file_id = resp['id']
        params = self.file_create_params.copy()
        params.update({'filename': 'unrestricted_file.wav', 
           'base64_encoded_file': wav_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        unrestricted_file_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'restricted', 
           'translations': [{'transcription': 'restricted', 'grammaticality': ''}], 'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        restricted_form_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'unrestricted', 
           'translations': [{'transcription': 'unrestricted', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        unrestricted_form_id = resp['id']
        params = self.collection_create_params.copy()
        params.update({'title': 'test', 
           'files': [
                   restricted_file_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, contrib, status=400)
        resp = json.loads(response.body)
        assert 'You are not authorized to access the file with id %d.' % restricted_file_id in resp['errors']['files']
        assert response.content_type == 'application/json'
        md_contents = ('\n').join([
         'Chapter',
         '=======',
         '',
         'Section',
         '-------',
         '',
         '* Item 1',
         '* Item 2',
         '',
         'Section containing forms',
         '------------------------',
         '',
         'form[%d]' % restricted_form_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'test', 
           'markup_language': 'Markdown', 
           'contents': md_contents})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, contrib, status=400)
        resp = json.loads(response.body)
        assert 'You are not authorized to access the form with id %d.' % restricted_form_id in resp['errors']['forms']
        params = self.collection_create_params.copy()
        params.update({'title': 'test', 
           'files': [
                   unrestricted_file_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        unrestricted_collection_id = resp['id']
        assert resp['title'] == 'test'
        assert resp['files'][0]['name'] == 'unrestricted_file.wav'
        assert response.content_type == 'application/json'
        md_contents = ('\n').join([
         'Chapter',
         '=======',
         '',
         'Section',
         '-------',
         '',
         '* Item 1',
         '* Item 2',
         '',
         'Section containing forms',
         '------------------------',
         '',
         'form[%d]' % unrestricted_form_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'test', 
           'markup_language': 'Markdown', 
           'contents': md_contents})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, contrib)
        resp = json.loads(response.body)
        assert resp['forms'][0]['transcription'] == 'unrestricted'
        params = self.collection_create_params.copy()
        params.update({'title': 'test', 
           'files': [
                   restricted_file_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        indirectly_restricted_collection1_id = resp['id']
        assert resp['title'] == 'test'
        assert resp['files'][0]['name'] == 'restricted_file.wav'
        assert 'restricted' in [ t['name'] for t in resp['tags'] ]
        assert response.content_type == 'application/json'
        md_contents = ('\n').join([
         'Chapter',
         '=======',
         '',
         'Section',
         '-------',
         '',
         '* Item 1',
         '* Item 2',
         '',
         'Section containing forms',
         '------------------------',
         '',
         'form[%d]' % restricted_form_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'test', 
           'markup_language': 'Markdown', 
           'contents': md_contents})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        indirectly_restricted_collection2_id = resp['id']
        assert resp['title'] == 'test'
        assert resp['forms'][0]['transcription'] == 'restricted'
        assert 'restricted' in [ t['name'] for t in resp['tags'] ]
        assert response.content_type == 'application/json'
        response = self.app.get(url('collections'), headers=self.json_headers, extra_environ=contrib)
        resp = json.loads(response.body)
        assert indirectly_restricted_collection1_id not in [ c['id'] for c in resp ]
        assert indirectly_restricted_collection2_id not in [ c['id'] for c in resp ]
        unrestricted_collection_params = self.collection_create_params.copy()
        unrestricted_collection_params.update({'title': 'test'})
        params = json.dumps(unrestricted_collection_params)
        response = self.app.post(url('collections'), params, self.json_headers, admin)
        resp = json.loads(response.body)
        unrestricted_collection_id = resp['id']
        assert resp['title'] == 'test'
        unrestricted_collection_params.update({'files': [restricted_file_id]})
        params = json.dumps(unrestricted_collection_params)
        response = self.app.put(url('collection', id=unrestricted_collection_id), params, self.json_headers, contrib, status=400)
        resp = json.loads(response.body)
        assert 'You are not authorized to access the file with id %d.' % restricted_file_id in resp['errors']['files']
        response = self.app.put(url('collection', id=unrestricted_collection_id), params, self.json_headers, admin)
        resp = json.loads(response.body)
        assert resp['id'] == unrestricted_collection_id
        assert 'restricted' in [ t['name'] for t in resp['tags'] ]
        assert response.content_type == 'application/json'
        response = self.app.get(url('collection', id=unrestricted_collection_id), headers=self.json_headers, extra_environ=contrib, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        h.clear_directory_of_files(self.files_path)

    @nottest
    def test_new(self):
        """Tests that GET /collection/new returns an appropriate JSON object for creating a new OLD collection.

        The properties of the JSON object are 'speakers', 'users', 'tags',
        'sources', 'collection_types', 'markup_languages' and their values are
        arrays/lists.
        """
        extra_environ = {'test.authentication.role': 'viewer'}
        response = self.app.get(url('new_collection'), extra_environ=extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        application_settings = h.generate_default_application_settings()
        foreign_word_tag = h.generate_foreign_word_tag()
        restricted_tag = h.generate_restricted_tag()
        speaker = h.generate_default_speaker()
        source = h.generate_default_source()
        Session.add_all([application_settings, foreign_word_tag, restricted_tag,
         speaker, source])
        Session.commit()
        data = {'speakers': h.get_mini_dicts_getter('Speaker')(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'tags': h.get_mini_dicts_getter('Tag')(), 
           'sources': h.get_mini_dicts_getter('Source')()}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        response = self.app.get(url('new_collection'), extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['tags'] == data['tags']
        assert resp['speakers'] == data['speakers']
        assert resp['users'] == data['users']
        assert resp['sources'] == data['sources']
        assert set(resp['collection_types']) == set(h.collection_types)
        assert set(resp['markup_languages']) == set(h.markup_languages)
        assert response.content_type == 'application/json'
        params = {'speakers': '', 
           'sources': 'anything can go here!', 
           'tags': datetime.datetime.utcnow().isoformat(), 
           'users': h.get_most_recent_modification_datetime('User').isoformat()}
        response = self.app.get(url('new_collection'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['speakers'] == []
        assert resp['sources'] == data['sources']
        assert resp['tags'] == data['tags']
        assert resp['users'] == []
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /collections/id correctly updates an existing collection."""
        collection_count = Session.query(model.Collection).count()
        restricted_tag = h.generate_restricted_tag()
        application_settings = h.generate_default_application_settings()
        Session.add_all([application_settings, restricted_tag])
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        restricted_tag_id = restricted_tag.id
        params = self.collection_create_params.copy()
        original_title = 'test_update_title'
        params.update({'title': original_title, 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        id = int(resp['id'])
        new_collection_count = Session.query(model.Collection).count()
        assert resp['title'] == original_title
        assert new_collection_count == collection_count + 1
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated!'})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=id), params, self.json_headers, extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated!'})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=id), params, self.json_headers, extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        orig_backup_count = Session.query(model.CollectionBackup).count()
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated!'})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        new_backup_count = Session.query(model.CollectionBackup).count()
        assert resp['title'] == 'Updated!'
        assert new_collection_count == collection_count + 1
        assert orig_backup_count + 1 == new_backup_count
        backup = Session.query(model.CollectionBackup).filter(model.CollectionBackup.UUID == unicode(resp['UUID'])).order_by(desc(model.CollectionBackup.id)).first()
        assert backup.datetime_modified.isoformat() <= resp['datetime_modified']
        assert backup.title == original_title
        assert response.content_type == 'application/json'
        orig_backup_count = Session.query(model.CollectionBackup).count()
        response = self.app.put(url('collection', id=id), params, self.json_headers, self.extra_environ_admin, status=400)
        new_backup_count = Session.query(model.CollectionBackup).count()
        resp = json.loads(response.body)
        assert orig_backup_count == new_backup_count
        assert 'the submitted data were not new' in resp['error']
        assert response.content_type == 'application/json'
        speaker = h.generate_default_speaker()
        Session.add(speaker)
        Session.commit()
        speaker = h.get_speakers()[0]
        speaker_id = speaker.id
        speaker_first_name = speaker.first_name
        params = self.collection_create_params.copy()
        params.update({'title': 'Another title', 
           'speaker': speaker_id})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=id), params, self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert resp['speaker']['first_name'] == speaker_first_name
        assert response.content_type == 'application/json'
        collection_count_at_start = Session.query(model.Collection).count()
        tag1 = model.Tag()
        tag2 = model.Tag()
        tag1.name = 'tag 1'
        tag2.name = 'tag 2'
        Session.add_all([tag1, tag2])
        Session.commit()
        tag1_id = tag1.id
        tag2_id = tag2.id
        wav_file_path = os.path.join(self.test_files_path, 'old_test.wav')
        params = self.file_create_params.copy()
        params.update({'filename': 'old_test.wav', 
           'base64_encoded_file': encodestring(open(wav_file_path).read())})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file1_id = resp['id']
        jpg_file_path = os.path.join(self.test_files_path, 'old_test.jpg')
        jpg_file_base64 = encodestring(open(jpg_file_path).read())
        params = self.file_create_params.copy()
        params.update({'filename': 'old_test.jpg', 
           'base64_encoded_file': jpg_file_base64})
        params = json.dumps(params)
        response = self.app.post(url('files'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        file2_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'transcription 1', 
           'translations': [{'transcription': 'translation 1', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form1_id = resp['id']
        params = self.form_create_params.copy()
        params.update({'transcription': 'transcription 2', 
           'translations': [{'transcription': 'translation 2', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form2_id = resp['id']
        md_contents = ('\n').join([
         'Chapter',
         '=======',
         '',
         'Section',
         '-------',
         '',
         '* Item 1',
         '* Item 2',
         '',
         'Section containing forms',
         '------------------------',
         '',
         'form[%d]' % form1_id,
         'form[%d]' % form2_id])
        params = self.collection_create_params.copy()
        params.update({'title': 'test_create_title', 
           'markup_language': 'Markdown', 
           'contents': md_contents, 
           'files': [
                   file1_id, file2_id], 
           'tags': [
                  restricted_tag_id, tag1_id, tag2_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        created_collection_id = resp['id']
        collection_count = Session.query(model.Collection).count()
        assert resp['title'] == 'test_create_title'
        assert resp['enterer']['first_name'] == 'Admin'
        assert resp['html'] == h.markup_language_to_func['Markdown'](md_contents)
        assert sorted([ f['id'] for f in resp['files'] ]) == sorted([file1_id, file2_id])
        assert sorted([ t['id'] for t in resp['tags'] ]) == sorted([tag1_id, tag2_id, restricted_tag_id])
        assert sorted([ f['id'] for f in resp['forms'] ]) == sorted([form1_id, form2_id])
        assert collection_count == collection_count_at_start + 1
        assert response.content_type == 'application/json'
        tags = [ t.id for t in h.get_tags() ]
        tags.reverse()
        files = [ f.id for f in h.get_files() ]
        files.reverse()
        params = self.collection_create_params.copy()
        params.update({'title': 'test_create_title', 
           'markup_language': 'Markdown', 
           'contents': md_contents, 
           'tags': tags, 
           'files': files})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=created_collection_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'
        params = self.collection_create_params.copy()
        params.update({'title': 'test_create_title', 
           'markup_language': 'Markdown', 
           'contents': md_contents, 
           'tags': tags, 
           'files': files[0:1]})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=created_collection_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        assert new_collection_count == collection_count
        assert len(resp['files']) == 1
        assert restricted_tag.name in [ t['name'] for t in resp['tags'] ]
        assert response.content_type == 'application/json'
        params = self.collection_create_params.copy()
        params.update({'title': 'test_create_title', 
           'markup_language': 'Markdown', 
           'contents': md_contents, 
           'tags': [
                  1000, 9875, 'abcdef'], 
           'files': [
                   44, '1t']})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin, status=400)
        collection_count = new_collection_count
        new_collection_count = Session.query(model.Collection).count()
        resp = json.loads(response.body)
        assert new_collection_count == collection_count
        assert 'Please enter an integer value' in resp['errors']['files']
        assert 'There is no file with id 44.' in resp['errors']['files']
        assert 'There is no tag with id 1000.' in resp['errors']['tags']
        assert 'There is no tag with id 9875.' in resp['errors']['tags']
        assert 'Please enter an integer value' in resp['errors']['tags']
        assert response.content_type == 'application/json'

    @nottest
    def test_delete(self):
        """Tests that DELETE /collections/id deletes the collection with id=id and returns a JSON representation.

        If the id is invalid or unspecified, then JSON null or a 404 status code
        are returned, respectively.
        """
        original_contributor_id = Session.query(model.User).filter(model.User.role == 'contributor').first().id
        application_settings = h.generate_default_application_settings()
        speaker = h.generate_default_speaker()
        my_contributor = h.generate_default_user()
        my_contributor.username = 'uniqueusername'
        tag = model.Tag()
        tag.name = 'default tag'
        file = h.generate_default_file()
        Session.add_all([application_settings, speaker, my_contributor, tag, file])
        Session.commit()
        my_contributor = Session.query(model.User).filter(model.User.username == 'uniqueusername').first()
        my_contributor_id = my_contributor.id
        my_contributor_first_name = my_contributor.first_name
        tag_id = tag.id
        file_id = file.id
        speaker_id = speaker.id
        speaker_first_name = speaker.first_name
        params = self.form_create_params.copy()
        params.update({'transcription': 'test_delete_transcription', 
           'translations': [{'transcription': 'test_delete_translation', 'grammaticality': ''}]})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_id = resp['id']
        collection_count = Session.query(model.Collection).count()
        collection_backup_count = Session.query(model.CollectionBackup).count()
        md_contents = ('\n').join([
         'Chapter',
         '=======',
         '',
         'Section',
         '-------',
         '',
         '* Item 1',
         '* Item 2',
         '',
         'Section containing forms',
         '------------------------',
         '',
         'form[%d]' % form_id])
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Test Delete', 
           'speaker': speaker_id, 
           'tags': [
                  tag_id], 
           'files': [
                   file_id], 
           'markup_language': 'Markdown', 
           'contents': md_contents})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        to_delete_id = resp['id']
        assert resp['title'] == 'Test Delete'
        assert resp['speaker']['first_name'] == speaker_first_name
        assert resp['tags'][0]['name'] == 'default tag'
        assert resp['files'][0]['name'] == 'test_file_name'
        assert resp['forms'][0]['transcription'] == 'test_delete_transcription'
        new_collection_count = Session.query(model.Collection).count()
        new_collection_backup_count = Session.query(model.CollectionBackup).count()
        assert new_collection_count == collection_count + 1
        assert new_collection_backup_count == collection_backup_count
        extra_environ = {'test.authentication.id': original_contributor_id, 'test.application_settings': True}
        response = self.app.delete(url('collection', id=to_delete_id), extra_environ=extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.delete(url('collection', id=to_delete_id), extra_environ=extra_environ)
        resp = json.loads(response.body)
        new_collection_count = Session.query(model.Collection).count()
        new_collection_backup_count = Session.query(model.CollectionBackup).count()
        tag_of_deleted_collection = Session.query(model.Tag).get(resp['tags'][0]['id'])
        file_of_deleted_collection = Session.query(model.File).get(resp['files'][0]['id'])
        speaker_of_deleted_collection = Session.query(model.Speaker).get(resp['speaker']['id'])
        assert isinstance(tag_of_deleted_collection, model.Tag)
        assert isinstance(file_of_deleted_collection, model.File)
        assert isinstance(speaker_of_deleted_collection, model.Speaker)
        assert new_collection_count == collection_count
        assert new_collection_backup_count == collection_backup_count + 1
        assert response.content_type == 'application/json'
        assert resp['title'] == 'Test Delete'
        deleted_collection = Session.query(model.Collection).get(to_delete_id)
        assert deleted_collection == None
        backed_up_collection = Session.query(model.CollectionBackup).filter(model.CollectionBackup.UUID == unicode(resp['UUID'])).first()
        assert backed_up_collection.title == resp['title']
        modifier = json.loads(unicode(backed_up_collection.modifier))
        assert modifier['first_name'] == my_contributor_first_name
        backed_up_speaker = json.loads(unicode(backed_up_collection.speaker))
        assert backed_up_speaker['first_name'] == speaker_first_name
        assert backed_up_collection.datetime_entered.isoformat() == resp['datetime_entered']
        assert backed_up_collection.UUID == resp['UUID']
        assert response.content_type == 'application/json'
        id = 9999999999999
        response = self.app.delete(url('collection', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no collection with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('collection', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_show(self):
        """Tests that GET /collection/id returns a JSON collection object, null or 404
        depending on whether the id is valid, invalid or unspecified, respectively.
        """
        collection = model.Collection()
        collection.title = 'Title'
        Session.add(collection)
        Session.commit()
        collection_id = h.get_models_by_name('Collection')[0].id
        id = 100000000000
        response = self.app.get(url('collection', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no collection with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('collection', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('collection', id=collection_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['title'] == 'Title'
        assert response.content_type == 'application/json'
        users = h.get_users()
        contributor_id = [ u for u in users if u.role == 'contributor' ][0].id
        restricted_tag = h.generate_restricted_tag()
        my_contributor = h.generate_default_user()
        my_contributor_first_name = 'Mycontributor'
        my_contributor.first_name = my_contributor_first_name
        my_contributor.username = 'uniqueusername'
        Session.add_all([restricted_tag, my_contributor])
        Session.commit()
        my_contributor_id = my_contributor.id
        restricted_tag_id = restricted_tag.id
        application_settings = h.generate_default_application_settings()
        application_settings.unrestricted_users = [my_contributor]
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Test Restricted Tag', 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        restricted_collection_id = resp['id']
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        response = self.app.get(url('collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=extra_environ)
        extra_environ = {'test.authentication.id': contributor_id, 'test.application_settings': True}
        response = self.app.get(url('collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=extra_environ)
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.get(url('collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=extra_environ)
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=extra_environ, status=403)
        application_settings = h.get_application_settings()
        application_settings.unrestricted_users = []
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.id': my_contributor_id, 'test.application_settings': True}
        response = self.app.get(url('collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=extra_environ, status=403)
        assert response.content_type == 'application/json'
        restricted_collection = Session.query(model.Collection).get(restricted_collection_id)
        restricted_collection.tags = []
        Session.add(restricted_collection)
        Session.commit()
        extra_environ = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url('collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=extra_environ)
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /collections/id/edit returns a JSON object of data necessary to edit the collection with id=id.

        The JSON object is of the form {'collection': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        application_settings = h.generate_default_application_settings()
        restricted_tag = h.generate_restricted_tag()
        Session.add_all([restricted_tag, application_settings])
        Session.commit()
        restricted_tag = h.get_restricted_tag()
        collection = model.Collection()
        collection.title = 'Test'
        collection.tags = [restricted_tag]
        Session.add(collection)
        Session.commit()
        restricted_collection_id = collection.id
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        response = self.app.get(url('edit_collection', id=restricted_collection_id), extra_environ=extra_environ, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_collection', id=restricted_collection_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_collection', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no collection with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_collection', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_collection', id=restricted_collection_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['collection']['title'] == 'Test'
        assert response.content_type == 'application/json'
        application_settings = h.generate_default_application_settings()
        foreign_word_tag = h.generate_foreign_word_tag()
        speaker = h.generate_default_speaker()
        source = h.generate_default_source()
        Session.add_all([application_settings, foreign_word_tag, speaker, source])
        Session.commit()
        data = {'speakers': h.get_mini_dicts_getter('Speaker')(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'tags': h.get_mini_dicts_getter('Tag')(), 
           'sources': h.get_mini_dicts_getter('Source')()}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        params = {'tags': 'give me some tags!', 
           'speakers': '', 
           'sources': datetime.datetime.utcnow().isoformat(), 
           'users': h.get_most_recent_modification_datetime('User').isoformat()}
        response = self.app.get(url('edit_collection', id=restricted_collection_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['data']['tags'] == data['tags']
        assert resp['data']['speakers'] == []
        assert resp['data']['users'] == []
        assert resp['data']['sources'] == data['sources']
        assert set(resp['data']['collection_types']) == set(h.collection_types)
        assert set(resp['data']['markup_languages']) == set(h.markup_languages)
        assert response.content_type == 'application/json'
        params = {'speakers': 'True'}
        response = self.app.get(url('edit_collection', id=id), params, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no collection with id %s' % id in json.loads(response.body)['error']

    @nottest
    def test_history(self):
        """Tests that GET /collections/id/history returns the collection with id=id and its previous incarnations.

        The JSON object returned is of the form
        {'collection': collection, 'previous_versions': [...]}.
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
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Created by the Contributor', 
           'elicitor': contributor_id, 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, extra_environ)
        collection_count = Session.query(model.Collection).count()
        resp = json.loads(response.body)
        collection_id = resp['id']
        collection_UUID = resp['UUID']
        assert collection_count == 1
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'url': 'find/me/here', 
           'title': 'Updated by the Administrator', 
           'speaker': speaker_id, 
           'tags': tag_ids + [None, ''], 
           'enterer': administrator_id})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert collection_count == 1
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        params = self.collection_create_params.copy()
        params.update({'title': 'Updated by the Contributor', 
           'speaker': speaker_id, 
           'tags': tag_ids, 
           'files': file_ids})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        assert collection_count == 1
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        response = self.app.get(url(controller='oldcollections', action='history', id=collection_id), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert 'collection' in resp
        assert 'previous_versions' in resp
        first_version = resp['previous_versions'][1]
        second_version = resp['previous_versions'][0]
        current_version = resp['collection']
        assert first_version['title'] == 'Created by the Contributor'
        assert first_version['elicitor']['id'] == contributor_id
        assert first_version['enterer']['id'] == contributor_id
        assert first_version['modifier']['id'] == contributor_id
        assert first_version['datetime_modified'] <= second_version['datetime_modified']
        assert first_version['speaker'] == None
        assert [ t['id'] for t in first_version['tags'] ] == [restricted_tag_id]
        assert first_version['files'] == []
        assert response.content_type == 'application/json'
        assert second_version['title'] == 'Updated by the Administrator'
        assert second_version['elicitor'] == None
        assert second_version['enterer']['id'] == contributor_id
        assert second_version['modifier']['id'] == administrator_id
        assert second_version['datetime_modified'] <= current_version['datetime_modified']
        assert second_version['speaker']['id'] == speaker_id
        assert sorted([ t['id'] for t in second_version['tags'] ]) == sorted(tag_ids)
        assert second_version['files'] == []
        assert current_version['title'] == 'Updated by the Contributor'
        assert current_version['elicitor'] == None
        assert current_version['enterer']['id'] == contributor_id
        assert current_version['speaker']['id'] == speaker_id
        assert current_version['modifier']['id'] == contributor_id
        assert sorted([ t['id'] for t in current_version['tags'] ]) == sorted(tag_ids)
        assert sorted([ f['id'] for f in current_version['files'] ]) == sorted(file_ids)
        extra_environ_viewer = {'test.authentication.role': 'viewer', 'test.application_settings': True}
        response = self.app.get(url(controller='oldcollections', action='history', id=collection_id), headers=self.json_headers, extra_environ=extra_environ_viewer, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        bad_id = 103
        bad_UUID = str(uuid4())
        response = self.app.get(url(controller='oldcollections', action='history', id=bad_id), headers=self.json_headers, extra_environ=extra_environ, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'No collections or collection backups match %d' % bad_id
        response = self.app.get(url(controller='oldcollections', action='history', id=bad_UUID), headers=self.json_headers, extra_environ=extra_environ, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'No collections or collection backups match %s' % bad_UUID
        response = self.app.delete(url('collection', id=collection_id), headers=self.json_headers, extra_environ=extra_environ)
        response = self.app.get(url(controller='oldcollections', action='history', id=collection_UUID), headers=self.json_headers, extra_environ=extra_environ)
        by_UUID_resp = json.loads(response.body)
        assert by_UUID_resp['collection'] == None
        assert len(by_UUID_resp['previous_versions']) == 3
        first_version = by_UUID_resp['previous_versions'][2]
        second_version = by_UUID_resp['previous_versions'][1]
        third_version = by_UUID_resp['previous_versions'][0]
        assert first_version['title'] == 'Created by the Contributor'
        assert first_version['elicitor']['id'] == contributor_id
        assert first_version['enterer']['id'] == contributor_id
        assert first_version['modifier']['id'] == contributor_id
        assert first_version['datetime_modified'] <= second_version['datetime_modified']
        assert first_version['speaker'] == None
        assert [ t['id'] for t in first_version['tags'] ] == [restricted_tag_id]
        assert first_version['files'] == []
        assert second_version['title'] == 'Updated by the Administrator'
        assert second_version['elicitor'] == None
        assert second_version['enterer']['id'] == contributor_id
        assert second_version['modifier']['id'] == administrator_id
        assert second_version['datetime_modified'] <= third_version['datetime_modified']
        assert second_version['speaker']['id'] == speaker_id
        assert sorted([ t['id'] for t in second_version['tags'] ]) == sorted(tag_ids)
        assert second_version['files'] == []
        assert third_version['title'] == 'Updated by the Contributor'
        assert third_version['elicitor'] == None
        assert third_version['enterer']['id'] == contributor_id
        assert third_version['modifier']['id'] == contributor_id
        assert third_version['speaker']['id'] == speaker_id
        assert sorted([ t['id'] for t in third_version['tags'] ]) == sorted(tag_ids)
        assert sorted([ f['id'] for f in third_version['files'] ]) == sorted(file_ids)
        response = self.app.get(url(controller='oldcollections', action='history', id=collection_id), headers=self.json_headers, extra_environ=extra_environ)
        by_collection_id_resp = json.loads(response.body)
        assert by_collection_id_resp == by_UUID_resp
        params = self.collection_create_params.copy()
        params.update({'title': '2nd collection restricted', 
           'tags': [
                  restricted_tag_id]})
        params = json.dumps(params)
        response = self.app.post(url('collections'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        collection_count = Session.query(model.Collection).count()
        collection_id = resp['id']
        collection_UUID = resp['UUID']
        assert collection_count == 1
        params = self.collection_create_params.copy()
        params.update({'title': '2nd collection unrestricted', 
           'tags': []})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        params = self.collection_create_params.copy()
        params.update({'title': '2nd collection unrestricted updated', 
           'tags': []})
        params = json.dumps(params)
        response = self.app.put(url('collection', id=collection_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        response = self.app.get(url(controller='oldcollections', action='history', id=collection_id), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert len(resp['previous_versions']) == 1
        assert resp['previous_versions'][0]['title'] == '2nd collection unrestricted'
        assert resp['collection']['title'] == '2nd collection unrestricted updated'
        assert response.content_type == 'application/json'
        response = self.app.get(url(controller='oldcollections', action='history', id=collection_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp['previous_versions']) == 2
        assert resp['previous_versions'][0]['title'] == '2nd collection unrestricted'
        assert resp['previous_versions'][1]['title'] == '2nd collection restricted'
        assert resp['collection']['title'] == '2nd collection unrestricted updated'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_new_search(self):
        """Tests that GET /collections/new_search returns the search parameters for searching the collections resource."""
        query_builder = SQLAQueryBuilder('Collection')
        response = self.app.get(url('/collections/new_search'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['search_parameters'] == h.get_search_parameters(query_builder)