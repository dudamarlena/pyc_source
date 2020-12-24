# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/scm_access/scm_access.py
# Compiled at: 2010-10-28 13:12:44
from trac.core import *
from trac.perm import IPermissionRequestor
revision = '$Rev$'
url = '$URL$'

class SCMAccessRequestor(Component):
    implements(IPermissionRequestor)

    def get_permission_actions(self):
        """Returns a list of actions defined by this component."""
        yield 'SCM_READ'
        yield 'SCM_ACCESS'