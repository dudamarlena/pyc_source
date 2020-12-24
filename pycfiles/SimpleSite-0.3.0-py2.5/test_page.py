# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesite/tests/functional/test_page.py
# Compiled at: 2008-11-04 09:44:40
from simplesite.tests import *
from routes import url_for
from simplesite.model import meta
from urlparse import urlparse

class TestPageController(TestController):

    def test_save_prohibit_get(self):
        """Tests to ensure that GET requests are prohibited"""
        response = self.app.get(url=url_for(controller='page', action='save', id='1'), params={'heading': 'Updated Heading', 
           'title': 'Updated Title', 
           'content': 'Updated Content'}, status=405)

    def test_save_404_invalid_id(self):
        """Tests that a 404 response is returned if no ID is specified
        or if the ID doesn't exist"""
        response = self.app.post(url=url_for(controller='page', action='save', id=''), params={'heading': 'Updated Heading', 
           'title': 'Updated Title', 
           'content': 'Updated Content'}, status=404)
        response = self.app.post(url=url_for(controller='page', action='save', id='2'), params={'heading': 'Updated Heading', 
           'title': 'Updated Title', 
           'content': 'Updated Content'}, status=404)

    def test_save_invalid_form_data(self):
        """Tests that invalid data results in the form being returned with
        error messages"""
        response = self.app.post(url=url_for(controller='page', action='save', id='1'), params={'heading': 'Updated Heading', 
           'title': '', 
           'content': 'Updated Content'})
        assert 'Please enter a value' in response

    def test_save(self):
        """Tests that valid data is saved to the database, that the response redirects
        to the view() action and that a flash message is set in the session"""
        response = self.app.post(url=url_for(controller='page', action='save', id='1'), params={'heading': 'Updated Heading', 
           'title': 'Updated Title', 
           'content': 'Updated Content'})
        connection = meta.engine.connect()
        result = connection.execute('\n            SELECT heading, title, content\n            FROM page\n            WHERE id=?\n            ', (1, ))
        connection.close()
        row = result.fetchone()
        assert row.heading == 'Updated Heading'
        assert row.title == 'Updated Title'
        assert row.content == 'Updated Content'
        assert response.session['flash'] == 'Page successfully updated.'
        assert urlparse(response.response.location).path == url_for(controller='page', action='view', id=1)
        assert response.status == 302