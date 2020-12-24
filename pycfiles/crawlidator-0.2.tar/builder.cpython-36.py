# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/middleware/url_builder/builder.py
# Compiled at: 2019-04-16 18:31:21
# Size of source mod 2**32: 1531 bytes
from __future__ import print_function
from ..base import DomainSpecifiedKlass
from ... import util

class BaseUrlBuilder(DomainSpecifiedKlass):
    """BaseUrlBuilder"""

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