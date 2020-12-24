# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_syntacticcategories.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from time import sleep
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import SyntacticCategory
log = logging.getLogger(__name__)

class TestSyntacticcategoriesController(TestController):

    @nottest
    def test_index(self):
        """Tests that GET /syntacticcategories returns an array of all syntactic categories and that order_by and pagination parameters work correctly."""

        def create_syntactic_category_from_index(index):
            syntactic_category = model.SyntacticCategory()
            syntactic_category.name = 'sc%d' % index
            syntactic_category.type = 'lexical'
            syntactic_category.description = 'description %d' % index
            return syntactic_category

        syntactic_categories = [ create_syntactic_category_from_index(i) for i in range(1, 101) ]
        Session.add_all(syntactic_categories)
        Session.commit()
        syntactic_categories = h.get_syntactic_categories(True)
        syntactic_categories_count = len(syntactic_categories)
        response = self.app.get(url('syntacticcategories'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == syntactic_categories_count
        assert resp[0]['name'] == 'sc1'
        assert resp[0]['id'] == syntactic_categories[0].id
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('syntacticcategories'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['name'] == syntactic_categories[46].name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'SyntacticCategory', 'order_by_attribute': 'name', 'order_by_direction': 'desc'}
        response = self.app.get(url('syntacticcategories'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted([ sc.name for sc in syntactic_categories ], reverse=True)
        assert result_set == [ sc['name'] for sc in resp ]
        params = {'order_by_model': 'SyntacticCategory', 'order_by_attribute': 'name', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('syntacticcategories'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert result_set[46] == resp['items'][0]['name']
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'SyntacticCategory', 'order_by_attribute': 'name', 'order_by_direction': 'descending'}
        response = self.app.get(url('syntacticcategories'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'SyntacticCategoryist', 'order_by_attribute': 'nominal', 'order_by_direction': 'desc'}
        response = self.app.get(url('syntacticcategories'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == syntactic_categories[0].id
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('syntacticcategories'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('syntacticcategories'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /syntacticcategories creates a new syntactic category
        or returns an appropriate error if the input is invalid.
        """
        original_SC_count = Session.query(SyntacticCategory).count()
        params = json.dumps({'name': 'sc', 'type': 'lexical', 'description': 'Described.'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_SC_count = Session.query(SyntacticCategory).count()
        assert new_SC_count == original_SC_count + 1
        assert resp['name'] == 'sc'
        assert resp['description'] == 'Described.'
        assert resp['type'] == 'lexical'
        assert response.content_type == 'application/json'
        params = json.dumps({'name': 'sc', 'type': 'lexical', 'description': 'Described.'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'The submitted value for SyntacticCategory.name is not unique.'
        assert response.content_type == 'application/json'
        params = json.dumps({'name': '', 'type': 'lexical', 'description': 'Described.'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'Please enter a value'
        params = json.dumps({'name': 'name' * 400, 'type': 'lexical', 'description': 'Described.'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        params = json.dumps({'name': 'name' * 400, 'type': 'spatial', 'description': 'Described.'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['type'] == "Value must be one of: lexical; phrasal; sentential (not u'spatial')"
        assert response.content_type == 'application/json'

    @nottest
    def test_new(self):
        """Tests that GET /syntacticcategories/new returns an empty JSON object."""
        response = self.app.get(url('new_syntacticcategory'), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp['syntactic_category_types'] == list(h.syntactic_category_types)
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /syntacticcategories/id updates the syntacticcategory with id=id."""
        params = json.dumps({'name': 'name', 'type': 'lexical', 'description': 'description'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        syntactic_category_count = Session.query(SyntacticCategory).count()
        syntactic_category_id = resp['id']
        original_datetime_modified = resp['datetime_modified']
        sleep(1)
        params = json.dumps({'name': 'name', 'type': 'lexical', 'description': 'More content-ful description.'})
        response = self.app.put(url('syntacticcategory', id=syntactic_category_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        datetime_modified = resp['datetime_modified']
        new_syntactic_category_count = Session.query(SyntacticCategory).count()
        assert syntactic_category_count == new_syntactic_category_count
        assert datetime_modified != original_datetime_modified
        assert response.content_type == 'application/json'
        sleep(1)
        response = self.app.put(url('syntacticcategory', id=syntactic_category_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        syntactic_category_count = new_syntactic_category_count
        new_syntactic_category_count = Session.query(SyntacticCategory).count()
        our_SC_datetime_modified = Session.query(SyntacticCategory).get(syntactic_category_id).datetime_modified
        assert our_SC_datetime_modified.isoformat() == datetime_modified
        assert syntactic_category_count == new_syntactic_category_count
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'

    @nottest
    def test_delete(self):
        """Tests that DELETE /syntacticcategories/id deletes the syntactic_category with id=id."""
        params = json.dumps({'name': 'name', 'type': 'lexical', 'description': 'description'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        syntactic_category_count = Session.query(SyntacticCategory).count()
        syntactic_category_id = resp['id']
        response = self.app.delete(url('syntacticcategory', id=syntactic_category_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        new_syntactic_category_count = Session.query(SyntacticCategory).count()
        assert new_syntactic_category_count == syntactic_category_count - 1
        assert resp['id'] == syntactic_category_id
        assert response.content_type == 'application/json'
        deleted_syntactic_category = Session.query(SyntacticCategory).get(syntactic_category_id)
        assert deleted_syntactic_category == None
        id = 9999999999999
        response = self.app.delete(url('syntacticcategory', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no syntactic category with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('syntacticcategory', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_show(self):
        """Tests that GET /syntacticcategories/id returns the syntactic category with id=id or an appropriate error."""
        params = json.dumps({'name': 'name', 'type': 'lexical', 'description': 'description'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        syntactic_category_id = resp['id']
        id = 100000000000
        response = self.app.get(url('syntacticcategory', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no syntactic category with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('syntacticcategory', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('syntacticcategory', id=syntactic_category_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'name'
        assert resp['description'] == 'description'
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /syntacticcategories/id/edit returns a JSON object of data necessary to edit the syntactic category with id=id.

        The JSON object is of the form {'syntactic_category': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        params = json.dumps({'name': 'name', 'type': 'lexical', 'description': 'description'})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        syntactic_category_id = resp['id']
        response = self.app.get(url('edit_syntacticcategory', id=syntactic_category_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_syntacticcategory', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no syntactic category with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_syntacticcategory', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_syntacticcategory', id=syntactic_category_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['syntactic_category']['name'] == 'name'
        assert resp['data']['syntactic_category_types'] == list(h.syntactic_category_types)
        assert response.content_type == 'application/json'

    @nottest
    def test_category_percolation(self):
        """Tests that changes to a category's name and deletion of a category trigger updates to forms containing morphemes of that category.
        """
        application_settings = h.generate_default_application_settings()
        Session.add(application_settings)
        Session.commit()
        extra_environ = {'test.authentication.role': 'administrator', 'test.application_settings': True}
        params = json.dumps({'name': 'N', 'type': 'lexical', 'description': ''})
        response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        NId = resp['id']
        assert resp['name'] == 'N'
        assert response.content_type == 'application/json'
        params = self.form_create_params.copy()
        params.update({'transcription': 'chien', 
           'morpheme_break': 'chien', 
           'morpheme_gloss': 'dog', 
           'translations': [{'transcription': 'dog', 'grammaticality': ''}], 'syntactic_category': NId})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        chien_id = resp['id']
        assert resp['morpheme_break_ids'][0][0][0][1] == 'dog'
        assert resp['morpheme_break_ids'][0][0][0][2] == 'N'
        assert resp['morpheme_gloss_ids'][0][0][0][1] == 'chien'
        assert resp['morpheme_gloss_ids'][0][0][0][2] == 'N'
        assert resp['syntactic_category_string'] == 'N'
        assert resp['break_gloss_category'] == 'chien|dog|N'
        params = self.form_create_params.copy()
        params.update({'transcription': 'chiens', 
           'morpheme_break': 'chien-s', 
           'morpheme_gloss': 'dog-PL', 
           'translations': [{'transcription': 'dogs', 'grammaticality': ''}], 'syntactic_category': NId})
        params = json.dumps(params)
        response = self.app.post(url('forms'), params, self.json_headers, extra_environ)
        resp = json.loads(response.body)
        chiens_id = resp['id']
        assert resp['morpheme_break_ids'][0][0][0][1] == 'dog'
        assert resp['morpheme_break_ids'][0][0][0][2] == 'N'
        assert resp['morpheme_gloss_ids'][0][0][0][1] == 'chien'
        assert resp['morpheme_gloss_ids'][0][0][0][2] == 'N'
        assert resp['syntactic_category_string'] == 'N-?'
        assert resp['break_gloss_category'] == 'chien|dog|N-s|PL|?'
        form_backup_count = Session.query(model.FormBackup).count()
        params = json.dumps({'name': 'Noun', 'type': 'lexical', 'description': ''})
        response = self.app.put(url('syntacticcategory', id=NId), params, self.json_headers, extra_environ)
        new_form_backup_count = Session.query(model.FormBackup).count()
        chien = Session.query(model.Form).get(chien_id)
        chiens = Session.query(model.Form).get(chiens_id)
        assert new_form_backup_count == form_backup_count + 2
        assert chien.syntactic_category_string == 'Noun'
        assert chiens.syntactic_category_string == 'Noun-?'
        assert json.loads(chiens.morpheme_break_ids)[0][0][0][2] == 'Noun'
        params = json.dumps({'name': 'Noun', 'type': 'lexical', 'description': 'Blah!'})
        response = self.app.put(url('syntacticcategory', id=NId), params, self.json_headers, extra_environ)
        form_backup_count = new_form_backup_count
        new_form_backup_count = Session.query(model.FormBackup).count()
        chien = chiens = None
        chien = Session.query(model.Form).get(chien_id)
        chiens = Session.query(model.Form).get(chiens_id)
        assert new_form_backup_count == form_backup_count
        assert chien.syntactic_category_string == 'Noun'
        assert chiens.syntactic_category_string == 'Noun-?'
        assert json.loads(chiens.morpheme_break_ids)[0][0][0][2] == 'Noun'
        response = self.app.delete(url('syntacticcategory', id=NId), headers=self.json_headers, extra_environ=extra_environ)
        form_backup_count = new_form_backup_count
        new_form_backup_count = Session.query(model.FormBackup).count()
        chien = chiens = None
        chien = Session.query(model.Form).get(chien_id)
        chiens = Session.query(model.Form).get(chiens_id)
        assert new_form_backup_count == form_backup_count + 2
        assert chien.syntactic_category == None
        assert chien.syntactic_category_string == '?'
        assert chiens.syntactic_category_string == '?-?'
        assert json.loads(chiens.morpheme_break_ids)[0][0][0][2] == None
        return