# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/UUIDField.py
# Compiled at: 2010-05-14 03:47:11
from django.db.models import CharField
try:
    import uuid
except ImportError:
    from django.utils import uuid

class UUIDVersionError(Exception):
    __module__ = __name__


class UUIDField(CharField):
    """
    UUIDField for Django, supports all uuid versions which are natively
    suported by the uuid python module.
    """
    __module__ = __name__

    def __init__(self, verbose_name=None, name=None, auto=True, version=1, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 36
        self.auto = auto
        if auto:
            kwargs['blank'] = True
            kwargs['editable'] = kwargs.get('editable', False)
        self.version = version
        self.node = None
        self.clock_seq = None
        self.namespace = None
        self.name = None
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        CharField.__init__(self, verbose_name, name, **kwargs)
        return

    def contribute_to_class(self, cls, name):
        if name in ('id', 'uuid'):
            assert not cls._meta.has_auto_field, "A model can't have more than one AutoField: %s %s %s; have %s" % (self, cls, name, cls._meta.auto_field)
            super(UUIDField, self).contribute_to_class(cls, name)
            cls._meta.has_auto_field = True
            cls._meta.auto_field = self
        else:
            super(UUIDField, self).contribute_to_class(cls, name)

    def get_internal_type(self):
        return CharField.__name__

    def create_uuid(self):
        if not self.version or self.version == 4:
            return uuid.uuid4()
        elif self.version == 1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version == 2:
            raise UUIDVersionError('UUID version 2 is not supported.')
        elif self.version == 3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version == 5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UUIDVersionError('UUID version %s is not valid.' % self.version)

    def pre_save(self, model_instance, add):
        if self.auto and add:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(UUIDField, self).pre_save(model_instance, add)
            if self.auto and not value:
                value = unicode(self.create_uuid())
                setattr(model_instance, self.attname, value)
        return value


try:
    import django
    from django.conf import settings
    from south.modelsinspector import add_introspection_rules
    rules = [
     (
      (
       UUIDField,), [], {'auto': ['auto', {'default': True}], 'version': ['version', {'default': 1}], 'node': ['node', {'default': None}], 'clock_seq': ['clock_seq', {'default': None}], 'namespace': ['namespace', {'default': None}], 'name': ['name', {'default': None}], 'max_length': ['max_length', {'default': 36}], 'blank': ['blank', {'default': False, 'ignore_if': 'auto'}], 'editable': ['editable', {'default': False}]})]
    add_introspection_rules(rules, ['^softwarefabrica\\.django\\.utils'])
except ImportError:
    pass