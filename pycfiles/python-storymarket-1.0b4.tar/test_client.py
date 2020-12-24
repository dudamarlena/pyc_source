# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-storymarket/tests/test_client.py
# Compiled at: 2010-07-12 17:00:55
"""
Tests for the parts of StorymarketClient not otherwise covered.
"""
import mock, storymarket, httplib2
from nose.tools import assert_raises
client = storymarket.StorymarketClient('APIKEY')

def test_json_encoding():
    mock_resp = httplib2.Response({'status': 200})
    mock_body = '{"hi": "there"}'
    mock_req = mock.Mock(return_value=(mock_resp, mock_body))
    with mock.patch('httplib2.Http.request', mock_req):
        client.request('/url/', 'POST', body={'hello': ['world']})
        mock_req.assert_called_with('%surl/' % client.BASE_URL, 'POST', body='{"hello": ["world"]}', headers={'Authorization': client.apikey, 
           'Content-Type': 'application/json', 
           'User-Agent': client.USER_AGENT})


def test_error_response():
    mock_resp = httplib2.Response({'status': 400})
    mock_body = 'oops!'
    mock_req = mock.Mock(return_value=(mock_resp, mock_body))
    with mock.patch('httplib2.Http.request', mock_req):
        assert_raises(storymarket.exceptions.StorymarketError, client.request, '/url/', 'GET')