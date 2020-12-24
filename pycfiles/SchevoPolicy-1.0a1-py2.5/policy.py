# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/policy.py
# Compiled at: 2008-01-19 12:32:25
"""Policy classes.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevopolicy.constant import DENY
from schevopolicy.rdatabase import RestrictedDatabase
from schevopolicy.error import Unauthorized

class Policy(object):

    def __init__(self, db):
        self.db = db

    def __call__(self, context=None):
        """Return a restricted database.

        - `context`: The context, if available, to use when enforcing
          restriction rules.
        """
        return RestrictedDatabase(self, context)

    def attach(self, obj, context):
        """Attach convenience functions and attributes to `obj` based
        on `context`."""
        d = obj.__dict__

        def _allow():
            return self.allow(context)

        def _allow_t(extent, entity, t_name):
            return self.allow_t(context, extent, entity, t_name)

        def _allow_v(entity, v_name):
            return self.allow_v(context, entity, v_name)

        def _unauthorized():
            raise Unauthorized('The operation was not authorized.')

        d['_allow'] = _allow
        d['_allow_t'] = _allow_t
        d['_allow_v'] = _allow_v
        d['_context'] = context
        d['_policy'] = self
        d['_unauthorized'] = _unauthorized


optimize.bind_all(sys.modules[__name__])