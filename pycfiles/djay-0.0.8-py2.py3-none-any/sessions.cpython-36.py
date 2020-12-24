# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/sessions.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 2321 bytes
import requests
from ._compat import urljoin

class BaseUrlSession(requests.Session):
    __doc__ = "A Session with a URL that all requests will use as a base.\n\n    Let's start by looking at an example:\n\n    .. code-block:: python\n\n        >>> from requests_toolbelt import sessions\n        >>> s = sessions.BaseUrlSession(\n        ...     base_url='https://example.com/resource/')\n        >>> r = s.get('sub-resource/' params={'foo': 'bar'})\n        >>> print(r.request.url)\n        https://example.com/resource/sub-resource/?foo=bar\n\n    Our call to the ``get`` method will make a request to the URL passed in\n    when we created the Session and the partial resource name we provide.\n\n    We implement this by overriding the ``request`` method so most uses of a\n    Session are covered. (This, however, precludes the use of PreparedRequest\n    objects).\n\n    .. note::\n\n        The base URL that you provide and the path you provide are **very**\n        important.\n\n    Let's look at another *similar* example\n\n    .. code-block:: python\n\n        >>> from requests_toolbelt import sessions\n        >>> s = sessions.BaseUrlSession(\n        ...     base_url='https://example.com/resource/')\n        >>> r = s.get('/sub-resource/' params={'foo': 'bar'})\n        >>> print(r.request.url)\n        https://example.com/sub-resource/?foo=bar\n\n    The key difference here is that we called ``get`` with ``/sub-resource/``,\n    i.e., there was a leading ``/``. This changes how we create the URL\n    because we rely on :mod:`urllib.parse.urljoin`.\n\n    To override how we generate the URL, sub-class this method and override the\n    ``create_url`` method.\n\n    Based on implementation from\n    https://github.com/kennethreitz/requests/issues/2554#issuecomment-109341010\n    "
    base_url = None

    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = self.create_url(url)
        return (super(BaseUrlSession, self).request)(
 method, url, *args, **kwargs)

    def create_url(self, url):
        """Create the URL based off this partial path."""
        return urljoin(self.base_url, url)