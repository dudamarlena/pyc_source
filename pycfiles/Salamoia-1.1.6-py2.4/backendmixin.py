# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/backendmixin.py
# Compiled at: 2007-12-02 16:26:59
from salamoia.nacl.feeds import FeedControl
from salamoia.nacl.transaction import TransactionControl
from salamoia.nacl.cache import BackendObjectCache
from salamoia.nacl.lock import LockControl
from salamoia.nacl.fetchpattern import FetchPatternControl
from salamoia.nacl.security import SecurityControl
from salamoia.nacl.introspection import IntrospectionControl
from salamoia.h2o.logioni import Ione

class BackendMixin(TransactionControl, BackendObjectCache, FeedControl, LockControl, FetchPatternControl, SecurityControl, IntrospectionControl):
    """
    Add classes that extends the BackendControl as superclasses
    of this class.

    Backend specific mixins must be added in the backend specific BackendControl
    subclass, not here. (see nacl.ldap.ldapbackend.CachedLDAPBackendControl for example
    """
    __module__ = __name__

    def __init__(self):
        Ione.log('BackendMixin init')
        super(BackendMixin, self).__init__()


from salamoia.tests import *
runDocTests()