# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/lib/decorators.py
# Compiled at: 2007-09-06 07:54:22
import logging, formencode, formencode.variabledecode as variabledecode, pylons
from decorator import decorator
from formencode import htmlfill
from paste.util.multidict import UnicodeMultiDict
from pylons.i18n import _
from pylons.helpers import abort
from authxpprojectname.lib.auth import redirect_to_login
log = logging.getLogger(__name__)

def authorize(permission):
    """Decorator for authenticating individual actions. Takes a permission 
    instance as argument(see lib/permissions.py for examples)"""

    def wrapper(func, self, *args, **kw):
        if permission.check():
            log.debug('Checking permission')
            return func(self, *args, **kw)
        redirect_to_login()

    return decorator(wrapper)