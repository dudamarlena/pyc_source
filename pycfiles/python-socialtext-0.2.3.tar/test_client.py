# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_client.py
# Compiled at: 2011-12-29 14:42:22
import base64, mock, requests
from nose.tools import assert_equal
from fakeserver import FakeConfig
from socialtext.client import SocialtextClient

def get_fake_response():
    r = requests.models.Response()
    r.status_code = 200
    r._content = '{"hi": "there"}'
    return r


fake_response = get_fake_response()
mock_request = mock.Mock(return_value=fake_response)

def client():
    cl = SocialtextClient(FakeConfig())
    return cl


def test_impersonate():
    cl = client()
    cl.impersonate('joe@example.com')
    assert_equal('joe@example.com', cl.on_behalf_of)


def test_get():
    cl = client()
    cl.impersonate('joe@example.com')

    @mock.patch.object(requests, 'request', mock_request)
    @mock.patch('time.time', mock.Mock(return_value=1234))
    def test_get_call():
        resp, body = cl.get('/hi')
        mock_request.assert_called_with('GET', 'https://st.example.com/hi', headers={'Accept': 'application/json', 
           'authorization': cl.authorization(), 
           'User-Agent': cl.config.user_agent, 
           'X-On-Behalf-Of': cl.on_behalf_of})
        assert_equal(body, {'hi': 'there'})

    test_get_call()


def test_post():
    cl = client()
    cl.impersonate('joe@example.com')

    @mock.patch.object(requests, 'request', mock_request)
    def test_post_call():
        cl.post('/hi', data=[1, 2, 3])
        mock_request.assert_called_with('POST', 'https://st.example.com/hi', headers={'Accept': 'application/json', 
           'authorization': cl.authorization(), 
           'Content-Type': 'application/json', 
           'User-Agent': cl.config.user_agent, 
           'X-On-Behalf-Of': cl.on_behalf_of}, data='[1, 2, 3]')

    test_post_call()