# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_pages.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from time import sleep
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import Page
log = logging.getLogger(__name__)

class TestPagesController(TestController):
    md_contents = ('\n').join([
     'My Page',
     '=======',
     '',
     'Research Interests',
     '---------------------',
     '',
     '* Item 1',
     '* Item 2',
     ''])

    @nottest
    def test_index(self):
        """Tests that GET /pages returns an array of all pages and that order_by and pagination parameters work correctly."""

        def create_page_from_index(index):
            page = model.Page()
            page.name = 'page%d' % index
            page.markup_language = 'Markdown'
            page.content = self.md_contents
            return page

        pages = [ create_page_from_index(i) for i in range(1, 101) ]
        Session.add_all(pages)
        Session.commit()
        pages = h.get_pages(True)
        pages_count = len(pages)
        response = self.app.get(url('pages'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == pages_count
        assert resp[0]['name'] == 'page1'
        assert resp[0]['id'] == pages[0].id
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 23, 'page': 3}
        response = self.app.get(url('pages'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 23
        assert resp['items'][0]['name'] == pages[46].name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Page', 'order_by_attribute': 'name', 'order_by_direction': 'desc'}
        response = self.app.get(url('pages'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted([ p.name for p in pages ], reverse=True)
        assert result_set == [ p['name'] for p in resp ]
        params = {'order_by_model': 'Page', 'order_by_attribute': 'name', 'order_by_direction': 'desc', 
           'items_per_page': 23, 'page': 3}
        response = self.app.get(url('pages'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert result_set[46] == resp['items'][0]['name']
        order_by_params = {'order_by_model': 'Page', 'order_by_attribute': 'name', 'order_by_direction': 'descending'}
        response = self.app.get(url('pages'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Pageist', 'order_by_attribute': 'nominal', 'order_by_direction': 'desc'}
        response = self.app.get(url('pages'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == pages[0].id
        paginator = {'items_per_page': 'a', 'page': ''}
        response = self.app.get(url('pages'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter an integer value'
        assert resp['errors']['page'] == 'Please enter a value'
        paginator = {'items_per_page': 0, 'page': -1}
        response = self.app.get(url('pages'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['items_per_page'] == 'Please enter a number that is 1 or greater'
        assert resp['errors']['page'] == 'Please enter a number that is 1 or greater'
        assert response.content_type == 'application/json'

    @nottest
    def test_create(self):
        """Tests that POST /pages creates a new page
        or returns an appropriate error if the input is invalid.
        """
        original_page_count = Session.query(Page).count()
        params = self.page_create_params.copy()
        params.update({'name': 'page', 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_page_count = Session.query(Page).count()
        assert new_page_count == original_page_count + 1
        assert resp['name'] == 'page'
        assert resp['content'] == self.md_contents
        assert resp['html'] == h.get_HTML_from_contents(self.md_contents, 'Markdown')
        assert response.content_type == 'application/json'
        params = self.page_create_params.copy()
        params.update({'name': '', 
           'markup_language': 'markdownable', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'Please enter a value'
        assert resp['errors']['markup_language'] == "Value must be one of: Markdown; reStructuredText (not u'markdownable')"
        assert response.content_type == 'application/json'
        params = self.page_create_params.copy()
        params.update({'name': 'name' * 200, 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['name'] == 'Enter a value not more than 255 characters long'
        assert response.content_type == 'application/json'

    @nottest
    def test_new(self):
        """Tests that GET /pages/new returns the list of accepted markup languages."""
        response = self.app.get(url('new_page'), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp == {'markup_languages': list(h.markup_languages)}
        assert response.content_type == 'application/json'

    @nottest
    def test_update(self):
        """Tests that PUT /pages/id updates the page with id=id."""
        params = self.page_create_params.copy()
        params.update({'name': 'page', 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        page_count = Session.query(Page).count()
        page_id = resp['id']
        original_datetime_modified = resp['datetime_modified']
        sleep(1)
        params = self.page_create_params.copy()
        params.update({'name': 'Awesome Page', 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.put(url('page', id=page_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        datetime_modified = resp['datetime_modified']
        new_page_count = Session.query(Page).count()
        assert page_count == new_page_count
        assert datetime_modified != original_datetime_modified
        assert resp['name'] == 'Awesome Page'
        assert response.content_type == 'application/json'
        sleep(1)
        response = self.app.put(url('page', id=page_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        page_count = new_page_count
        new_page_count = Session.query(Page).count()
        our_page_datetime_modified = Session.query(Page).get(page_id).datetime_modified
        assert our_page_datetime_modified.isoformat() == datetime_modified
        assert page_count == new_page_count
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'

    @nottest
    def test_delete(self):
        """Tests that DELETE /pages/id deletes the page with id=id."""
        params = self.page_create_params.copy()
        params.update({'name': 'page', 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        page_count = Session.query(Page).count()
        page_id = resp['id']
        response = self.app.delete(url('page', id=page_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        new_page_count = Session.query(Page).count()
        assert new_page_count == page_count - 1
        assert resp['id'] == page_id
        assert response.content_type == 'application/json'
        deleted_page = Session.query(Page).get(page_id)
        assert deleted_page == None
        assert response.content_type == 'application/json'
        id = 9999999999999
        response = self.app.delete(url('page', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no page with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.delete(url('page', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        return

    @nottest
    def test_show(self):
        """Tests that GET /pages/id returns the page with id=id or an appropriate error."""
        params = self.page_create_params.copy()
        params.update({'name': 'page', 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        page_id = resp['id']
        id = 100000000000
        response = self.app.get(url('page', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no page with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('page', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('page', id=page_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == 'page'
        assert resp['content'] == self.md_contents
        assert response.content_type == 'application/json'

    @nottest
    def test_edit(self):
        """Tests that GET /pages/id/edit returns a JSON object of data necessary to edit the page with id=id.

        The JSON object is of the form {'page': {...}, 'data': {...}} or
        {'error': '...'} (with a 404 status code) depending on whether the id is
        valid or invalid/unspecified, respectively.
        """
        params = self.page_create_params.copy()
        params.update({'name': 'page', 
           'markup_language': 'Markdown', 
           'content': self.md_contents})
        params = json.dumps(params)
        response = self.app.post(url('pages'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        page_id = resp['id']
        response = self.app.get(url('edit_page', id=page_id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_page', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no page with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_page', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        response = self.app.get(url('edit_page', id=page_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['page']['name'] == 'page'
        assert resp['data'] == {'markup_languages': list(h.markup_languages)}
        assert response.content_type == 'application/json'