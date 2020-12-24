# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-m2m-history/m2m_history/fields.py
# Compiled at: 2016-04-13 08:47:12
from django.db import models
from .descriptors import ManyRelatedObjectsHistoryDescriptor, ReverseManyRelatedObjectsHistoryDescriptor
__all__ = [
 'ManyToManyHistoryField']

class ManyToManyHistoryField(models.ManyToManyField):

    def __init__(self, *args, **kwargs):
        self.versions = kwargs.pop('versions', False)
        super(ManyToManyHistoryField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        """
        Call super method and remove unique_together, add time fields and change descriptor class
        """
        super(ManyToManyHistoryField, self).contribute_to_class(cls, name)
        try:
            self.rel.through._meta.unique_together = ()
            self.rel.through.add_to_class('time_from', models.DateTimeField('Datetime from', null=True, db_index=True))
            self.rel.through.add_to_class('time_to', models.DateTimeField('Datetime to', null=True, db_index=True))
        except AttributeError:
            pass

        setattr(cls, self.name, ReverseManyRelatedObjectsHistoryDescriptor(self))

    def contribute_to_related_class(self, cls, related):
        """
        Change descriptor class
        """
        super(ManyToManyHistoryField, self).contribute_to_related_class(cls, related)
        if not self.rel.is_hidden() and not getattr(related.model._meta, 'swapped', None):
            setattr(cls, related.get_accessor_name(), ManyRelatedObjectsHistoryDescriptor(related))
        return


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^m2m_history\\.fields\\.ManyToManyHistoryField'])
except ImportError:
    pass