# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_languages.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from nose.tools import nottest
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
log = logging.getLogger(__name__)

class TestLanguagesController(TestController):

    @nottest
    def test_index(self):
        """Tests that GET & SEARCH /languages behave correctly.
        
        NOTE: during testing, the language table contains only 8 records.
        """
        languages = Session.query(model.Language).all()
        response = self.app.get(url('languages'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == len(languages)
        assert response.content_type == 'application/json'
        paginator = {'items_per_page': 2, 'page': 2}
        response = self.app.get(url('languages'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 2
        assert resp['items'][0]['Part2B'] == languages[2].Part2B
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'Language', 'order_by_attribute': 'Ref_Name', 'order_by_direction': 'desc'}
        response = self.app.get(url('languages'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = sorted(languages, key=lambda l: l.Ref_Name, reverse=True)
        assert [ l['Id'] for l in resp ] == [ l.Id for l in result_set ]
        params = {'order_by_model': 'Language', 'order_by_attribute': 'Ref_Name', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('languages'), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert result_set[2].Ref_Name == resp['items'][0]['Ref_Name']
        assert response.content_type == 'application/json'
        response = self.app.get(url('language', id=languages[4].Id), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['Ref_Name'] == languages[4].Ref_Name
        assert response.content_type == 'application/json'
        response = self.app.get(url('language', id=100987), headers=self.json_headers, extra_environ=self.extra_environ_view, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no language with Id 100987'
        assert response.content_type == 'application/json'
        self._add_SEARCH_to_web_test_valid_methods()
        json_query = json.dumps({'query': {'filter': [
                              'Language', 'Ref_Name', 'like', '%m%']}})
        response = self.app.post(url('/languages/search'), json_query, self.json_headers, self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = [ l for l in languages if 'm' in l.Ref_Name ]
        assert resp
        assert set([ l['Id'] for l in resp ]) == set([ l.Id for l in result_set ])
        assert response.content_type == 'application/json'
        json_query = json.dumps({'query': {'filter': [
                              'Language', 'Ref_Name', 'like', '%l%']}})
        response = self.app.request(url('languages'), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
        resp = json.loads(response.body)
        result_set = [ l for l in languages if 'l' in l.Ref_Name ]
        assert resp
        assert len(resp) == len(result_set)
        assert set([ l['Id'] for l in resp ]) == set([ l.Id for l in result_set ])
        response = self.app.get(url('edit_language', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('new_language', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        response = self.app.post(url('languages'), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        response = self.app.put(url('language', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'
        response = self.app.delete(url('language', id=2232), status=404)
        assert json.loads(response.body)['error'] == 'This resource is read-only.'
        assert response.content_type == 'application/json'

    @nottest
    def test_new_search(self):
        """Tests that GET /languages/new_search returns the search parameters for searching the languages resource."""
        query_builder = SQLAQueryBuilder('Language')
        response = self.app.get(url('/languages/new_search'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['search_parameters'] == h.get_search_parameters(query_builder)