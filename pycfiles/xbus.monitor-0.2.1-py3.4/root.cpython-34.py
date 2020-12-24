# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/resources/root.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 405 bytes
from pyramid import security

class RootFactory(object):
    __doc__ = 'Default factory that allows any authenticated user to access our views.\n    All views under the URL dispatch system use this root factory.\n    '
    __acl__ = [
     (
      security.Allow, security.Authenticated, 'view')]

    def __init__(self, request):
        """Empty on purpose - this is needed to avoid errors."""
        pass