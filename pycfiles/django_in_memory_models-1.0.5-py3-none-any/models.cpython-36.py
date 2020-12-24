# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oldcai/programs/python/webproject/django-in-memory-models/in_memory/models.py
# Compiled at: 2017-10-23 01:53:27
# Size of source mod 2**32: 6673 bytes
from django.db.models import Model, DEFERRED, FieldDoesNotExist
from django.db.models.base import ModelState
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.signals import pre_init, post_init

class InMemoryModel(Model):

    class Meta:
        abstract = True
        managed = False

    def __init__(self, *args, **kwargs):
        cls = self.__class__
        opts = self._meta
        _setattr = setattr
        _DEFERRED = DEFERRED
        pre_init.send(sender=cls, args=args, kwargs=kwargs)
        self._state = ModelState()
        if len(args) > len(opts.concrete_fields):
            raise IndexError('Number of args exceeds number of fields')
        else:
            if not kwargs:
                fields_iter = iter(opts.concrete_fields)
                for val, field in zip(args, fields_iter):
                    if val is _DEFERRED:
                        pass
                    else:
                        _setattr(self, field.attname, val)

            else:
                fields_iter = iter(opts.fields)
                for val, field in zip(args, fields_iter):
                    if val is _DEFERRED:
                        pass
                    else:
                        _setattr(self, field.attname, val)
                        kwargs.pop(field.name, None)

        for field in fields_iter:
            is_related_object = False
            if field.attname not in kwargs:
                if field.column is None:
                    continue
            else:
                if kwargs:
                    if isinstance(field.remote_field, ForeignObjectRel):
                        try:
                            rel_obj = kwargs.pop(field.name)
                            is_related_object = True
                        except KeyError:
                            try:
                                val = kwargs.pop(field.attname)
                            except KeyError:
                                val = field.get_default()

                        else:
                            if rel_obj is None and field.null:
                                val = None
                    else:
                        try:
                            val = kwargs.pop(field.attname)
                        except KeyError:
                            val = field.get_default()

                else:
                    val = field.get_default()
            if is_related_object:
                if rel_obj is not _DEFERRED:
                    _setattr(self, field.name, rel_obj)
                else:
                    if val is not _DEFERRED:
                        _setattr(self, field.attname, val)

        if kwargs:
            property_names = opts._property_names
            for prop in tuple(kwargs):
                try:
                    if prop in property_names or opts.get_field(prop):
                        if kwargs[prop] is not _DEFERRED:
                            _setattr(self, prop, kwargs[prop])
                        del kwargs[prop]
                except (AttributeError, FieldDoesNotExist):
                    pass

            if kwargs:
                for key, value in kwargs.items():
                    if hasattr(self, key):
                        raise TypeError("'%s' is an invalid keyword argument for this function" % key)
                    setattr(self, key, value)

        super(Model, self).__init__()
        post_init.send(sender=cls, instance=self)


class Sorter(object):

    def __init__(self, name, key, related_class, default=None):
        self.name = name
        self.key = key
        self.default = default
        self.sorted_class = related_class
        super(Sorter, self).__init__()

    def __iadd__(self, other):
        if isinstance(other, (int, float)):
            self.increase(int(other))
        return self

    def __isub__(self, other):
        if isinstance(other, (int, float)):
            self.increase(-int(other))
        return self

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def top(self, count):
        top_ids = self.top_ids(count)
        sorted_class_key = getattr(self.sorted_class, 'key_field', 'user_id')
        return [(self.sorted_class)(**{sorted_class_key: top_id}) for top_id in top_ids]

    @property
    def rank(self):
        return self.get_rank()

    @property
    def value(self):
        result = self.get_value()
        if result is None:
            result = self.default
        return result

    def increase(self, value):
        raise NotImplementedError

    def set(self, value):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def get_rank(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def top_ids(self, count):
        raise NotImplementedError