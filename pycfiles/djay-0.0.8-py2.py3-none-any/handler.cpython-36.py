# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/auth/handler.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 4408 bytes
"""

requests_toolbelt.auth.handler
==============================

This holds all of the implementation details of the Authentication Handler.

"""
from requests.auth import AuthBase, HTTPBasicAuth
from requests.compat import urlparse, urlunparse

class AuthHandler(AuthBase):
    __doc__ = "\n\n    The ``AuthHandler`` object takes a dictionary of domains paired with\n    authentication strategies and will use this to determine which credentials\n    to use when making a request. For example, you could do the following:\n\n    .. code-block:: python\n\n        from requests import HTTPDigestAuth\n        from requests_toolbelt.auth.handler import AuthHandler\n\n        import requests\n\n        auth = AuthHandler({\n            'https://api.github.com': ('sigmavirus24', 'fakepassword'),\n            'https://example.com': HTTPDigestAuth('username', 'password')\n        })\n\n        r = requests.get('https://api.github.com/user', auth=auth)\n        # => <Response [200]>\n        r = requests.get('https://example.com/some/path', auth=auth)\n        # => <Response [200]>\n\n        s = requests.Session()\n        s.auth = auth\n        r = s.get('https://api.github.com/user')\n        # => <Response [200]>\n\n    .. warning::\n\n        :class:`requests.auth.HTTPDigestAuth` is not yet thread-safe. If you\n        use :class:`AuthHandler` across multiple threads you should\n        instantiate a new AuthHandler for each thread with a new\n        HTTPDigestAuth instance for each thread.\n\n    "

    def __init__(self, strategies):
        self.strategies = dict(strategies)
        self._make_uniform()

    def __call__(self, request):
        auth = self.get_strategy_for(request.url)
        return auth(request)

    def __repr__(self):
        return '<AuthHandler({0!r})>'.format(self.strategies)

    def _make_uniform(self):
        existing_strategies = list(self.strategies.items())
        self.strategies = {}
        for k, v in existing_strategies:
            self.add_strategy(k, v)

    @staticmethod
    def _key_from_url(url):
        parsed = urlparse(url)
        return urlunparse((parsed.scheme.lower(),
         parsed.netloc.lower(),
         '', '', '', ''))

    def add_strategy(self, domain, strategy):
        """Add a new domain and authentication strategy.

        :param str domain: The domain you wish to match against. For example:
            ``'https://api.github.com'``
        :param str strategy: The authentication strategy you wish to use for
            that domain. For example: ``('username', 'password')`` or
            ``requests.HTTPDigestAuth('username', 'password')``

        .. code-block:: python

            a = AuthHandler({})
            a.add_strategy('https://api.github.com', ('username', 'password'))

        """
        if isinstance(strategy, tuple):
            strategy = HTTPBasicAuth(*strategy)
        key = self._key_from_url(domain)
        self.strategies[key] = strategy

    def get_strategy_for(self, url):
        """Retrieve the authentication strategy for a specified URL.

        :param str url: The full URL you will be making a request against. For
            example, ``'https://api.github.com/user'``
        :returns: Callable that adds authentication to a request.

        .. code-block:: python

            import requests
            a = AuthHandler({'example.com', ('foo', 'bar')})
            strategy = a.get_strategy_for('http://example.com/example')
            assert isinstance(strategy, requests.auth.HTTPBasicAuth)

        """
        key = self._key_from_url(url)
        return self.strategies.get(key, NullAuthStrategy())

    def remove_strategy(self, domain):
        """Remove the domain and strategy from the collection of strategies.

        :param str domain: The domain you wish remove. For example,
            ``'https://api.github.com'``.

        .. code-block:: python

            a = AuthHandler({'example.com', ('foo', 'bar')})
            a.remove_strategy('example.com')
            assert a.strategies == {}

        """
        key = self._key_from_url(domain)
        if key in self.strategies:
            del self.strategies[key]


class NullAuthStrategy(AuthBase):

    def __repr__(self):
        return '<NullAuthStrategy>'

    def __call__(self, r):
        return r