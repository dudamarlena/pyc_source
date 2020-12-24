# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/labeled_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 10192 bytes
from mvc.support.utils import rec_getattr, rec_setattr
from mvc.support.observables.value_wrapper import ValueWrapper
import inspect

class Mixable(object):
    __doc__ = '\n    Base class that allows to mix-in any other new-style class\n    passed in the constructor, using the mix_with keyword argument\n    (tuple of class types).\n    '

    def __init__(self, mix_with=None, *args, **kwargs):
        (super(Mixable, self).__init__)(*args, **kwargs)
        if mix_with is not None:
            name = type(self).__name__
            for klass in mix_with:
                name = '%s_%s' % (klass.__name__.replace('Mixin', ''), name)

            bases = tuple(mix_with) + (type(self),)
            self.__class__ = type(name, bases, {})


class LabeledProperty(Mixable):
    __doc__ = "\n     Property descriptor base class to be used in combination with a\n     ~:class:`mvc.models.Model` (sub)class.\n     Expects it's label (attribute name) to be set or passed to __init__, for\n     ~:class:`mvc.models.Model` (sub)class this is done automagically using\n     its metaclass.\n     \n     Additional keyword arguments will be set as attributes on the descriptor.\n     \n     Some of these keywords have been given sane default values, even though\n     they are not required for the implementation:\n     \n         - title = label\n         - math_title = label\n         - description = label\n         - persistent (False)\n         - store_private = (False)\n         - visible (False)\n         - data_type (object)\n         - observable (True)\n         - widget_type ('custom')\n         \n     To use this class, use it like the regular Property or property decorators.\n     E.g.:\n         attribute = LabeledProperty(...)\n     or\n         @LabeledProperty(...)\n         def get_attribute(self):\n             return self.attribute\n             \n     The setter function is expected to accept either a single argument (the \n     new value) or two arguments (the property descriptor instance and the new \n     value). Similarly, the getter and deleter function are expected to accept\n     no arguments or a single argument (the property descriptor function instance).\n    "
    _label = None

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        if self.default is not None:
            self.default = ValueWrapper.wrap_value((self.label), (self.default), verbose=(bool(value == 'specimens')))

    persistent = False
    store_private = False
    title = None
    math_title = None
    visible = False
    widget_type = 'custom'
    tabular = False
    data_type = object
    observable = True
    default = None
    declaration_index = 0
    private_attribute_format = '_%(label)s'

    def _get_private_label(self):
        """ Private attribute label (holds the actual value on the model) """
        return self.private_attribute_format % {'label': self.label}

    def _set(self, instance, value):
        """ Private setter """
        rec_setattr(instance, self._get_private_label(), value)

    def _get(self, instance):
        """ Private getter """
        return rec_getattr(instance, self._get_private_label(), self.default)

    def __call__(self, fget):
        return self.getter(fget)

    def _inject_self(self, f):
        """ Injects self into the arguments of function `f`
           (first argument after self) """

        def wrapper(*args, **kwargs):
            return f(*(args[0] + (self,)) + (args[1:]), **kwargs)

        return wrapper

    def getter(self, fget):
        if len(inspect.getargspec(fget).args) > 1:
            fget = self._inject_self(fget)
        self.fget = fget
        return self

    def setter(self, fset):
        if len(inspect.getargspec(fset).args) > 2:
            fset = self._inject_self(fset)
        self.fset = fset
        return self

    def deleter(self, fdel):
        if len(inspect.getargspec(fdel).args) > 1:
            fdel = self._inject_self(fdel)
        self.fdel = fdel
        return self

    def __init__(self, fget=None, fset=None, fdel=None, doc=None, default=None, label=None, mix_with=None, **kwargs):
        super(LabeledProperty, self).__init__(mix_with=mix_with)
        LabeledProperty.declaration_index += 1
        self.declaration_index = LabeledProperty.declaration_index
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None:
            if fget is not None:
                doc = fget.__doc__
        self.__doc__ = doc
        self.label = self.math_title = self.title = self.description = label
        self.persistent_label = label
        self.default = default
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        return other is not None and self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def __neq__(self, other):
        return not self.__eq__(other)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        with instance._prop_lock:
            if self.fget is None:
                return self._get(instance)
            else:
                return self.fget(instance)

    def __set__(self, instance, value):
        with instance._prop_lock:
            old = getattr(instance, self.label)
            value = ValueWrapper.wrap_value(self.label, value, instance)
            if self.fset is None:
                self._set(instance, value)
            else:
                self.fset(instance, value)
            if self.observable:
                if type(instance).check_value_change(old, value):
                    instance._reset_property_notification(self, old)
                if hasattr(instance, 'notify_property_value_change'):
                    instance.notify_property_value_change(self.label, old, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("Can't delete attribute `%s`!" % self.label)
        self.fdel(instance)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.label)