# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/test_lib.py
# Compiled at: 2020-03-13 10:57:40
# Size of source mod 2**32: 5720 bytes
"""Tests for the Timesketch API client"""
from __future__ import unicode_literals
import json

def mock_session():
    """Mock HTTP requests session."""

    class MockHeaders(object):
        __doc__ = 'Mock requests HTTP headers.'

        @staticmethod
        def update(*args, **kwargs):
            """Mock header update method."""
            pass

    class MockSession(object):
        __doc__ = 'Mock HTTP requests session.'

        def __init__(self):
            """Initializes the mock Session object."""
            self.verify = False
            self.headers = MockHeaders()
            self._post_done = False

        @staticmethod
        def get(*args, **kwargs):
            """Mock GET request handler."""
            return mock_response(*args, **kwargs)

        def post(self, *args, **kwargs):
            """Mock POST request handler."""
            if self._post_done:
                return mock_response(*args, empty=True)
            return mock_response(*args, **kwargs)

    return MockSession()


def mock_response(*args, **kwargs):
    """Mocks HTTP response."""

    class MockResponse(object):
        __doc__ = 'Mock HTTP response object.'

        def __init__(self, json_data=None, text_data=None, status_code=200):
            """Initializes mock object."""
            self.json_data = json_data
            self.text = text_data
            self.status_code = status_code

        def json(self):
            """Mock JSON response."""
            return self.json_data

    auth_text_data = '<input id="csrf_token" name="csrf_token" value="test">'
    sketch_data = {'meta': {'views': [
                        {'id': 1, 
                         'name': 'test'},
                        {'id': 2, 
                         'name': 'test'}], 
              
              'es_time': 41444}, 
     
     'objects': [
                 {'id': 1, 
                  
                  'name': 'test', 
                  'description': 'test', 
                  'timelines': [
                                {'id': 1, 
                                 'name': 'test', 
                                 'searchindex': {'index_name': 'test'}},
                                {'id': 2, 
                                 'name': 'test', 
                                 'searchindex': {'index_name': 'test'}}]}]}
    sketch_list_data = {'meta': {'es_time': 324}, 
     'objects': [sketch_data['objects']]}
    timeline_data = {'meta': {'es_time': 12}, 
     
     'objects': [
                 {'id': 1, 
                  'name': 'test', 
                  'searchindex': {'index_name': 'test'}}]}
    empty_data = {'meta': {'es_time': 0}, 
     'objects': []}
    story_list_data = {'meta': {'es_time': 23}, 
     'objects': [[{'id': 1}]]}
    story_data = {'meta': {'es_time': 1}, 
     
     'objects': [
                 {'title': 'My First Story', 
                  'content': json.dumps([
                              {'componentName': '', 
                               'componentProps': {}, 
                               'content': '# My Heading\nWith Some Text.', 
                               'edit': False, 
                               'showPanel': False, 
                               'isActive': False},
                              {'componentName': 'TsViewEventList', 
                               'componentProps': {'view': {'id': 1, 
                                                           'name': 'Smoking Gun'}}, 
                               
                               'content': '', 
                               'edit': False, 
                               'showPanel': False, 
                               'isActive': False},
                              {'componentName': '', 
                               'componentProps': {}, 
                               'content': '... and that was the true crime.', 
                               'edit': False, 
                               'showPanel': False, 
                               'isActive': False}])}]}
    url_router = {'http://127.0.0.1': MockResponse(text_data=auth_text_data), 
     
     'http://127.0.0.1/api/v1/sketches/': MockResponse(json_data=sketch_list_data), 
     
     'http://127.0.0.1/api/v1/sketches/1': MockResponse(json_data=sketch_data), 
     
     'http://127.0.0.1/api/v1/sketches/1/timelines/1': MockResponse(json_data=timeline_data), 
     
     'http://127.0.0.1/api/v1/sketches/1/explore/': MockResponse(json_data=timeline_data), 
     
     'http://127.0.0.1/api/v1/sketches/1/stories/': MockResponse(json_data=story_list_data), 
     
     'http://127.0.0.1/api/v1/sketches/1/stories/1/': MockResponse(json_data=story_data)}
    if kwargs.get('empty', False):
        return MockResponse(text_data=empty_data)
    return url_router.get(args[0], MockResponse(None, 404))