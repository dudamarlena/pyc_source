# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/synchronizer.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 22, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nSynchronizer for security with ACL.\n'
from acl.spec import Acl, TypeAcl, RightAcl
from ally.container import wire, app
from ally.container.ioc import injected
from ally.container.support import setup
from ally.exception import InputError
from security.api.right import IRightService, Right
from security.api.right_type import IRightTypeService, RightType

@injected
@setup(name='synchronizerRights')
class SynchronizerRights:
    """
    Provides the synchronization of rights and right types for security with the ACL rights and rights types.
    This synchronization is required for @see: RbacPopulateRights processor to work properly.
    """
    acl = Acl
    wire.entity('acl')
    rightTypeService = IRightTypeService
    wire.entity('rightTypeService')
    rightService = IRightService
    wire.entity('rightService')

    def __init__(self):
        assert isinstance(self.acl, Acl), 'Invalid acl repository %s' % self.acl
        assert isinstance(self.rightTypeService, IRightTypeService), 'Invalid right type service %s' % self.rightTypeService
        assert isinstance(self.rightService, IRightService), 'Invalid right service %s' % self.rightService

    @app.populate(app.DEVEL, app.CHANGED, priority=app.PRIORITY_FIRST)
    def synchronizeSecurityWithACL(self):
        """
        Synchronize the ACL rights with the database RBAC rights.
        """
        for aclType in self.acl.types:
            self.processRightType(aclType)

    def processRightType(self, aclType):
        """
        Process the security right type for ACL type.
        
        @param aclType: TypeAcl
            The ACL type to process.
        """
        assert isinstance(aclType, TypeAcl), 'Invalid acl type %s' % aclType
        try:
            rightType = self.rightTypeService.getByName(aclType.name)
        except InputError:
            rightType = RightType()
            rightType.Name = aclType.name
            rightType.Description = aclType.description
            typeId = self.rightTypeService.insert(rightType)
            self.processRights(typeId, True, aclType)
        else:
            assert isinstance(rightType, RightType)
            if rightType.Description != aclType.description:
                rightType.Description = aclType.description
                self.rightTypeService.update(rightType)
            self.processRights(rightType.Id, False, aclType)

    def processRights(self, typeId, isNew, aclType):
        """
        Process the security rights from the provided ACL type.
        
        @param typeId: integer
            The security type id.
        @param isNew: boolean
            Flag indicating that the security type is new or not.
        @param aclType: TypeAcl
            The ACL type to have the rights processed.
        """
        assert isinstance(typeId, int), 'Invalid security type id %s' % typeId
        assert isinstance(isNew, bool), 'Invalid is new flag %s' % isNew
        assert isinstance(aclType, TypeAcl), 'Invalid acl type %s' % aclType
        aclRights = {right.name:right for right in aclType.rights}
        if not isNew:
            for right in self.rightService.getAll(typeId):
                assert isinstance(right, Right), 'Invalid right %s' % right
                aclRight = aclRights.pop(right.Name, None)
                if aclRight:
                    assert isinstance(aclRight, RightAcl)
                    if right.Description != aclRight.description:
                        right.Description = aclRight.description
                        self.rightService.update(right)
                    else:
                        continue

        for aclRight in aclRights.values():
            right = Right()
            right.Type = typeId
            right.Name = aclRight.name
            right.Description = aclRight.description
            self.rightService.insert(right)

        return