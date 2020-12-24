# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/acl/security.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Mar 6, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the acl security support setup.\n'
from acl.spec import RightAcl, TypeAcl
from ally.container import support
import logging
log = logging.getLogger(__name__)
try:
    from .. import security
except ImportError:
    log.info('No security plugin available, thus no support available for it')
else:
    security = security
    from acl.core.impl.synchronizer import SynchronizerRights
    from security.api.right import IRightService
    support.createEntitySetup(SynchronizerRights)

    def rightId(aclRight):
        """
        Provides the security right id for the provided acl right.
        
        @param aclRight: RightAcl
            The acl right to provide the id for.
        @return: integer
            The id of the security right.
        """
        assert isinstance(aclRight, RightAcl), 'Invalid right %s' % aclRight
        assert isinstance(aclRight.type, TypeAcl), 'Invalid right %s, has no type' % aclRight
        rightService = support.entityFor(IRightService)
        assert isinstance(rightService, IRightService)
        return rightService.getByName(aclRight.type.name, aclRight.name).Id