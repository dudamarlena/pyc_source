# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/middleware/url_builder/builder.py
# Compiled at: 2019-04-16 18:31:21
# Size of source mod 2**32: 1531 bytes
from __future__ import print_function
from ..base import DomainSpecifiedKlass
from ... import util

class BaseUrlBuilder(DomainSpecifiedKlass):
    __doc__ = '\n    Base url builder. Provide functional interface to create url.\n\n    Example::\n\n        >>> from crawlib2 import BaseUrlBuilder\n        >>> class PythonOrgUrlBuilder(DomainSpecifiedKlass):\n        ...     domain = "https://www.python.org"\n        ...\n        ...     def url_downloads_page(self):\n        ...         return self.join_all("downloads")\n        ...\n        ...     def url_release(self, version):\n        ...         \'\'\'version is like "2.7.16", "3.6.8", ...\'\'\'\n        ...         return self.join_all("downloads", "release", version.replace(".". ""))\n        >>> url_builder = PythonOrgUrlBuilder()\n    '

    def join_all(self, *parts):
        """
        Join all parts with domain. Example domain: https://www.python.org

        :rtype: list
        :param parts: Other parts, example: "/doc", "/py27"

        :rtype: str
        :return: url

        Example::

            >>> join_all("product", "iphone")
            https://www.apple.com/product/iphone
        """
        url = (util.join_all)(self.domain, *parts)
        return url

    def add_params(self, endpoint, params):
        """
        Combine query endpoint and params.
        """
        if not endpoint.startswith(self.domain):
            raise ValueError('%s not start with %s' % (endpoint, self.domain))
        return util.add_params(endpoint, params)