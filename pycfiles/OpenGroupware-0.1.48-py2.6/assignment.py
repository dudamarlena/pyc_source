# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/assignment.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from base import Base, KVC
from sqlalchemy.orm import MapperExtension

class ProjectAssignmentExtension(MapperExtension):

    def _set_has_access(self, instance):
        if instance.rights:
            instance.is_acl = 1
        else:
            instance.is_acl = 0

    def before_insert(self, mapper, connection, instance):
        self._set_has_access(instance)

    def before_update(self, mapper, connection, instance):
        self._set_has_access(instance)


class ProjectAssignment(Base):
    """ An assignment between company objects and a project"""
    __tablename__ = 'project_company_assignment'
    __mapper_args__ = {'extension': ProjectAssignmentExtension()}
    object_id = Column('project_company_assignment_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('project_id', Integer, ForeignKey('project.project_id'), ForeignKey('job.project_id'), nullable=False)
    child_id = Column('company_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), nullable=False)
    info = Column('info', String(255))
    rights = Column('access_right', String(50))
    is_acl = Column('has_access', Integer)

    def __init__(self, project_id, company_id, permissions=None, info=None):
        self.parent_id = project_id
        self.child_id = company_id
        self.info = info
        self.rights = permissions

    @property
    def action(self):
        if self.rights:
            return 'allowed'
        else:
            return

    @property
    def permissions(self):
        return self.rights

    @permissions.setter
    def permissions(self, value):
        self.rights = value

    @property
    def context_id(self):
        if self.rights:
            return self.child_id
        else:
            return

    def __repr__(self):
        return ('<ProjectAssignment objectId="{0}" parentId="{1}" childId="{2}" isACL="{3}" rights="{4}"/>').format(self.object_id, self.parent_id, self.child_id, self.is_acl, self.rights)


class CompanyAssignment(Base):
    """ An assignment between company objects """
    __tablename__ = 'company_assignment'
    object_id = Column('company_assignment_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('company_id', Integer, ForeignKey('enterprise.company_id'), ForeignKey('team.company_id'), nullable=False)
    child_id = Column('sub_company_id', Integer, ForeignKey('person.company_id'), nullable=False)
    info = ''
    rights = ''

    def __init__(self, parent_id, child_id):
        self.parent_id = parent_id
        self.child_id = child_id

    @property
    def is_acl(self):
        return 0

    def __repr__(self):
        return ('<CompanyAssignment objectId="{0}" parentId="{1}" childId="{2}" isACL="{3}" rights="{4}"/>').format(self.object_id, self.parent_id, self.child_id, self.is_acl, self.rights)