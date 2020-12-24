# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/weargoggles/django-coreapi/django_coreapi/mock.py
# Compiled at: 2017-05-15 07:49:40
# Size of source mod 2**32: 1934 bytes
import functools, coreapi, django_coreapi.client
_responses = []

def get_match(document, keys):
    """
    Find the first matching response in the current set
    :param keys: the key path to be matched
    :return: the matching response or None
    """
    global _responses
    for response in _responses:
        if response[:2] == (document.url, keys):
            return response[(-1)]


class Mock(object):
    __doc__ = '\n    Can be used as a context manager. Takes handler functions as arguments, which are evaluated in order in place of\n    '

    def __init__(self):
        super(Mock, self).__init__()

    def __enter__(self):
        self._real_action = coreapi.Client.action
        self._real_django_client_action = django_coreapi.client.DjangoCoreAPIClient.action

        def fake_action(client, document, keys, *args, **kwargs):
            res = get_match(document, keys)
            if res is not None:
                return res
            raise Exception('No such mocked action')

        coreapi.Client.action = fake_action
        django_coreapi.client.DjangoCoreAPIClient.action = fake_action

    def __exit__(self, exc_type, value, tb):
        global _responses
        coreapi.Client.action = self._real_action
        django_coreapi.client.DjangoCoreAPIClient.action = self._real_django_client_action
        _responses = []


def activate(f):
    """
    A decorator which mocks the coreapi and django_coreapi clients, allowing use of `add`
    :param f: the function to be wrapped
    :return: the wrapped function
    """

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        with Mock():
            return f(*args, **kwargs)

    return decorated


def add(document, keys, response):
    _responses.append((document.url, keys, response))