# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/model/memento.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = 'The ORM part of the classes that store the change history of objects to\nthe database.  The table defined here is used in :mod:`camelot.core.memento` \nto store the changes.\n\nTo prevent this table to be used to store changes, overwrite the \n:meth:`camelot.admin.application_admin.ApplicationAdmin.get_memento` method\nthe custom `ApplicationAdmin`.\n'
import datetime
from sqlalchemy import schema, orm
from sqlalchemy.types import Unicode, Integer, DateTime, PickleType
from camelot.admin.entity_admin import EntityAdmin
from camelot.admin.object_admin import ObjectAdmin
from camelot.admin.not_editable_admin import not_editable_admin
from camelot.core.orm import Entity, ManyToOne
from camelot.core.utils import ugettext_lazy as _
from camelot.view import filters
from camelot.view.controls import delegates
from authentication import AuthenticationMechanism

class PreviousAttribute(object):
    """Helper class to display previous attributes"""

    def __init__(self, attribute, previous_value):
        self.attribute = attribute
        self.previous_value = unicode(previous_value)

    class Admin(ObjectAdmin):
        list_display = [
         'attribute', 'previous_value']


class Memento(Entity):
    """Keeps information on the previous state of objects, to keep track
    of changes and enable restore to that previous state"""
    __tablename__ = 'memento'
    model = schema.Column(Unicode(256), index=True, nullable=False)
    primary_key = schema.Column(Integer(), index=True, nullable=False)
    creation_date = schema.Column(DateTime(), default=datetime.datetime.now)
    authentication = ManyToOne(AuthenticationMechanism, required=True, ondelete='restrict', onupdate='cascade')
    memento_type = schema.Column(Integer, nullable=False, index=True)
    previous_attributes = orm.deferred(schema.Column(PickleType()))

    @property
    def previous(self):
        previous = self.previous_attributes
        if previous:
            return [ PreviousAttribute(k, v) for k, v in previous.items() ]
        return []

    class Admin(EntityAdmin):
        verbose_name = _('History')
        verbose_name_plural = _('History')
        list_display = ['creation_date', 'authentication', 'model',
         'primary_key']
        form_display = list_display + ['previous']
        list_filter = [filters.ComboBoxFilter('model')]
        field_attributes = {'previous': {'target': PreviousAttribute, 'delegate': delegates.One2ManyDelegate, 
                        'python_type': list}}

    Admin = not_editable_admin(Admin)