# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/models/role.py
# Compiled at: 2016-12-30 20:15:02
from flask_security import RoleMixin
from ..facets.database import db
from ..facets.marshalling import ma
from ..mixins.crud import CRUDMixin
from ..mixins.marshmallow import MarshmallowMixin

class RoleSchema(ma.Schema):

    class Meta:
        additional = ('id', 'name', 'description')


class Role(db.Model, RoleMixin, CRUDMixin, MarshmallowMixin):
    """
    For the purpose of access controls, Roles can be used to create
    collections of users and give them permissions as a group.
    """
    __schema__ = RoleSchema
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    @classmethod
    def add_default_roles(cls):
        """
        Create a basic set of users and roles

        :returns: None
        """
        from .. import security
        security.user_datastore.find_or_create_role('Admin')
        security.user_datastore.find_or_create_role('User')
        db.session.commit()