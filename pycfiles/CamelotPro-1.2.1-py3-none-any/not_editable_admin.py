# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/admin/not_editable_admin.py
# Compiled at: 2013-04-11 17:47:52
from copy import copy
from itertools import tee

def not_editable_admin(original_admin, actions=False, editable_fields=[], deep=True):
    """Class decorator to make all fields read-only.

    :param original_admin: an :class:`camelot.admin.object_admin.ObjectAdmin` 
        class (not an instance)
    :param actions: :const:`True` if the new admin should have its actions 
        enabled, defaults to :const:`False`
    :param editable_fields: list of fields that should remain editable, if they
        are editable in the original admin.
    :param deep: indicates if Admin classes related to this admin should become
        read-only as well.  This makes other objects pointed to by OneToMany and
        ManyToOne fields read only.
    :return: a new admin class, with read only fields.  The new admin class
        is a subclass of the original class.

    usage ::

        class Movie(Entity):
            name = Field(Unicode(50))
            contributions = Field(Unicode(255))

            class Admin(EntityAdmin):
                list_display = ['name', 'contributions]

            Admin = not_editable_admin( Admin, 
                                        editable_fields=['contributions'] )
    """

    class NewAdmin(original_admin):

        def get_related_admin(self, cls):
            admin = super(NewAdmin, self).get_related_admin(cls)
            if not deep:
                return admin

            class AdminReadOnlyDecorator(object):

                def __init__(self, original_admin, editable_fields):
                    self._original_admin = original_admin
                    self._editable_fields = editable_fields
                    self._field_attributes = dict()

                def _process_field_attributes(self, field, attributes):
                    if 'editable' not in attributes:
                        return attributes
                    if attributes['editable'] == False:
                        return attributes
                    if self._editable_fields and field in self._editable_fields:
                        return attributes
                    new_attributes = copy(attributes)
                    new_attributes['editable'] = False
                    return new_attributes

                def __getattr__(self, name):
                    return getattr(self._original_admin, name)

                def get_fields(self):
                    fields = self._original_admin.get_fields()
                    return [ (field_name, self._process_field_attributes(field_name, _attrs)) for field_name, _attrs in fields ]

                def get_field_attributes(self, field_name):
                    attributes = self._original_admin.get_field_attributes(field_name)
                    return self._process_field_attributes(field_name, attributes)

                def get_dynamic_field_attributes(self, obj, field_names):
                    fn1, fn2 = tee(field_names, 2)
                    dynamic_fa = self._original_admin.get_dynamic_field_attributes(obj, fn1)
                    return [ self._process_field_attributes(name, attributes) for name, attributes in zip(fn2, dynamic_fa) ]

                def get_static_field_attributes(self, field_names):
                    fn1, fn2 = tee(field_names, 2)
                    static_fa = self._original_admin.get_static_field_attributes(fn1)
                    return [ self._process_field_attributes(name, attributes) for name, attributes in zip(fn2, static_fa) ]

                def get_related_admin(self, entity):
                    return AdminReadOnlyDecorator(self._original_admin.get_related_admin(entity), self._editable_fields)

                def get_form_actions(self, *a, **kwa):
                    return []

                def get_list_actions(self, *a, **kwa):
                    return []

                def get_columns(self):
                    return [ (field, self._process_field_attributes(field, attrs)) for field, attrs in self._original_admin.get_columns()
                           ]

            return AdminReadOnlyDecorator(admin, editable_fields)

        def get_field_attributes(self, field_name):
            attribs = super(NewAdmin, self).get_field_attributes(field_name)
            if field_name not in editable_fields:
                attribs['editable'] = False
            return attribs

        def get_form_actions(self, obj):
            if actions == True:
                return super(NewAdmin, self).get_form_actions(obj)
            return []

        def get_list_actions(self):
            if actions == True:
                return super(NewAdmin, self).get_list_actions()
            return []

    return NewAdmin