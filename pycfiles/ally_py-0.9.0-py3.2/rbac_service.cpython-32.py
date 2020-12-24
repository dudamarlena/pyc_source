# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/core/impl/rbac_service.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Dec 21, 2012

@package: security - role based access control
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

SQL Alchemy based implementation for the rbac API.
"""
from ..spec import IRbacService
from ally.container.ioc import injected
from ally.container.support import setup
from ally.support.sqlalchemy.mapper import InsertFromSelect, tableFor
from ally.support.sqlalchemy.session import SessionSupport
from security.meta.right import RightMapped
from security.rbac.meta.rbac import RbacMapped, RoleMapped
from security.rbac.meta.rbac_intern import RoleNode, RbacRight, RbacRole
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql.expression import and_, select

@injected
@setup(IRbacService, name='rbacService')
class RbacServiceAlchemy(SessionSupport, IRbacService):
    """
    Implementation for @see: IRbacService
    """

    def __init__(self):
        """
        Construct the rbac service implementation.
        """
        self._idRoot = None
        return

    def rightsForRbacSQL(self, rbacId, sql=None):
        """
        @see: IRbacService.rightsForRbacSQL
        """
        child, parent = aliased(RoleNode), aliased(RoleNode)
        subq = sql or self.session().query(RightMapped)
        subq = subq.join(RbacRight, RbacRight.right == RightMapped.Id)
        subq = subq.join(child, child.role == RbacRight.rbac)
        subq = subq.join(parent, and_(child.left >= parent.left, child.right <= parent.right))
        subq = subq.join(RbacRole, and_(RbacRole.role == parent.role, RbacRole.rbac == rbacId))
        sql = sql or self.session().query(RightMapped)
        sql = sql.join(RbacRight, and_(RbacRight.right == RightMapped.Id, RbacRight.rbac == rbacId))
        sql = sql.union(subq).distinct(RightMapped.Id).order_by(RightMapped.Id)
        return sql

    def rolesForRbacSQL(self, rbacId, sql=None):
        """
        @see: IRbacService.rolesForRbacSQL
        """
        child, parent = aliased(RoleNode), aliased(RoleNode)
        sql = sql or self.session().query(RoleMapped)
        sql = sql.join(child, child.role == RoleMapped.Id)
        sql = sql.join(parent, and_(child.left >= parent.left, child.right <= parent.right))
        sql = sql.join(RbacRole, and_(RbacRole.role == parent.role, RbacRole.rbac == rbacId))
        return sql

    def rbacsForRightSQL(self, rightId, sql=None):
        """
        @see: IRbacService.rbacsForRightSQL
        """
        child, parent = aliased(RoleNode), aliased(RoleNode)
        subq = sql or self.session().query(RbacMapped)
        subq = subq.join(RbacRole, RbacRole.rbac == RbacMapped.Id)
        subq = subq.join(parent, parent.role == RbacRole.role)
        subq = subq.join(child, and_(child.left >= parent.left, child.right <= parent.right))
        subq = subq.join(RbacRight, RbacRight.rbac == child.role)
        subq = subq.join(RightMapped, and_(RightMapped.Id == RbacRight.right, RightMapped.Id == rightId))
        sql = sql or self.session().query(RbacMapped)
        sql = sql.join(RbacRight, RbacRight.rbac == RbacMapped.Id)
        sql = sql.join(RightMapped, and_(RightMapped.Id == RbacRight.right, RightMapped.Id == rightId))
        sql = sql.union(subq).distinct(RbacMapped.Id).order_by(RbacMapped.Id)
        return sql

    def rbacsForRoleSQL(self, roleId, sql=None):
        """
        @see: IRbacService.rbacsForRoleSQL
        """
        child, parent = aliased(RoleNode), aliased(RoleNode)
        subq = sql or self.session().query(RbacMapped)
        subq = subq.join(RbacRole, RbacRole.rbac == RbacMapped.Id)
        subq = subq.join(RoleMapped, and_(RoleMapped.Id == RbacRole.role, RoleMapped.Id == roleId))
        subq = subq.join(parent, parent.role == RbacRole.role)
        subq = subq.join(child, and_(child.left >= parent.left, child.right <= parent.right))
        sql = sql or self.session().query(RbacMapped)
        sql = sql.join(RbacRole, RbacRole.rbac == RbacMapped.Id)
        sql = sql.join(RoleMapped, and_(RoleMapped.Id == RbacRole.role, RoleMapped.Id == roleId))
        sql = sql.union(subq).distinct(RbacMapped.Id).order_by(RbacMapped.Id)
        return sql

    def mergeRole(self, roleId):
        """
        @see: IRbacService.mergeRole
        """
        sql = self.session().query(RoleNode).filter(RoleNode.role == roleId)
        if sql.count() > 0:
            return
        else:
            rbacRole = RbacRole()
            rbacRole.rbac = roleId
            rbacRole.role = roleId
            roleNode = RoleNode()
            roleNode.role = roleId
            rootId = self._rootId()
            rootNode = self.session().query(RoleNode).get(rootId)
            roleNode.left = rootNode.right
            roleNode.right = roleNode.left + 1
            rootNode.right += 2
            self.session().add(rbacRole)
            self.session().add(roleNode)
            self.session().add(rootNode)
            return

    def assignRole(self, roleId, toRoleId):
        """
        @see: IRbacService.assignRole
        """
        child, parent = aliased(RoleNode), aliased(RoleNode)
        sql = self.session().query(child)
        sql = sql.join(parent, and_(child.left < parent.left, child.right > parent.right))
        sql = sql.filter(and_(child.role == toRoleId, parent.role == roleId))
        if sql.count() > 0:
            return False
        sql = self.session().query(parent.id)
        sql = sql.join(child, and_(child.left > parent.left, child.right < parent.right))
        sql = sql.filter(child.role == roleId)
        parentCnt = sql.count()
        childNode = self.session().query(RoleNode).filter(RoleNode.role == roleId).first()
        treeWidth = childNode.right - childNode.left + 1
        id = childNode.id
        sql = self.session().query(RoleNode).filter(RoleNode.role == toRoleId)
        treeCnt = sql.count()
        right, count = (0, 0)
        sql = self.session().query(RoleNode.right).filter(RoleNode.role == toRoleId).order_by(RoleNode.right.desc())
        for left, in sql.all():
            if count == 0:
                gap = treeWidth * treeCnt
                sql = self.session().query(RoleNode).filter(RoleNode.left >= left)
                sql.update({RoleNode.left: RoleNode.left + gap}, False)
                sql = self.session().query(RoleNode).filter(RoleNode.right >= left)
                sql.update({RoleNode.right: RoleNode.right + gap}, False)
                self.session().flush()
                self.session().commit()
                childNode = self.session().query(RoleNode).get(id)
                gap = left - childNode.left
                insert = InsertFromSelect(tableFor(RoleNode), 'fk_role_id, lft, rgt', select([RoleNode.role, RoleNode.left + gap, RoleNode.right + gap]).where(and_(RoleNode.left >= childNode.left, RoleNode.right <= childNode.right)))
                self.session().execute(insert)
                right = left
                count = count + 1
                continue
            gap = (treeCnt - count) * treeWidth
            sql = self.session().query(RoleNode).filter(and_(RoleNode.left >= left, RoleNode.left < right))
            sql.update({RoleNode.left: RoleNode.left + gap}, False)
            sql = self.session().query(RoleNode).filter(and_(RoleNode.right >= left, RoleNode.right < right))
            sql.update({RoleNode.right: RoleNode.right + gap}, False)
            self.session().flush()
            self.session().commit()
            sql = self.session().query(RoleNode).get(id)
            gap = gap + left - childNode.left
            insert = InsertFromSelect(tableFor(RoleNode), 'fk_role_id, lft, rgt', select([RoleNode.role, RoleNode.left + gap, RoleNode.right + gap]).where(and_(RoleNode.left >= childNode.left, RoleNode.right <= childNode.right)))
            self.session().execute(insert)
            right = left
            count = count + 1

        if parentCnt == 1:
            sql = self.session().query(RoleNode).get(id)
            left = childNode.left
            right = childNode.right
            sql = self.session().query(RoleNode).filter(and_(RoleNode.left >= left, RoleNode.right <= right))
            sql.delete()
            sql = self.session().query(RoleNode).filter(RoleNode.left > left)
            sql.update({RoleNode.left: RoleNode.left - treeWidth}, False)
            sql = self.session().query(RoleNode).filter(RoleNode.right > right)
            sql.update({RoleNode.right: RoleNode.right - treeWidth}, False)
        return True

    def unassignRole(self, roleId, toRoleId):
        """
        @see: IRbacService.unassignRole
        """
        sql = self.session().query(RoleNode).filter(RoleNode.role == toRoleId)
        try:
            parentNode = sql.first()
        except NoResultFound:
            return False

        sql = self.session().query(RoleNode)
        sql = sql.filter(and_(RoleNode.role == roleId, RoleNode.left > parentNode.left, RoleNode.right < parentNode.right))
        try:
            childNode = sql.one()
        except NoResultFound:
            return False

        sql = self.session().query(RoleNode)
        sql = sql.filter(and_(RoleNode.left < childNode.left, RoleNode.right > childNode.right))
        childCount = sql.count()
        sql = self.session().query(RoleNode)
        sql = sql.filter(and_(RoleNode.left <= parentNode.left, RoleNode.right >= parentNode.right))
        parentCount = sql.count()
        treeWidth = childNode.right - childNode.left + 1
        leftOffset = parentNode.right - childNode.left
        rightOffset = parentNode.right - childNode.right
        if parentCount == childCount:
            rootNode = self.session().query(RoleNode).get(self._rootId())
            gap = rootNode.right - childNode.left
            rootNode.right = rootNode.right + treeWidth
            insert = InsertFromSelect(tableFor(RoleNode), 'fk_role_id, lft, rgt', select([RoleNode.role, RoleNode.left + gap, RoleNode.right + gap]).where(and_(RoleNode.left >= childNode.left, RoleNode.right <= childNode.right)))
            self.session().execute(insert)
        left, count = (0, 0)
        sql = self.session().query(RoleNode.right).filter(RoleNode.role == toRoleId).order_by(RoleNode.right.asc())
        for right, in sql.all():
            childLeft = right - leftOffset
            childRight = right - rightOffset
            sql = self.session().query(RoleNode).filter(and_(RoleNode.left >= childLeft, RoleNode.right <= childRight))
            sql.delete()
            if count != 0:
                gap = count * treeWidth + leftOffset
                sql = self.session().query(RoleNode).filter(and_(RoleNode.left > left, RoleNode.left < childLeft))
                sql.update({RoleNode.left: RoleNode.left - gap}, False)
                sql = self.session().query(RoleNode).filter(and_(RoleNode.right > left, RoleNode.right < childLeft))
                sql.update({RoleNode.right: RoleNode.right - gap}, False)
            left = childRight
            count = count + 1

        if count > 0:
            gap = treeWidth * count
            sql = self.session().query(RoleNode).filter(RoleNode.left >= childRight)
            sql.update({RoleNode.left: RoleNode.left - gap}, False)
            sql = self.session().query(RoleNode).filter(RoleNode.right >= childRight)
            sql.update({RoleNode.right: RoleNode.right - gap}, False)
        return True

    def deleteRole(self, roleId):
        """
        @see: IRbacService.deleteRole
        """
        raise NotImplementedError('Ask Nelu, still not implemented')

    def _rootId(self):
        """
        Return the root id, that has the lower left value
        """
        if self._idRoot is None:
            sql = self.session().query(RoleNode)
            sql = sql.order_by(RoleNode.left)
            rootNode = sql.first()
            if not rootNode:
                rootNode = RoleNode()
                rootNode.left = 1
                rootNode.right = 2
                self.session().add(rootNode)
                self.session().flush((rootNode,))
            self._idRoot = rootNode.id
        return self._idRoot