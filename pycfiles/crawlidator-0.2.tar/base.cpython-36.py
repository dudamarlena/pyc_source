# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/middleware/base.py
# Compiled at: 2019-04-16 18:29:39
# Size of source mod 2**32: 436 bytes
from .. import util

class DomainSpecifiedKlass(object):
    """DomainSpecifiedKlass"""
    domain = None

    def __init__(self, domain=None):
        """
        :type domain: str
        :param domain:
        """
        if domain is not None:
            self.domain = domain
        if self.domain is None:
            raise ValueError('You have to specify `domain`')
        self.domain = util.get_domain(self.domain)