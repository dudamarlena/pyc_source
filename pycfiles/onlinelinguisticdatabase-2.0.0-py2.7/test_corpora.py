# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_corpora.py
# Compiled at: 2016-09-19 13:27:02
import datetime, logging, os, simplejson as json
from uuid import uuid4
from time import sleep
from nose.tools import nottest
from sqlalchemy.sql import desc
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import Corpus, CorpusBackup
log = logging.getLogger(__name__)

class TestCorporaController(TestController):

    def tearDown(self):
        TestController.tearDown(self, dirs_to_destroy=['user', 'corpus'])

    @nottest
    def test_index(self):
        """Tests that GET /corpora returns an array of all corpora and that order_by and pagination parameters work correctly."""

        def create_corpus_from_index(index):
            corpus = model.Corpus()
            corpus.name = 'Corpus %d' % index
            corpus.description = 'A corpus with %d rules' % index
            corpus.content = '1'
            return corpus

        corpora = [ create_corpus_from_index(i) for i in range(1, 101) ]
        Session.add_all(corpora)
        Session.commit()
        corpora = h.get_corpora(True)
        corpora_count = len(corpora)
        response = self.app.get(url('corpora'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == corpora_count
        assert resp[0]['name'] == 'Corpus 1'
        assert resp[0]['id'] == corpora[0].id
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('corpora'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['name'] == corpora[46].name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Corpus', 'order_by_attribute': 'name', 'order_by_direction': 'desc'}
        response = self.app.get(url('corpora'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted(corpora, key=lambda c: c.name, reverse=True)
        assert [ c.id for c in result_set ] == [ c['id'] for c in resp ]
        assert response.content_type == 'application/json'
        params = {'order_by_model': 'Corpus', 'order_by_attribute': 'name', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('corpora'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert result_set[46].name == resp['items'][0]['name']
        order_by_params = {'order_by_model': 'Corpus', 'order_by_attribute': 'name', 'order_by_direction': 'descending'}
        response = self.app.get(url('corpora'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Corpusist', 'order_by_attribute': 'nominal', 'order_by_direction': 'desc'}
        response = self.app.get(url('corpora'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == corpora[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('corpora'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('corpora'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /corpora creates a new corpus
        or returns an appropriate error if the input is invalid.

        """

        def create_form_from_index(index):
            form = model.Form()
            form.transcription = 'Form %d' % index
            translation = model.Translation()
            translation.transcription = 'Translation %d' % index
            form.translation = translation
            return form

        forms = [ create_form_from_index(i) for i in range(1, 10) ]
        Session.add_all(forms)
        Session.commit()
        forms = h.get_forms()
        half_forms = forms[:5]
        form_ids = [ form.id for form in forms ]
        half_form_ids = [ form.id for form in half_forms ]
        test_corpus_content = (',').join(map(str, half_form_ids))
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_view, status=403)
        resp = json.loads(response.body)
        assert resp['error'] == 'You are not authorized to access this resource.'
        assert response.content_type == 'application/json'
        assert os.listdir(self.corpora_path) == []
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert new_corpus_count == original_corpus_count + 1
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(form_ids)
        assert resp['form_search']['id'] == form_search_id
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus Chi', 
           'description': 'Covers a lot of the data, padre.', 
           'content': test_corpus_content, 
           'form_search': 123456789})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert new_corpus_count == corpus_count
        assert resp['errors']['form_search'] == 'There is no form search with id 123456789.'
        assert response.content_type == 'application/json'
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus Chi Squared', 
           'description': 'Covers a lot of the data, padre.', 
           'content': test_corpus_content + ',123456789'})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert new_corpus_count == corpus_count
        assert resp['errors'] == 'At least one form id in the content was invalid.'
        assert response.content_type == 'application/json'
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data, dude.', 
           'content': test_corpus_content})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert new_corpus_count == corpus_count
        assert resp['errors']['name'] == 'The submitted value for Corpus.name is not unique.'
        assert response.content_type == 'application/json'
        params = self.corpus_create_params.copy()
        params.update({'name': '', 
           'description': 'Covers a lot of the data, sista.', 
           'content': test_corpus_content})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert new_corpus_count == corpus_count
        assert resp['errors']['name'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        params = self.corpus_create_params.copy()
        params.update({'name': None, 
           'description': "Covers a lot of the data, young'un.", 
           'content': test_corpus_content})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert new_corpus_count == corpus_count
        assert resp['errors']['name'] == 'Please enter a value'
        assert response.content_type == 'application/json'
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus' * 200, 
           'description': 'Covers a lot of the data, squirrel salad.', 
           'content': test_corpus_content})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert new_corpus_count == corpus_count
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        assert response.content_type == 'application/json'
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus by contents', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content})
        params = json.dumps(params)
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert new_corpus_count == original_corpus_count + 1
        assert resp['name'] == 'Corpus by contents'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(half_form_ids)
        assert resp['form_search'] == None
        return

    @nottest
    def test_new(self):
        """Tests that GET /corpora/new returns data needed to create a new corpus."""
        t = h.generate_restricted_tag()
        Session.add(t)
        Session.commit()
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        data = {'tags': h.get_mini_dicts_getter('Tag')(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'form_searches': h.get_mini_dicts_getter('FormSearch')(), 
           'corpus_formats': h.corpus_formats.keys()}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        response = self.app.get(url('new_corpus'), status=403, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'You are not authorized to access this resource.'
        response = self.app.get(url('new_corpus'), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp['users'] == data['users']
        assert resp['form_searches'] == data['form_searches']
        assert resp['tags'] == data['tags']
        assert resp['corpus_formats'] == data['corpus_formats']
        assert response.content_type == 'application/json'
        params = {'form_searches': 'anything can go here!', 
           'tags': datetime.datetime.utcnow().isoformat(), 
           'users': h.get_most_recent_modification_datetime('User').isoformat()}
        response = self.app.get(url('new_corpus'), params, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['form_searches'] == data['form_searches']
        assert resp['tags'] == data['tags']
        assert resp['users'] == []
        assert resp['corpus_formats'] == data['corpus_formats']

    @nottest
    def test_update(self):
        """Tests that PUT /corpora/id updates the corpus with id=id."""

        def create_form_from_index(index):
            form = model.Form()
            form.transcription = 'Form %d' % index
            translation = model.Translation()
            translation.transcription = 'Translation %d' % index
            form.translation = translation
            return form

        forms = [ create_form_from_index(i) for i in range(1, 10) ]
        Session.add_all(forms)
        Session.commit()
        forms = h.get_forms()
        form_ids = [ form.id for form in forms ]
        test_corpus_content = (',').join(map(str, form_ids))
        new_test_corpus_content = (',').join(map(str, form_ids[:5]))
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        assert os.listdir(self.corpora_path) == []
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        original_datetime_modified = resp['datetime_modified']
        assert new_corpus_count == original_corpus_count + 1
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(form_ids)
        assert resp['form_search']['id'] == form_search_id
        sleep(1)
        orig_backup_count = Session.query(CorpusBackup).count()
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.  Best yet!', 
           'content': new_test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        response = self.app.put(url('corpus', id=corpus_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_backup_count = Session.query(CorpusBackup).count()
        datetime_modified = resp['datetime_modified']
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        assert corpus_count == new_corpus_count
        assert datetime_modified != original_datetime_modified
        assert resp['description'] == 'Covers a lot of the data.  Best yet!'
        assert resp['content'] == new_test_corpus_content
        assert response.content_type == 'application/json'
        assert orig_backup_count + 1 == new_backup_count
        assert response.content_type == 'application/json'
        backup = Session.query(CorpusBackup).filter(CorpusBackup.UUID == unicode(resp['UUID'])).order_by(desc(CorpusBackup.id)).first()
        assert backup.datetime_modified.isoformat() == original_datetime_modified
        assert backup.content == test_corpus_content
        sleep(1)
        response = self.app.put(url('corpus', id=corpus_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        our_corpus_datetime_modified = Session.query(Corpus).get(corpus_id).datetime_modified
        assert our_corpus_datetime_modified.isoformat() == datetime_modified
        assert corpus_count == new_corpus_count
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'

    @nottest
    def test_delete(self):
        """Tests that DELETE /corpora/id deletes the corpus with id=id."""
        corpus_count = Session.query(Corpus).count()
        corpus_backup_count = Session.query(CorpusBackup).count()

        def create_form_from_index(index):
            form = model.Form()
            form.transcription = 'Form %d' % index
            translation = model.Translation()
            translation.transcription = 'Translation %d' % index
            form.translation = translation
            return form

        forms = [ create_form_from_index(i) for i in range(1, 10) ]
        Session.add_all(forms)
        Session.commit()
        forms = h.get_forms()
        form_ids = [ form.id for form in forms ]
        test_corpus_content = (',').join(map(str, form_ids))
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        assert os.listdir(self.corpora_path) == []
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(form_ids)
        assert resp['form_search']['id'] == form_search_id
        new_corpus_count = Session.query(Corpus).count()
        new_corpus_backup_count = Session.query(CorpusBackup).count()
        assert new_corpus_count == corpus_count + 1
        assert new_corpus_backup_count == corpus_backup_count
        response = self.app.delete(url('corpus', id=corpus_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_count = new_corpus_count
        new_corpus_count = Session.query(Corpus).count()
        corpus_backup_count = new_corpus_backup_count
        new_corpus_backup_count = Session.query(CorpusBackup).count()
        assert new_corpus_count == corpus_count - 1
        assert new_corpus_backup_count == corpus_backup_count + 1
        assert resp['id'] == corpus_id
        assert response.content_type == 'application/json'
        assert not os.path.exists(corpus_dir)
        assert resp['content'] == test_corpus_content
        deleted_corpus = Session.query(Corpus).get(corpus_id)
        assert deleted_corpus == None
        backed_up_corpus = Session.query(CorpusBackup).filter(CorpusBackup.UUID == unicode(resp['UUID'])).first()
        assert backed_up_corpus.name == resp['name']
        modifier = json.loads(unicode(backed_up_corpus.modifier))
        assert modifier['first_name'] == 'Admin'
        assert backed_up_corpus.datetime_entered.isoformat() == resp['datetime_entered']
        assert backed_up_corpus.UUID == resp['UUID']
        id = 9999999999999
        response = self.app.delete(url('corpus', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no corpus with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('corpus', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_show(self):
        """Tests that GET /corpora/id returns the corpus with id=id or an appropriate error."""

        def create_form_from_index(index):
            form = model.Form()
            form.transcription = 'Form %d' % index
            translation = model.Translation()
            translation.transcription = 'Translation %d' % index
            form.translation = translation
            return form

        forms = [ create_form_from_index(i) for i in range(1, 10) ]
        Session.add_all(forms)
        Session.commit()
        forms = h.get_forms()
        form_ids = [ form.id for form in forms ]
        test_corpus_content = (',').join(map(str, form_ids))
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        assert os.listdir(self.corpora_path) == []
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_count = Session.query(Corpus).count()
        corpus_id = resp['id']
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(form_ids)
        assert resp['form_search']['id'] == form_search_id
        assert corpus_count == original_corpus_count + 1
        id = 100000000000
        response = self.app.get(url('corpus', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no corpus with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('corpus', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('corpus', id=corpus_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert resp['content'] == test_corpus_content
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /corpora/id/edit returns a JSON object of data necessary to edit the corpus with id=id.

        The JSON object is of the form {'corpus': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """

        def create_form_from_index(index):
            form = model.Form()
            form.transcription = 'Form %d' % index
            translation = model.Translation()
            translation.transcription = 'Translation %d' % index
            form.translation = translation
            return form

        forms = [ create_form_from_index(i) for i in range(1, 10) ]
        Session.add_all(forms)
        Session.commit()
        forms = h.get_forms()
        form_ids = [ form.id for form in forms ]
        test_corpus_content = (',').join(map(str, form_ids))
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        assert os.listdir(self.corpora_path) == []
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_count = Session.query(Corpus).count()
        corpus_id = resp['id']
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(form_ids)
        assert resp['form_search']['id'] == form_search_id
        assert corpus_count == original_corpus_count + 1
        response = self.app.get(url('edit_corpus', id=corpus_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_corpus', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no corpus with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_corpus', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        data = {'tags': h.get_mini_dicts_getter('Tag')(), 
           'users': h.get_mini_dicts_getter('User')(), 
           'form_searches': h.get_mini_dicts_getter('FormSearch')(), 
           'corpus_formats': h.corpus_formats.keys()}
        data = json.loads(json.dumps(data, cls=h.JSONOLDEncoder))
        response = self.app.get(url('edit_corpus', id=corpus_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['corpus']['name'] == 'Corpus'
        assert resp['data'] == data
        assert response.content_type == 'application/json'

    @nottest
    def test_history(self):
        """Tests that GET /corpora/id/history returns the corpus with id=id and its previous incarnations.
        
        The JSON object returned is of the form
        {'corpus': corpus, 'previous_versions': [...]}.

        """
        users = h.get_users()
        contributor_id = [ u for u in users if u.role == 'contributor' ][0].id
        administrator_id = [ u for u in users if u.role == 'administrator' ][0].id

        def create_form_from_index(index):
            form = model.Form()
            form.transcription = 'Form %d' % index
            translation = model.Translation()
            translation.transcription = 'Translation %d' % index
            form.translation = translation
            return form

        forms = [ create_form_from_index(i) for i in range(1, 10) ]
        Session.add_all(forms)
        Session.commit()
        forms = h.get_forms()
        form_ids = [ form.id for form in forms ]
        test_corpus_content = (',').join(map(str, form_ids))
        new_test_corpus_content = (',').join(map(str, form_ids[:5]))
        newest_test_corpus_content = (',').join(map(str, form_ids[:4]))
        query = {'filter': ['Form', 'transcription', 'regex', '[a-zA-Z]{3,}']}
        params = json.dumps({'name': 'form search', 
           'description': "This one's worth saving!", 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.', 
           'content': test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        assert os.listdir(self.corpora_path) == []
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_count = Session.query(Corpus).count()
        corpus_id = resp['id']
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_form_ids = sorted([ f.id for f in corpus.forms ])
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        original_datetime_modified = resp['datetime_modified']
        assert resp['name'] == 'Corpus'
        assert resp['description'] == 'Covers a lot of the data.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == test_corpus_content
        assert corpus_form_ids == sorted(form_ids)
        assert resp['form_search']['id'] == form_search_id
        assert corpus_count == original_corpus_count + 1
        sleep(1)
        orig_backup_count = Session.query(CorpusBackup).count()
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers a lot of the data.  Best yet!', 
           'content': new_test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        response = self.app.put(url('corpus', id=corpus_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_backup_count = Session.query(CorpusBackup).count()
        first_update_datetime_modified = datetime_modified = resp['datetime_modified']
        new_corpus_count = Session.query(Corpus).count()
        assert corpus_count == new_corpus_count
        assert datetime_modified != original_datetime_modified
        assert resp['description'] == 'Covers a lot of the data.  Best yet!'
        assert resp['content'] == new_test_corpus_content
        assert response.content_type == 'application/json'
        assert orig_backup_count + 1 == new_backup_count
        backup = Session.query(CorpusBackup).filter(CorpusBackup.UUID == unicode(resp['UUID'])).order_by(desc(CorpusBackup.id)).first()
        assert backup.datetime_modified.isoformat() == original_datetime_modified
        assert backup.content == test_corpus_content
        assert json.loads(backup.modifier)['first_name'] == 'Admin'
        assert response.content_type == 'application/json'
        sleep(1)
        orig_backup_count = Session.query(CorpusBackup).count()
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus', 
           'description': 'Covers even more data.  Better than ever!', 
           'content': newest_test_corpus_content, 
           'form_search': form_search_id})
        params = json.dumps(params)
        response = self.app.put(url('corpus', id=corpus_id), params, self.json_headers, self.extra_environ_contrib)
        resp = json.loads(response.body)
        backup_count = new_backup_count
        new_backup_count = Session.query(CorpusBackup).count()
        datetime_modified = resp['datetime_modified']
        new_corpus_count = Session.query(Corpus).count()
        assert corpus_count == new_corpus_count == 1
        assert datetime_modified != original_datetime_modified
        assert resp['description'] == 'Covers even more data.  Better than ever!'
        assert resp['content'] == newest_test_corpus_content
        assert resp['modifier']['id'] == contributor_id
        assert response.content_type == 'application/json'
        assert backup_count + 1 == new_backup_count
        backup = Session.query(CorpusBackup).filter(CorpusBackup.UUID == unicode(resp['UUID'])).order_by(desc(CorpusBackup.id)).first()
        assert backup.datetime_modified.isoformat() == first_update_datetime_modified
        assert backup.content == new_test_corpus_content
        assert json.loads(backup.modifier)['first_name'] == 'Admin'
        assert response.content_type == 'application/json'
        extra_environ = {'test.authentication.role': 'contributor', 'test.application_settings': True}
        response = self.app.get(url(controller='corpora', action='history', id=corpus_id), headers=self.json_headers, extra_environ=extra_environ)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert 'corpus' in resp
        assert 'previous_versions' in resp
        first_version = resp['previous_versions'][1]
        second_version = resp['previous_versions'][0]
        current_version = resp['corpus']
        assert first_version['name'] == 'Corpus'
        assert first_version['description'] == 'Covers a lot of the data.'
        assert first_version['enterer']['id'] == administrator_id
        assert first_version['modifier']['id'] == administrator_id
        assert first_version['datetime_modified'] <= second_version['datetime_modified']
        assert second_version['name'] == 'Corpus'
        assert second_version['description'] == 'Covers a lot of the data.  Best yet!'
        assert second_version['content'] == new_test_corpus_content
        assert second_version['enterer']['id'] == administrator_id
        assert second_version['modifier']['id'] == administrator_id
        assert second_version['datetime_modified'] <= current_version['datetime_modified']
        assert current_version['name'] == 'Corpus'
        assert current_version['description'] == 'Covers even more data.  Better than ever!'
        assert current_version['content'] == newest_test_corpus_content
        assert current_version['enterer']['id'] == administrator_id
        assert current_version['modifier']['id'] == contributor_id
        corpus_UUID = resp['corpus']['UUID']
        response = self.app.get(url(controller='corpora', action='history', id=corpus_UUID), headers=self.json_headers, extra_environ=extra_environ)
        resp_UUID = json.loads(response.body)
        assert resp == resp_UUID
        bad_id = 103
        bad_UUID = str(uuid4())
        response = self.app.get(url(controller='corpora', action='history', id=bad_id), headers=self.json_headers, extra_environ=extra_environ, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'No corpora or corpus backups match %d' % bad_id
        response = self.app.get(url(controller='corpora', action='history', id=bad_UUID), headers=self.json_headers, extra_environ=extra_environ, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'No corpora or corpus backups match %s' % bad_UUID
        response = self.app.delete(url('corpus', id=corpus_id), headers=self.json_headers, extra_environ=extra_environ)
        response = self.app.get(url(controller='corpora', action='history', id=corpus_UUID), headers=self.json_headers, extra_environ=extra_environ)
        by_UUID_resp = json.loads(response.body)
        assert by_UUID_resp['corpus'] == None
        assert len(by_UUID_resp['previous_versions']) == 3
        first_version = by_UUID_resp['previous_versions'][2]
        second_version = by_UUID_resp['previous_versions'][1]
        third_version = by_UUID_resp['previous_versions'][0]
        assert first_version['name'] == 'Corpus'
        assert first_version['description'] == 'Covers a lot of the data.'
        assert first_version['enterer']['id'] == administrator_id
        assert first_version['modifier']['id'] == administrator_id
        assert first_version['datetime_modified'] <= second_version['datetime_modified']
        assert second_version['name'] == 'Corpus'
        assert second_version['description'] == 'Covers a lot of the data.  Best yet!'
        assert second_version['content'] == new_test_corpus_content
        assert second_version['enterer']['id'] == administrator_id
        assert second_version['modifier']['id'] == administrator_id
        assert second_version['datetime_modified'] <= third_version['datetime_modified']
        assert third_version['name'] == 'Corpus'
        assert third_version['description'] == 'Covers even more data.  Better than ever!'
        assert third_version['content'] == newest_test_corpus_content
        assert third_version['enterer']['id'] == administrator_id
        assert third_version['modifier']['id'] == contributor_id
        response = self.app.get(url(controller='corpora', action='history', id=corpus_id), headers=self.json_headers, extra_environ=extra_environ)
        by_corpus_id_resp = json.loads(response.body)
        assert by_corpus_id_resp == by_UUID_resp
        return