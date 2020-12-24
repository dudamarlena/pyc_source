# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/middleware/base.py
# Compiled at: 2019-04-16 18:29:39
# Size of source mod 2**32: 436 bytes
from .. import util

class DomainSpecifiedKlass(object):
    __doc__ = '\n    '
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